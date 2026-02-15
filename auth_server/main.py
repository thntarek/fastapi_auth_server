from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth_server.database.db_config import engine, close_db_engine, Base
from auth_server.router import auth, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown
    await close_db_engine()


app = FastAPI(
    title="auth_server API",
    description="Production-ready FastAPI application with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "auth_server API is running",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "ok"}
