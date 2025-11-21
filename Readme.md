# Brain.com.ua Parser

A web scraper for collecting product information from brain.com.ua using Selenium (undetected-chromedriver) with Django ORM and PostgreSQL database.

## Features

- 🔍 Automated product search on brain.com.ua
- 📊 Complete product data extraction (prices, specifications, photos, reviews)
- 💾 PostgreSQL database storage with Django ORM
- 📁 CSV export functionality
- 🤖 Anti-detection with undetected-chromedriver
- 📝 Comprehensive logging

## Tech Stack

- **Python** 3.10+
- **Django** 5.2.8 - ORM and data models
- **Selenium** 4.38.0 with undetected-chromedriver 3.5.5
- **PostgreSQL** 15 (Docker)
- **Poetry** - dependency management
- **pandas** - CSV export

## Dependencies

- Python 3.10 or higher
- Poetry (dependency manager)
- Docker & Docker Compose
- Google Chrome 131

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd braincomua-project
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Create `.env` file
Create a `.env` file in the `braincomua_project/` directory:

```env
SECRET_KEY=your-secret-django-key-here
POSTGRES_DB=braincomua
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
```

### 4. Start PostgreSQL
```bash
docker-compose up -d
```

### 5. Apply Django migrations
```bash
cd braincomua_project
poetry run python manage.py migrate
```

## Usage

### Run the parser
```bash
poetry run python modules/1_selenium_parser.py
```

The parser will:
1. Navigate to brain.com.ua
2. Search for "Apple iPhone 15 128GB Black"
3. Extract complete product information
4. Save data to PostgreSQL database
5. Export results to `results/products.csv`

### Access Django admin (optional)
```bash
cd braincomua_project
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```
Then visit `http://localhost:8000/admin/`

## Project Structure

```
.
├── braincomua_project/              # Django project
│   ├── braincomua_project/          # Main settings package
│   │   ├── settings.py              # Django settings (DB, apps, etc.)
│   │   ├── urls.py                  # URL routing
│   │   └── ...
│   ├── parser_app/                  # Django app for parser
│   │   ├── models.py                # Product model
│   │   ├── admin.py                 # Admin interface
│   │   └── migrations/              # Database migrations
│   └── manage.py                    # Django management script
│
├── modules/                         # Selenium parser modules
│   ├── 1_selenium_parser.py         # Main parser script
│   ├── load_django.py               # Django environment loader
│   ├── config/                      # Configuration
│   │   ├── driver_config.py         # Undetected-chromedriver setup
│   │   └── logger_config.py         # Logging configuration
│   └── utils/                       # Utility modules
│       ├── collect_products.py      # Product data extraction logic
│       └── search_product.py        # Search & navigation logic
│
├── results/                         # Output directory
│   └── products.csv                 # Exported product data
│
├── pyproject.toml                   # Poetry dependencies
├── docker-compose.yml               # PostgreSQL container
└── parser.log                       # Application logs (auto-generated)
```

## Logging

All parser operations are logged to `parser.log` with timestamps and severity levels.

## Configuration

### Chrome Driver
The parser uses `undetected-chromedriver` to bypass bot detection:
- Chrome version: 131 (specified in `modules/config/driver_config.py`)
- Headless mode enabled
- Anti-detection features configured

### Database
PostgreSQL configuration in `docker-compose.yml`:
- Port: 5432
- Database: braincomua
- User: admin
- Password: admin