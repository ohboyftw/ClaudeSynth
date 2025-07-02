# Project Guidelines

## API Design
- All new endpoints must be under the `/api/v1/` prefix
- Use Pydantic for request and response models
- Always include clear success and error responses
- Use appropriate HTTP status codes

## Code Style
- Use type hints for all function signatures
- Follow PEP 8 naming conventions
- Add docstrings for all public functions and classes

## Architecture
- Business logic should be separated from endpoint handlers if complex
- Use dependency injection for database connections
- Keep models in separate files from endpoints

## Error Handling
- Use FastAPI's HTTPException for API errors
- Provide meaningful error messages
- Log errors for debugging purposes