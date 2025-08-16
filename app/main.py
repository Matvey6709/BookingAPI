import time
from contextlib import asynccontextmanager
from datetime import date
from typing import Optional
from urllib.request import Request

import aioredis
# import uvicorn
from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import s
from app.database import engine
from fastapi import Depends, FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from pydantic import BaseModel
from sqladmin import Admin, ModelView
from starlette.middleware.cors import CORSMiddleware
from app.users.router import router as router_users
from app.logger import logger
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import start_http_server
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.requests import Request
from fastapi import FastAPI, Response
import time

from app.logger import logger



@asynccontextmanager
async def startup(app: FastAPI):
    redis = aioredis.create_redis_pool(
        f"redis://{s.REDIS_HOST}:{s.REDIS_PORT}", encoding="utf8"
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=startup)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)

app.include_router(router_pages)
app.include_router(router_images)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow=Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['.*admin.*', '/metrics']
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


# @app.middleware('http')
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers['X-Process-Time'] = str(process_time)
#     logger.info('Request handling time', extra={
#         'process_time': round(process_time, 4)
#     })
#     return response

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
ERROR_COUNT = Counter("http_errors_total", "Total HTTP Errors", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint"])

EXCLUDED_PATHS = ["/metrics", "/favicon.ico", "/app/static"]

# @app.middleware("http")
# async def metrics_middleware(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#
#     response.headers['X-Process-Time'] = str(process_time)
#
#     endpoint = request.url.path
#
#     if not any(endpoint.startswith(p) for p in EXCLUDED_PATHS):
#         logger.info(f'Request handling time {endpoint}', extra={
#             'process_time': round(process_time, 4)
#         })
#         REQUEST_COUNT.labels(request.method,  response.status_code).inc()
#         REQUEST_LATENCY.labels(endpoint).observe(process_time)
#
#         if response.status_code >= 400:
#             ERROR_COUNT.labels(request.method, endpoint).inc()
#
#     return response

# @app.get("/metrics")
# def metrics():
#     return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.mount("/app/static", StaticFiles(directory="app/static/"), "static")


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")

