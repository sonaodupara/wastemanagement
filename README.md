# WasteSmart - Smart Waste Management & AI Classification System

[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini AI](https://img.shields.io/badge/Google%20Gemini%20AI-Multimodal-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**WasteSmart** is a digital platform designed to modernize municipal and private waste management operations. The platform connects citizens, waste collection agencies, field staff, and system administrators through a centralized web application and RESTful API backend equipped with **AI-powered waste classification**.

---

## Key Features & Role-Based Portals

### System Administration Portal
- **Pickup Agency Onboarding**: Verify, approve, or reject new waste collection companies.
- **Master Rate & Category Management**: Dynamically configure waste types (e.g., Organic, E-Waste, Recyclable) and pricing per kg.
- **User & Staff Directory**: Complete oversight of registered citizens and field agents.
- **Resolution Center**: Monitor citizen complaints, feedback, and SLA compliance.

### Pickup Company Portal
- **Service Zone Coverage**: Manage assigned geographic regions, sub-areas, and collection routes.
- **Workforce Management**: Onboard and assign drivers and field technicians to pickup requests.
- **Billing & Invoicing**: Upload digital collection receipts and manage payment tracking.
- **Real-Time Communication**: In-app messaging system to communicate directly with citizens.

### Field Staff / Driver Portal
- **Task Management**: Access daily assigned pickup schedules and route details.
- **Status Updates**: Mark pickups as pending, in-progress, or completed.
- **Payment Verification**: Log on-site cash/digital payments collected from citizens.

### Citizen / User Portal
- **On-Demand Requests**: Schedule waste collection pickups with location tagging.
- **Status Tracking**: Real-time status updates from request to completion.
- **Direct Messaging**: Chat directly with assigned pickup providers.
- **Gemini AI Waste Identification**: Upload photos of waste items to automatically classify waste type using computer vision.

---

## Tech Stack & Architecture

| Domain | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.10+, Django 5.x |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Artificial Intelligence** | Google Gemini Flash Vision API (`google-generativeai`) |
| **Database** | MySQL (Production) / SQLite3 (Zero-config Dev) |
| **Security** | Environment-isolated secrets (`python-dotenv`), Django Auth, CSRF Guards |

---

## Repository Structure

```text
wastemanagement/
├── .env.example              # Template for environment variables
├── .gitignore                # Production-grade git ignore patterns
├── LICENSE                   # Open-source MIT License
├── README.md                 # Project documentation
├── manage.py                 # Django CLI runner
├── requirements.txt          # Python dependencies
├── media/                    # User & AI upload directory
├── templates/                # HTML layout templates
├── wastemanagement/          # Django core settings & routing
│   ├── settings.py           # Configured for environment variables
│   ├── urls.py               # Main URL dispatcher
│   └── wsgi.py               # WSGI entry point
└── myapp/                    # Core application logic
    ├── models.py             # ORM models (Users, Pickup, Staff, WasteRequest, etc.)
    ├── views.py              # Business logic & AI endpoints
    ├── urls.py               # Application URL routes
    └── static/               # CSS, JavaScript, assets
```

---

## Quick Start Guide

### Prerequisites
- **Python**: `3.10` or higher
- **Git**: Installed on your system
- **MySQL** *(Optional)*: Or use SQLite out-of-the-box

### 1. Clone the Repository
```bash
git clone https://github.com/sonaodupara/wastemanagement.git
cd wastemanagement
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and configure your settings:
```ini
SECRET_KEY=your-custom-django-secret-key
DEBUG=True

# To use SQLite instantly without MySQL:
USE_SQLITE=True

# Add your Gemini AI key for AI image classification:
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Launch Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/myapp/login_get/` in your browser.

---

## API Endpoints & AI Integration

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/myapp/userupload/` | `POST` | Uploads waste image (`photo`), runs Gemini Vision model, returns waste type JSON. |
| `/myapp/User_sendchat/` | `POST` | Sends in-app chat message between citizen and pickup agency. |
| `/myapp/User_viewchat/` | `POST` | Retrieves chat history between two user accounts. |

---

## Security & Best Practices

- **Environment-Based Configuration**: All sensitive values (Secret Key, DB credentials, AI API keys) are managed strictly via `.env`.
- **CSRF Protection**: Native Django CSRF token validation enabled across web forms.
- **Modular Architecture**: Decoupled models, views, templates, and static assets following standard Django patterns.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Developed by **Sona Odupara**.
