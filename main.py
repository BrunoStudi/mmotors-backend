from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.models import user
from app.routes.auth import router as auth_router
from app.routes.vehicle import router as vehicle_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes import dossier

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="M-Motors API",
    description="API backend pour la plateforme M-Motors",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_router)
app.include_router(vehicle_router)
app.include_router(dossier.router)


@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle"}