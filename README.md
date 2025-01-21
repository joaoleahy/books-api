# Books API

A robust REST API for managing books with automatic data enrichment from Google Books API. Built with Django REST Framework and featuring Redis caching, JWT authentication, and Swagger documentation.

## 🚀 Features

- **CRUD Operations for Books**
  - Create, Read, Update, and Delete books
  - Automatic data enrichment from Google Books API
  - Input validation and error handling

- **Data Enrichment**
  - Automatic fetching of additional book data from Google Books API
  - Enriched data includes:
    - Book cover images
    - Publisher information
    - Page count
    - Categories
    - Ratings and reviews
    - Description
    - Preview links

- **Caching System**
  - Redis-based caching
  - Cache invalidation strategies
  - Configurable TTL (Time To Live)
  - Performance optimization

- **Authentication & Security**
  - JWT (JSON Web Token) authentication
  - Token refresh mechanism
  - Protected endpoints
  - Role-based access control

- **API Documentation**
  - Interactive Swagger UI
  - ReDoc alternative interface
  - Detailed endpoint descriptions
  - Request/Response examples

## 🛠 Tech Stack

- **Backend Framework**: Django 4.2
- **API Framework**: Django REST Framework 3.14
- **Database**: PostgreSQL 15
- **Caching**: Redis 7
- **Documentation**: drf-spectacular
- **Authentication**: djangorestframework-simplejwt
- **Containerization**: Docker & Docker Compose
- **Proxy Server**: Nginx
- **Testing**: pytest

## 🏗 Architecture

```
├── nginx/              # Nginx configuration
├── books/             # Main application
│   ├── api/          # API endpoints
│   │   ├── migrations/    # Database migrations
│   │   ├── services/     # External services
│   │   │   ├── cache.py  # Caching service
│   │   │   └── enrichment.py  # Google Books integration
│   │   ├── admin.py      # Admin interface
│   │   ├── models.py     # Database models
│   │   ├── serializers.py # API serializers
│   │   ├── urls.py       # URL routing
│   │   └── views.py      # API views
│   ├── core/         # Core functionality
│   └── tests/        # Test suites
└── core/             # Project settings
```

## 🚦 Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd books-api
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Build and run the containers:
   ```bash
   docker compose up --build
   ```

3. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

4. Create a superuser to access the admin interface:
```bash
docker-compose exec web python manage.py createsuperuser
```

5. Load sample data (optional):
```bash
docker-compose exec web python manage.py seed_books
```

The API will be available at `http://localhost`

### Environment Variables

- `DEBUG`: Enable/disable debug mode
- `DJANGO_SETTINGS_MODULE`: Django settings module
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `REDIS_URL`: Redis connection URL

## 📚 API Documentation

### Authentication

There are two ways to obtain the JWT token for authentication:

#### Option 1: Using curl

1. Obtain JWT token:
   ```bash
   curl -X POST http://localhost/api/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "your_username", "password": "your_password"}'
   ```

2. Use the token in requests:
   ```bash
   curl http://localhost/api/books/ \
        -H "Authorization: Bearer your_token_here"
   ```

#### Option 2: Using the endpoint directly

1. Make a POST request to `/api/token/` with the following body:
   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. The response will be in the format:
   ```json
   {
     "access": "your_jwt_token_here",
     "refresh": "your_refresh_token_here"
   }
   ```

3. To use the token, add the `Authorization` header in all requests:
   ```
   Authorization: Bearer your_jwt_token_here
   ```

4. To renew an expired token, use the `/api/token/refresh/` endpoint with the refresh token:
   ```json
   {
     "refresh": "your_refresh_token_here"
   }
   ```

### Available Endpoints

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token
- `GET /api/books/`: List all books
- `POST /api/books/`: Create a new book
- `GET /api/books/{id}/`: Get book details
- `PUT /api/books/{id}/`: Update a book
- `DELETE /api/books/{id}/`: Delete a book
- `POST /api/books/{id}/refresh_enriched_data/`: Refresh book's enriched data

### Documentation Interfaces

- Swagger UI: `http://localhost/api/docs/`
- ReDoc: `http://localhost/api/redoc/`

## 🔧 Development

### Project Structure

```
books-api/
├── books/
│   ├── migrations/    # Database migrations
│   ├── services/     # External services
│   │   ├── cache.py  # Caching service
│   │   └── enrichment.py  # Google Books integration
│   │   ├── admin.py      # Admin interface
│   │   ├── models.py     # Database models
│   │   ├── serializers.py # API serializers
│   │   ├── urls.py       # URL routing
│   │   └── views.py      # API views
│   ├── core/             # Project settings
│   ├── nginx/            # Nginx configuration
│   ├── docker-compose.yml
│   └── requirements.txt
├── nginx/            # Nginx configuration
└── docker-compose.yml
```

### Running Tests

The project has comprehensive test coverage with different types of tests:

- Unit Tests
- Integration Tests
- API Tests
- Cache Tests
- Error Tests

To run tests with coverage report:
```bash
# Run tests
docker-compose exec web pytest

# Run tests with coverage
docker-compose exec web coverage run -m pytest
docker-compose exec web coverage report
```

Current test coverage is 99%, which is excellent for a production project. The only 3 uncovered statements are specific error paths in the services layer that are challenging to simulate in tests, such as rare API response scenarios and specific JSON parsing errors.

Coverage by file:
- `models.py`: 100%
- `views.py`: 100%
- `services.py`: 93%
- `serializers.py`: 100%
- `urls.py`: 100%
- `admin.py`: 100%
- `tests.py`: 100%

### Code Style

The project follows PEP 8 guidelines and uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

## 🔍 Monitoring

### Logging

- Application logs: Available through Docker Compose logs
- Nginx access logs: Available in the nginx container
- Cache operations: Logged at INFO level
- API requests: Logged with detailed information

### Performance

- Redis caching reduces load on Google Books API
- Nginx serves as reverse proxy and load balancer
- Database queries are optimized with proper indexing

## 🚀 Deployment

### Production Considerations

1. Update environment variables:
   - Set `DEBUG=0`
   - Use strong passwords
   - Configure proper Redis and PostgreSQL settings

2. Security measures:
   - Enable HTTPS
   - Configure proper CORS settings
   - Implement rate limiting
   - Use secure headers

3. Performance optimization:
   - Configure proper cache settings
   - Optimize database queries
   - Set up monitoring

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.