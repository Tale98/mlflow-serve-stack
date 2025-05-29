import mlflow.pyfunc
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from db.base import engine
from sqlmodel import SQLModel
## router ##
from routes.auth.router import router as auth_router
from routes.train.router import router as train_router
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Cleanup if needed
    # For example, close database connections or clean up resources
app = FastAPI(lifespan=lifespan)
# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(train_router, prefix="/train", tags=["Training Models"])

@app.exception_handler(Exception)
def all_exception_handler(request: Request, exc: Exception):
    # log error to console or monitoring service
    print(f"[ERROR] Unhandled Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )
@app.get("/")
def root():
    return {"message": "Welcome to the MLflow model serving API!"}