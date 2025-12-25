class AuthenticationFailed(Exception):
    pass


class RateLimitExceeded(Exception):
    """Raised when login rate limit is exceeded."""
    
    def __init__(self, retry_after_seconds: int = 60):
        self.retry_after_seconds = retry_after_seconds
        super().__init__(
            f"Too many login attempts. Please try again in {retry_after_seconds} seconds."
        )
