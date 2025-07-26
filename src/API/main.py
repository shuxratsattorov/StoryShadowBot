import pytz
import datetime
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.database import factory
from src.database import base as db
from src.config.config import settings
from src.API.routers import routers_prefixs_tags


toshkent_tz = pytz.timezone('Asia/Tashkent')


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.async_engine = create_async_engine(
        settings.DATABASE_URL_asyncpg,
        pool_pre_ping=True,
        pool_size=20,
        pool_timeout=30
    )

    factory.async_session_factory = sessionmaker(
        db.async_engine,
        expire_on_commit=False,
        autoflush=True,
        class_=AsyncSession
    )

    yield

    await db.async_engine.dispose()
    db.sync_engine.dispose()
    factory.async_session_factory.close_all()
    factory.sync_session_factory.close_all()


app = FastAPI(
    debug=settings.DEBUG,
    description="""
    Admin Dashboard API
    """,
    version='1.0.0',
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/reduc',
    swagger_ui_parameters={
        "docExpansion": "none",
        "defaultModelsExpandDepth": -1, 
        "displayRequestDuration": True,
        "tryItOutEnabled": True,
    },
    swagger_ui_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-themes@3.0.0/themes/3.x/dark.css"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


# @app.middleware('http')
# async def before_request(request: Request, call_next):
#     user = request.headers.get('X-Forwarded-For')
#     key = f'{user}:{datetime.datetime.now().minute}'
#     result = await RequestLimit(limit=1000, duration=30).is_over_limit(user=user, key=key)
#     if result:
#         return ORJSONResponse(
#             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#             content={'detail': 'Too many requests'}
#         )
#     return await call_next(request)


@app.get('/now/datetime',)
async def datatime():
    return datetime.datetime.now(tz=toshkent_tz)


for router, prefix, tags in routers_prefixs_tags():
    app.include_router(
        router=router,
        prefix=prefix,
        tags=tags
    )