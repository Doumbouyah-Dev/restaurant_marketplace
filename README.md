# 🍕 Social-First Restaurant Marketplace Platform

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2%20LTS-092E20.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.15%2B-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%2F17-336791.svg)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.x-geography-green.svg)](https://postgis.net/)
[![Redis](https://img.shields.io/badge/Redis-Pub%2FSub%20%26%20Cache-dc382d.svg)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-Async%20Tasks-37814A.svg)](https://docs.celeryq.dev/)
[![License](https://img.shields.io/badge/License-Proprietary-lightgrey.svg)]()

---

## 📌 Executive Summary & Core Value Proposition

The **Social-First Restaurant Marketplace Platform** is an enterprise-grade backend system built to solve the structural fragmentations of modern food discovery and hospitality transactions. Traditional delivery and discovery utilities rely on static text-based filters and high third-party merchant commission structures, divorcing social media culinary engagement from transactional execution.

This platform bridges that gap by fusing short-form visual discovery feeds (dish video clips, tagging, dynamic pricing overlays, and verified reviews) with guaranteed dish pre-ordering, real-time customer-to-vendor WebSocket chat, and vendor-to-vendor collaborative marketing workflows.

```
       [ CULINARY CONSUMERS ]                       [ RESTAURANT VENDORS ]
  +--------------------------------+          +--------------------------------+
  | - Visual Discovery Feed        |          | - Zero Third-Party Commissions |
  | - Real-Time Dish Pre-Ordering  |  =====>  | - Direct Customer Ownership    |
  | - Verified Item Reviews        |  <=====  | - Operational Status Dashboards|
  | - Omnichannel Live Vendor Chat |          | - Co-Marketing Pop-Up Events   |
  +--------------------------------+          +--------------------------------+
                                   \          /
                                    v        v
                        [ ENTERPRISE DJANGO ARCHITECTURE ]
```

---

## 🏗️ High-Level System Architecture

The system utilizes a dual **WSGI** and **ASGI** pipeline running behind an **Nginx** edge routing proxy:
* **Synchronous REST API (`/api/v1/`)**: Processed by **Gunicorn** WSGI workers executing **Django REST Framework (DRF)** endpoints for transactional business logic.
* **Asynchronous WebSockets (`/ws/`)**: Processed by **Daphne / Uvicorn** ASGI workers via **Django Channels** and **Redis Channel Layer** for real-time messaging and live reservation status updates.
* **Spatial & Transactional Storage**: **PostgreSQL** with the **PostGIS** extension utilizing `GEOGRAPHY(Point, 4326)` for radius/proximity calculation, supported by composite B-Tree, GIST, and Trigram GIN indexes.
* **Asynchronous Processing**: **Celery** workers powered by a **Redis** message broker execute video transcoding (via FFmpeg), push notifications, and batch inventory updates.

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT APPLICATIONS                               |
|        React Native (Mobile iOS/Android)  |  Django Templates + Tailwind (Web)   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             NGINX REVERSE PROXY / TLS                             |
+-----------------------------------------------------------------------------------+
                    |                                       |
          (REST Traffic: /api/v1/)                (WebSocket Traffic: /ws/)
                    v                                       v
+---------------------------------------+ +-----------------------------------------+
|            GUNICORN (WSGI)            | |             DAPHNE (ASGI)               |
|      Django REST Framework Core       | |    Django Channels + Redis Pub/Sub     |
+---------------------------------------+ +-----------------------------------------+
                    |                                       |
                    +-------------------+-------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                                PERSISTENCE LAYER                                  |
|   PostgreSQL + PostGIS (Spatial Data) | Redis (Cache/Broker) | AWS S3 (Media)   |
+-----------------------------------------------------------------------------------+
```

---

## 🛠️ Technology Stack Breakdown

| Domain | Technology | Usage & Specification |
| :--- | :--- | :--- |
| **Language** | Python 3.12+ | Core programming runtime |
| **Framework** | Django 5.2 LTS | Backend framework with security support through 2028 |
| **API Layer** | Django REST Framework | RESTful endpoints, serializers, custom permissions |
| **Real-Time Engine** | Django Channels 4.x | Asynchronous WebSocket routing and consumer handling |
| **Authentication** | SimpleJWT | Token rotation, refresh blacklisting, custom ASGI query middleware |
| **Database** | PostgreSQL 16/17 | Primary relational data store |
| **Spatial Engine** | PostGIS 3.x | `GEOGRAPHY(Point, 4326)` spatial point storage and distance queries |
| **Broker & Cache** | Redis | In-memory cache, Celery task queue broker, Channels layer |
| **Task Queue** | Celery 5.x | Asynchronous background processing (FFmpeg, alerts) |
| **Storage** | AWS S3 / MinIO | Object storage for high-resolution images and transcode outputs |

---

## 📁 Repository & Modular Application Structure

The platform enforces a clean, modular Django architecture isolating clear business domains:

```
restaurant-marketplace/
│
├── config/                         # Central Project Configuration
│   ├── __init__.py
│   ├── asgi.py                     # ASGI entrypoint for Django Channels & WebSockets
│   ├── settings.py                 # Environment-aware settings
│   ├── urls.py                     # Root URL routing table
│   └── wsgi.py                     # WSGI entrypoint for Gunicorn
│
├── apps/                           # Modular Domain Applications
│   ├── __init__.py
│   │
│   ├── users/                      # Identity & Access Control
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── managers.py             # CustomUserManager (Email-based)
│   │   ├── models.py               # CustomUser (UUID PK, RBAC: CUSTOMER/VENDOR/ADMIN)
│   │   ├── permissions.py          # IsCustomerUser, IsVendorOwner, IsPlatformAdmin
│   │   ├── serializers.py          # JWT & User profile serializers
│   │   ├── urls.py
│   │   └── views.py                # Auth endpoints (Register, Login, Token Refresh)
│   │
│   ├── catalog/                    # Restaurant Profiles & Menus
│   │   ├── models.py               # VendorProfile (PostGIS Point), Dish
│   │   └── ...
│   │
│   ├── content/                    # Social Content & Discovery
│   │   ├── models.py               # Post, PostMedia, Feed aggregations
│   │   └── ...
│   │
│   ├── bookings/                   # Inventory & Reservation Engine
│   │   ├── models.py               # DishBooking (Atomic transactions, state machine)
│   │   └── ...
│   │
│   ├── events/                     # Collaborative Pop-ups & Marketing
│   │   ├── models.py               # Collaboration, Joint Event entities
│   │   └── ...
│   │
│   └── chat/                       # WebSocket Omnichannel Messaging
│       ├── consumers.py            # Async WebSockets handling JSON frames
│       ├── middleware.py           # WebSocketJWTAuthMiddleware (Query-string decoding)
│       └── models.py               # ChatRoom, ChatMessage
│
├── static/                         # Static Asset Files
├── templates/                      # Django HTML Templates (Vendor Portal UI)
├── .env                            # Environment Variables (Excluded from Git)
├── .env.example                    # Template Environment File
├── .gitignore                      # Git Exclusion Configuration
├── manage.py                       # Django CLI Execution Utility
└── requirements.txt                # Pinned Dependency Declarations
```

---

## 🗄️ Core Database Models & Entity-Relationship Schemas

### 1. Identity & Profiles (`apps/users` & `apps/catalog`)
* **`CustomUser`**: Replaces standard Django User.
  * `id`: `UUID` (Primary Key, `uuid4`)
  * `email`: `VARCHAR(254)` (Unique, Indexed, Primary Login Identifier)
  * `username`: `VARCHAR(150)` (Unique, Indexed, Social Handle)
  * `role`: `VARCHAR(20)` (`CUSTOMER`, `VENDOR`, `ADMIN`)
  * `is_verified`: `BOOLEAN`
* **`VendorProfile`**: 1-to-1 extension of `CustomUser` for `VENDOR` role.
  * `user_id`: `FK -> CustomUser.id` (Unique, On Delete CASCADE)
  * `business_name`: `VARCHAR(255)` (Indexed)
  * `location_point`: `GEOGRAPHY(Point, 4326)` (GIST Indexed)
  * `operating_hours`: `JSONB`

### 2. Catalog & Content (`apps/catalog` & `apps/content`)
* **`Dish`**:
  * `restaurant_id`: `FK -> VendorProfile.id`
  * `price`: `DECIMAL(10, 2)`
  * `daily_stock`: `INTEGER` (Batch limit, `-1` for unconstrained)
* **`Post`**:
  * `author_id`: `FK -> VendorProfile.id`
  * `tagged_dish_id`: `FK -> Dish.id` (Nullable)
  * `created_at`: `TIMESTAMPTZ` (Composite B-Tree indexed with `author_id`)

### 3. Transactions & Messaging (`apps/bookings` & `apps/chat`)
* **`DishBooking`**:
  * `customer_id`: `FK -> CustomUser.id`
  * `dish_id`: `FK -> Dish.id`
  * `booking_status`: `VARCHAR(20)` (`PENDING`, `CONFIRMED`, `READY`, `COMPLETED`, `CANCELLED`)
  * `reserved_slot`: `TIMESTAMPTZ`
* **`ChatMessage`**:
  * `room_id`: `FK -> ChatRoom.id`
  * `sender_id`: `FK -> CustomUser.id`
  * `content`: `TEXT`

---

## ⚡ Key Architectural Patterns & Optimizations

### 1. N+1 Query Elimination Strategy
To maintain sub-200ms database response times on high-volume feed serialization, queries explicitly prefetch relationships and defer heavy JSON attributes:

```python
def get_optimized_social_feed(limit=20, offset=0):
    return (
        Post.objects.select_related("author", "tagged_dish")
        .prefetch_related("media_attachments", "likes")
        .defer("author__operating_hours")
        .filter(author__verification_status="APPROVED")
        .order_by("-created_at")[offset : offset + limit]
    )
```

### 2. Race-Condition Prevention in Bookings
Inventory checking and stock allocation use strict database-level atomic locking (`transaction.atomic()` and `select_for_update()`):

```python
from django.db import transaction

@transaction.atomic
def reserve_dish_stock(dish_id, quantity):
    dish = Dish.objects.select_for_update().get(id=dish_id)
    if dish.daily_stock != -1 and dish.daily_stock < quantity:
        raise ValueError("Insufficient stock available.")
    if dish.daily_stock != -1:
        dish.daily_stock -= quantity
        dish.save()
    return True
```

### 3. JWT WebSocket Handshake Authentication
Because standard browser/mobile WebSocket client handshakes cannot set custom HTTP Authorization headers, authentication extracts and verifies the JWT from URL query parameters before accepting the connection:

```python
# Query string connection syntax: wss://domain.com/ws/chat/<room_id>/?token=<JWT_TOKEN>
class WebSocketJWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope.get("query_string", b"").decode("utf-8"))
        token = query_params.get("token", [None])[0]
        scope["user"] = await get_user_from_token(token) if token else AnonymousUser()
        return await self.inner(scope, receive, send)
```

---

## 🗺️ Project Delivery Roadmap (6 Phases / 11 Sprints)

```
[Phase 1: Weeks 1-4]  ---> [Phase 2: Weeks 5-8]  ---> [Phase 3: Weeks 9-12]
 Core & Identity            Catalog & Social Feed      Bookings & WebSockets
 (Current Phase)

                                                               |
                                                               v

[Phase 6: Weeks 21-24] <--- [Phase 5: Weeks 17-20] <--- [Phase 4: Weeks 13-16]
 QA & Deployment            Indexes & Security         Vendor Dashboard
```

* **Phase 1: Core Foundation & Identity (Weeks 1–4)** — *[IN PROGRESS]*
  * Setup local development environments (Native Windows, PostgreSQL + PostGIS, Redis).
  * Custom `UUID`-based user model, DRF simple JWT integration, identity permissions.
* **Phase 2: Catalog Management & Content Feeds (Weeks 5–8)**
  * Restaurant profiles, PostGIS spatial point configuration, dish catalog management.
  * S3 storage integration, media upload handlers, Celery + FFmpeg transcode pipeline.
* **Phase 3: Booking Engine & WebSocket Messaging (Weeks 9–12)**
  * Atomic stock reservation state machine, QR code generation.
  * ASGI setup, Django Channels integration, custom WebSocket query-string JWT middleware.
* **Phase 4: Vendor Portal & Collaboration Engine (Weeks 13–16)**
  * Django Templates + Tailwind CSS server-rendered vendor control dashboard.
  * Real-time order update board, vendor-to-vendor pop-up event collaboration.
* **Phase 5: Database Optimization & Security Hardening (Weeks 17–20)**
  * PostGIS GIST indexes, Trigram GIN fuzzy search, ORM profiling (`select_related`/`defer`).
  * Rate limiting, Redis caching layers, security audit sweeps.
* **Phase 6: QA, Load Testing & Production Deployment (Weeks 21–24)**
  * Locust load testing (WebSocket concurrency + REST throughput), Nginx TLS configuration, App Store/Play Store asset finalization.

---

## 🚀 Quick-Start Development Setup (Local / Docker-Free)

### Prerequisites
* **Python 3.12+**
* **PostgreSQL 16/17** with **PostGIS 3.x Extension**
* **Redis** (via WSL2 Ubuntu or native Windows service)
* **Git**

### Step 1: Clone Repository & Setup Virtual Environment
```powershell
git clone https://github.com/your-org/restaurant-marketplace.git
cd restaurant-marketplace

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file at the root directory based on `.env.example`:
```env
SECRET_KEY=your-local-development-secret-key-change-in-production
DEBUG=True
DB_NAME=restaurant_marketplace
DB_USER=restaurant_app
DB_PASSWORD=your_secure_password
DB_HOST=127.0.0.1
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/0
```

### Step 4: Prepare PostgreSQL & PostGIS Database
Execute in pgAdmin or `psql`:
```sql
CREATE DATABASE restaurant_marketplace;
\c restaurant_marketplace;
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Full_Version(); -- Verify PostGIS installation
```

### Step 5: Execute Database Migrations & Run Development Server
```powershell
# Validate configuration state
python manage.py check

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver
```

---

## 🧪 Verification & System Health Checks

Run the Django connection verification check in shell:
```powershell
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Database Vendor:', connection.vendor)"
```

Execute unit tests:
```powershell
python manage.py test apps.users
```

---

## 🔒 Security & Code Standards

* **Secrets Isolation**: No database passwords, API credentials, or secret keys are committed to Git (`.env` is explicitly ignored).
* **Role Enforcement**: Every API endpoint must be protected by explicit DRF permission classes (`IsCustomerUser`, `IsVendorOwner`, `IsPlatformAdmin`).
* **Database Integrity**: Spatial types must use `GEOGRAPHY(Point, 4326)` for precise meter-based calculations without planar distortion.
```

---

### Summary of What Was Generated
I have assembled and generated a complete, highly detailed `README.md` file tailored to your PRD and architectural requirements. It covers:
1. Executive summary & technical stakeholder value matrix.
2. Complete architectural diagram (WSGI + ASGI, Redis, PostgreSQL/PostGIS, Celery).
3. Technology stack table with pinned versions and responsibilities.
4. Modular directory layout (`apps/users`, `apps/catalog`, `apps/chat`, etc.).
5. Database models schema breakdown including custom user fields and relationships.
6. Crucial code snippet implementations (N+1 query elimination, atomic stock handling, query-string JWT middleware).
7. Full 6-Phase / 11-Sprint execution roadmap.
8. Native Windows / Docker-free step-by-step installation instructions.

You can now save this file directly into your repository root directory!