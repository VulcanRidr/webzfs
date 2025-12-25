"""
Rate limiting for login attempts.
Implements a sliding window rate limiter to prevent brute force attacks.
"""
import time
from collections import defaultdict
from dataclasses import dataclass, field
from threading import Lock
from typing import Dict, List


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    max_attempts: int = 5
    window_seconds: int = 60


@dataclass
class AttemptTracker:
    """Tracks login attempts for a single IP address."""
    attempts: List[float] = field(default_factory=list)
    lock: Lock = field(default_factory=Lock)
    
    def add_attempt(self, timestamp: float) -> None:
        """Record a new login attempt."""
        with self.lock:
            self.attempts.append(timestamp)
    
    def get_attempts_in_window(self, window_start: float) -> int:
        """Get the number of attempts within the time window."""
        with self.lock:
            # Clean up old attempts
            self.attempts = [t for t in self.attempts if t >= window_start]
            return len(self.attempts)
    
    def get_oldest_attempt_in_window(self, window_start: float) -> float | None:
        """Get the oldest attempt timestamp within the window."""
        with self.lock:
            valid_attempts = [t for t in self.attempts if t >= window_start]
            return min(valid_attempts) if valid_attempts else None


class LoginRateLimiter:
    """
    Rate limiter for login attempts using a sliding window algorithm.
    Tracks failed login attempts per IP address and blocks excessive attempts.
    """
    
    def __init__(self, config: RateLimitConfig | None = None):
        self.config = config or RateLimitConfig()
        self._trackers: Dict[str, AttemptTracker] = defaultdict(AttemptTracker)
        self._global_lock = Lock()
    
    def _get_tracker(self, ip_address: str) -> AttemptTracker:
        """Get or create an attempt tracker for an IP address."""
        with self._global_lock:
            return self._trackers[ip_address]
    
    def is_rate_limited(self, ip_address: str) -> bool:
        """
        Check if an IP address is currently rate limited.
        
        Args:
            ip_address: The client's IP address
            
        Returns:
            True if the IP is rate limited, False otherwise
        """
        tracker = self._get_tracker(ip_address)
        window_start = time.time() - self.config.window_seconds
        attempt_count = tracker.get_attempts_in_window(window_start)
        return attempt_count >= self.config.max_attempts
    
    def record_failed_attempt(self, ip_address: str) -> None:
        """
        Record a failed login attempt for an IP address.
        
        Args:
            ip_address: The client's IP address
        """
        tracker = self._get_tracker(ip_address)
        tracker.add_attempt(time.time())
    
    def get_remaining_attempts(self, ip_address: str) -> int:
        """
        Get the number of remaining login attempts for an IP address.
        
        Args:
            ip_address: The client's IP address
            
        Returns:
            Number of remaining attempts before rate limiting kicks in
        """
        tracker = self._get_tracker(ip_address)
        window_start = time.time() - self.config.window_seconds
        attempt_count = tracker.get_attempts_in_window(window_start)
        return max(0, self.config.max_attempts - attempt_count)
    
    def get_retry_after_seconds(self, ip_address: str) -> int:
        """
        Get the number of seconds until the rate limit resets for an IP.
        
        Args:
            ip_address: The client's IP address
            
        Returns:
            Seconds until the oldest attempt expires from the window
        """
        tracker = self._get_tracker(ip_address)
        window_start = time.time() - self.config.window_seconds
        oldest_attempt = tracker.get_oldest_attempt_in_window(window_start)
        
        if oldest_attempt is None:
            return 0
        
        # Calculate when the oldest attempt will expire from the window
        expires_at = oldest_attempt + self.config.window_seconds
        retry_after = max(0, int(expires_at - time.time()) + 1)
        return retry_after
    
    def reset(self, ip_address: str) -> None:
        """
        Reset the rate limit for an IP address (e.g., after successful login).
        
        Args:
            ip_address: The client's IP address
        """
        with self._global_lock:
            if ip_address in self._trackers:
                del self._trackers[ip_address]
    
    def cleanup_old_entries(self) -> None:
        """Remove expired entries to prevent memory growth."""
        current_time = time.time()
        window_start = current_time - self.config.window_seconds
        
        with self._global_lock:
            # Find IPs with no recent attempts
            expired_ips = []
            for ip, tracker in self._trackers.items():
                if tracker.get_attempts_in_window(window_start) == 0:
                    expired_ips.append(ip)
            
            # Remove expired entries
            for ip in expired_ips:
                del self._trackers[ip]


# Global rate limiter instance
# Default: 5 attempts per 60 seconds
login_rate_limiter = LoginRateLimiter(RateLimitConfig(max_attempts=5, window_seconds=60))
