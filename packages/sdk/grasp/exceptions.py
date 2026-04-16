class GRASPError(Exception):
    """Base exception for all GRASP SDK errors."""
    pass

class GRASPAuthError(GRASPError):
    """Raised on authentication failures (401/403)."""
    pass

class GRASPRateLimitError(GRASPError):
    """Raised when daily quota or rate limits are exceeded (429)."""
    pass

class GRASPTimeoutError(GRASPError):
    """Raised when an operation (like wait()) times out."""
    pass

class GRASPAPIError(GRASPError):
    """Raised for general API errors (5xx or unexpected 4xx)."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
