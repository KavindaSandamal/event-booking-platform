from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from .models import Base, Event
from .schemas import EventIn, EventOut
from typing import List

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/eventdb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="Catalog Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.on_event("startup")
async def startup():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Seed data if database is empty
    db = SessionLocal()
    try:
        event_count = db.query(Event).count()
        if event_count == 0:
            events = [
                Event(
                    title="Rock Concert 2024",
                    description="An amazing rock concert featuring top artists",
                    venue="Madison Square Garden",
                    date="2024-06-15",
                    time="19:00",
                    price=75.0,
                    available_seats=1000
                ),
                Event(
                    title="Jazz Night",
                    description="Smooth jazz evening with live performances",
                    venue="Blue Note Jazz Club",
                    date="2024-06-20",
                    time="20:00",
                    price=45.0,
                    available_seats=200
                ),
                Event(
                    title="Classical Symphony",
                    description="Beethoven's 9th Symphony performed by the Philharmonic",
                    venue="Carnegie Hall",
                    date="2024-07-01",
                    time="19:30",
                    price=120.0,
                    available_seats=500
                ),
                Event(
                    title="Comedy Night",
                    description="Stand-up comedy featuring top comedians",
                    venue="Comedy Cellar",
                    date="2024-06-25",
                    time="21:00",
                    price=35.0,
                    available_seats=150
                ),
                Event(
                    title="Dance Performance",
                    description="Contemporary dance performance by renowned artists",
                    venue="Lincoln Center",
                    date="2024-07-10",
                    time="20:00",
                    price=85.0,
                    available_seats=300
                ),
                Event(
                    title="Opera Night",
                    description="La Traviata performed by the Metropolitan Opera",
                    venue="Metropolitan Opera House",
                    date="2024-07-15",
                    time="19:00",
                    price=150.0,
                    available_seats=400
                ),
                Event(
                    title="Folk Music Festival",
                    description="Traditional and modern folk music celebration",
                    venue="Central Park",
                    date="2024-07-20",
                    time="18:00",
                    price=25.0,
                    available_seats=2000
                ),
                Event(
                    title="Electronic Music Rave",
                    description="High-energy electronic music festival",
                    venue="Brooklyn Warehouse",
                    date="2024-07-25",
                    time="22:00",
                    price=60.0,
                    available_seats=800
                )
            ]
            db.add_all(events)
            db.commit()
    finally:
        db.close()

@app.get("/events", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

@app.get("/events/{event_id}", response_model=EventOut)
def get_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(404, "Not found")
    return event

@app.post("/events", response_model=EventOut)
def create_event(payload: EventIn, db: Session = Depends(get_db)):
    event = Event(**payload.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@app.put("/events/{event_id}/capacity")
def update_event_capacity(event_id: str, seats: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    
    if event.capacity < seats:
        raise HTTPException(400, "Not enough capacity available")
    
    event.capacity -= seats
    db.commit()
    db.refresh(event)
    return {"message": "Capacity updated successfully", "remaining_capacity": event.capacity}
