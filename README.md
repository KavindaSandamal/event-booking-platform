# Event Ticket Booking Platform (Demo)

## Prerequisites

- Docker & Docker Compose installed
- (Optional) Node & npm to run frontend locally

## Setup

1. **Create environment file**: Copy `env.example` to `.env` and adjust values if needed:
   ```bash
   cp env.example .env
   ```

2. **Build & start services**:
   ```bash
   docker compose up --build
   ```

This will start:

- Postgres (5432)
- Redis (6379)
- RabbitMQ (5672, management 15672)
- Auth service: http://localhost:8001
- Catalog service: http://localhost:8002
- Booking service: http://localhost:8003
- Payment service: http://localhost:8004
- Frontend: http://localhost:3000

## Demo Flow

1. Visit frontend `http://localhost:3000`
2. **Register** in a separate modal window (Create Account button)
3. **Login** with your credentials
4. **Browse Events** tab to view available events
5. **Book an event** by selecting seats
6. **Complete payment** with phone verification:
   - Enter phone number
   - Receive 6-digit verification code (check console logs)
   - Enter code to confirm payment
7. **View your bookings** in the "My Bookings" tab
8. **Real-time capacity updates** - event capacity reduces after booking

## New Features

### 🆕 **User Registration Modal**
- Separate window-like interface for account creation
- Password confirmation and validation
- Clean, modern UI design

### 🆕 **Event Capacity Management**
- Real-time capacity reduction when bookings are made
- Prevents overbooking
- Capacity updates across all services

### 🆕 **Payment System with Phone Verification**
- **Payment Service**: Handles payment processing
- **Phone Verification**: 6-digit SMS-like verification codes
- **Two-step Process**: Phone number → Verification code → Payment confirmation
- **Real-time Updates**: Booking status changes to "confirmed" after payment
- **Demo Mode**: Verification codes are printed to console (in production, SMS would be sent)

## Architecture

- **Frontend**: React 18 + Vite with modal-based UI
- **Backend**: FastAPI microservices with CORS support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for session management and verification codes
- **Message Queue**: RabbitMQ for async processing
- **Authentication**: JWT tokens with bcrypt password hashing
- **Payment**: Secure phone verification system

## Service Communication

```
Frontend → Auth Service (login/register)
Frontend → Catalog Service (browse events)
Frontend → Booking Service (create bookings)
Frontend → Payment Service (payment + verification)
Booking Service → Catalog Service (update capacity)
Payment Service → Booking Service (confirm bookings)
```

## Notes

- This demo uses simple SQLAlchemy `create_all()` (no migrations).
- For production: add migrations, proper token storage, HTTPS, secrets management, and robust error handling.
- All services use modern SQLAlchemy 2.0+ syntax and Python 3.11+.
- **Payment verification codes** are printed to console for demo purposes.
- **Event capacity** is automatically managed and updated in real-time.
