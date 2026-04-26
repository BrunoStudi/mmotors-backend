from fastapi import FastAPI
from app.database import engine

app = FastAPI(
    title="M-Motors API",
    description="API backend pour la plateforme M-Motors",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "API M-Motors opérationnelle"}


@app.on_event("startup")
def test_db():
    try:
        with engine.connect():
            print("Connexion DB OK")
    except Exception as e:
        print("Erreur DB :", e)