class AppError(Exception):
    """Base exception for all custom app errors."""
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BadRequestError(AppError):
    """400 - Invalid input or missing fields."""
    def __init__(self, message='Bad request'):
        super().__init__(message, 400)


class UnauthorizedError(AppError):
    """401 - Missing or invalid token."""
    def __init__(self, message='Missing or invalid token'):
        super().__init__(message, 401)


class ForbiddenError(AppError):
    """403 - Access denied to this resource."""
    def __init__(self, message='Access denied'):
        super().__init__(message, 403)


class NotFoundError(AppError):
    """404 - Resource not found."""
    def __init__(self, message='Resource not found'):
        super().__init__(message, 404)


class ConflictError(AppError):
    """409 - Duplicate or conflicting data."""
    def __init__(self, message='Resource already exists'):
        super().__init__(message, 409)


class RateLimitError(AppError):
    """429 - Daily request limit reached."""
    def __init__(self, message='Daily request limit reached'):
        super().__init__(message, 429)


class OpenAIError(AppError):
    """500 - OpenAI API call failed."""
    def __init__(self, message='AI service error'):
        super().__init__(message, 500)