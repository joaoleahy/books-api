# Book Management API

RESTful API developed with Django for book management, including integration with external services and caching system.

## Technologies Used

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis (for caching)
- Docker and Docker Compose
- OpenAPI 3.0 (Swagger)

## Requirements

- Docker
- Docker Compose

## How to Run

1. Clone the repository:
```bash
git clone git@github.com:joaoleahy/books-api.git
cd books-api
```

2. Start the containers:
```bash
docker-compose up --build
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

6. Access the application:
- API Documentation:
  - Swagger UI: http://localhost:8000/api/docs/
  - ReDoc: http://localhost:8000/api/redoc/
  - OpenAPI Schema: http://localhost:8000/api/schema/
- API Endpoints: http://localhost:8000/api/
- Admin Interface: http://localhost:8000/admin/

## Project Structure

- `core/`: Main Django settings
- `books/`: Main application with models and views
- `tests/`: Unit and integration tests

## API Documentation

The API is documented using OpenAPI 3.0 (Swagger) specification. You can access the documentation in three different formats:

1. **Swagger UI**: Interactive documentation where you can:
   - Read detailed API documentation
   - Test endpoints directly from the browser
   - See request/response examples
   - Access: http://localhost:8000/api/docs/

2. **ReDoc**: Clean and elegant documentation format:
   - More readable for non-technical users
   - Better for printing and sharing
   - Access: http://localhost:8000/api/redoc/

3. **Raw Schema**: OpenAPI schema in JSON format:
   - Use for generating client code
   - Import into other tools
   - Access: http://localhost:8000/api/schema/

## API Endpoints

- `GET /api/books/`: List all books
- `POST /api/books/`: Create a new book
- `GET /api/books/{id}/`: Get book details
- `PUT /api/books/{id}/`: Update a book
- `DELETE /api/books/{id}/`: Delete a book
- `POST /api/books/{id}/refresh_enriched_data/`: Update book's enriched data

## Admin Interface

The Django admin interface provides a user-friendly way to manage books. Features include:
- List view with sorting and filtering
- Search functionality
- Detailed book view with organized sections
- Automatic form validation
- Rich text editing for descriptions

## Development

### Testing

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