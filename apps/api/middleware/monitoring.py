import time
import logging
import traceback
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger("apps.api.monitoring")
logger.setLevel(logging.INFO)

# Structured Logging Implementation
class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        
        # Don't log sensitive health check noise in production
        path = request.url.path
        if path == "/health":
            return await call_next(request)

        try:
            response = await call_next(request)
            
            process_time = (time.perf_counter() - start_time) * 1000
            
            # Request timing log
            logger.info(
                f"method={request.method} path={path} "
                f"status={response.status_code} "
                f"duration={process_time:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            process_time = (time.perf_counter() - start_time) * 1000
            
            # Error tracking log with traceback
            logger.error(
                f"CRITICAL_ERROR method={request.method} path={path} "
                f"duration={process_time:.2f}ms\n"
                f"{traceback.format_exc()}"
            )
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "detail": "An unexpected error occurred. Team has been notified.",
                    "job_id": None
                }
            )

# Optional: Integration with external monitoring like Highlight.io or Sentry
# would happen here by wrapping logger/traceback calls.
