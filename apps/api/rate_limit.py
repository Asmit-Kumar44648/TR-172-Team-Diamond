import os

# Upstash Redis — optional, degrades gracefully
redis = None
try:
    from upstash_redis import Redis
    REDIS_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
    REDIS_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
    if REDIS_URL and REDIS_TOKEN:
        redis = Redis(url=REDIS_URL, token=REDIS_TOKEN)
        print("[RateLimit] Upstash Redis connected.")
    else:
        print("[RateLimit] Redis credentials missing — rate limiting disabled.")
except Exception as e:
    print(f"[RateLimit] Redis init failed: {e}")

DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"

PLAN_LIMITS = {
    "free": {"daily_requests": 1000, "max_upload_mb": 100},
}


def get_plan_limits(plan: str = "free"):
    """Returns (daily_requests, max_upload_mb)."""
    cfg = PLAN_LIMITS["free"]
    return cfg["daily_requests"], cfg["max_upload_mb"]


def check_rate_limit(org_id: str, plan: str) -> None:
    """
    Atomic daily rate limit check via Redis.
    Skips silently in DEMO_MODE or when Redis is unavailable.
    """
    if DEMO_MODE or redis is None:
        return  # unlimited in demo

    from datetime import date
    from fastapi import HTTPException

    daily_quota, _ = get_plan_limits(plan)
    key = f"rate:{org_id}:{date.today().isoformat()}"

    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 86400)  # 24 h TTL on first hit

    if count > daily_quota:
        raise HTTPException(
            status_code=429,
            detail=f"Daily quota of {daily_quota} requests exceeded for plan '{plan}'.",
        )
