from fastapi import FastAPI

from app.database import Base, engine
from app.models import user
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="M-Motors API",
    description="API backend pour la plateforme M-Motors",
    version="1.0.0"
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle"}