# M-Motors — Backend API

Backend de l’application **M-Motors**, développé avec **Python FastAPI**.

## Stack technique

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Pytest

---

## Documentation API

![Swagger](screenshots/swagger_docs.png)

---

## Couverture de tests

![Pytest](screenshots/test_cov.png)

---

L’API permet de gérer :

- l’authentification des utilisateurs ;
- les rôles client / administrateur ;
- le catalogue de véhicules ;
- les images des véhicules ;
- les dossiers clients d’achat ou de location ;
- le dépôt et la consultation des documents liés aux dossiers.

---

## 1. Prérequis

Avant de lancer le projet en local, installer :

- Python 3.14 ou version compatible ;
- PostgreSQL ;
- Git ;
- pip ;
- un terminal PowerShell ou équivalent.

---

## 2. Cloner le dépôt

Depuis le terminal de votre IDE tapez les commandes suivantes :

```bash
git clone https://github.com/BrunoStudi/mmotors-backend.git  
cd mmotors-backend
```

---

## 3. Créer et activer l’environnement virtuel

Sur Windows :

```bash
python -m venv venv  
venv\Scripts\activate  
```

Sur Linux / Mac :

```bash
python3 -m venv venv  
source venv/bin/activate  
```

---

## 4. Installer les dépendances

Depuis votre terminal :

```bash
pip install -r requirements.txt  
```

---

## 5. Configuration des variables d’environnement

Créer un fichier `.env` à la racine du projet et y mettre :

```bash
DATABASE_URL=postgresql://postgres:motdepasse@localhost:5432/mmotors  
SECRET_KEY=change_me_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=60  
```

Adapter selon votre configuration PostgreSQL avec le bon mot de passe.

---

## 6. Création des bases de données

Créer deux bases PostgreSQL :

```bash
CREATE DATABASE mmotors;  
CREATE DATABASE mmotors_test;  
```

(Vous pouvez aussi utiliser pgAdmin4 → Query Tool → la commande → bouton "play")

---

## 7. Création des tables

Dans le terminal :

```bash
python  
```

Puis dans Python :

```bash
from app.database import Base, engine  
Base.metadata.create_all(bind=engine)  
exit()  
```

---

## 8. Jeu de données local

Dans le terminal :

```bash
python  
```

Puis :

```bash
from app.database import SessionLocal  
from app.models.user import User  
from app.core.security import hash_password  

db = SessionLocal()  

admin = User(  
    email="admin@mmotors.fr",  
    password=hash_password("Admin1234"),  
    role="admin"  
)  

db.add(admin)  
db.commit()  
db.close()  

exit()  
```

Compte admin :

Email : admin@mmotors.fr  
Mot de passe : Admin1234  

---

## 9. Lancer le backend en local

```bash
uvicorn main:app --reload  
```

API :  
http://127.0.0.1:8000  

Swagger :  
http://127.0.0.1:8000/docs  

---

## 10. Endpoints principaux

Authentification :  
POST /auth/register  
POST /auth/login  

Véhicules :  
GET /vehicles/  
GET /vehicles/{vehicle_id}  
POST /vehicles/  
PUT /vehicles/{vehicle_id}  
DELETE /vehicles/{vehicle_id}  
POST /vehicles/{vehicle_id}/images  
DELETE /vehicles/images/{image_id}  

Dossiers :  
POST /dossiers/  
GET /dossiers/me  
GET /dossiers/  
PUT /dossiers/{dossier_id}  

Documents :  
POST /documents/{dossier_id}/documents  
GET /documents/{dossier_id}  

---

## 11. Lancement des tests

Créez une variable d'environnement **.env.test**
avec comme contenu :

```bash
DATABASE_URL=postgresql://postgres:motdepasse@localhost:5432/mmotors_test
SECRET_KEY=change_me_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=60 
```

Depuis votre terminal:

```bash
$env:ENV="test"; python -m pytest  
```

Couverture :

```bash
$env:ENV="test"; python -m pytest --cov=app 
```

---

## 12. Base de données de test

BDD dédiée :

**mmotors_test** 

Les tests doivent créer leurs propres données :

- utilisateur  
- véhicule  
- dossier  
- document  

Ne pas utiliser d’IDs en dur.

---

## 13. Sécurité

- bcrypt (hash mots de passe)  
- JWT  
- routes protégées  
- gestion des rôles  
- CORS sécurisé  

---

## 14. Gestion des fichiers

Dossier utilisé :

**uploads/**  

Sur Heroku :

filesystem éphémère (les fichiers peuvent disparaître)

Solutions recommandées :

- AWS S3  
- Cloudinary  
- Supabase Storage  

---

## 15. Déploiement

Fichier requis :

**Procfile**  

Contenu :

```bash
web: gunicorn main:app -k uvicorn.workers.UvicornWorker  
```

---

## 16. Commandes utiles Heroku

Logs :

```bash
heroku logs --tail -a nom-application-heroku  
```

Shell :

```bash
heroku run bash -a nom-application-heroku  
```

Créer les tables :

```bash
heroku run python -a nom-application-heroku  
```

Puis :

```bash
from app.database import Base, engine  
Base.metadata.create_all(bind=engine)  
exit()  
```

---

## 17. Structure du projet

```text
mmotors-backend/  
│  
├── app/  
│   ├── core/  
│   ├── models/  
│   ├── routes/  
│   ├── schemas/  
│   ├── database.py  
│   └── dependencies.py  
│  
├── tests/  
├── uploads/  
├── main.py 
├── .env
├── .env.test
├── requirements.txt  
├── Procfile  
└── README.md  
```

---

## 18. Fonctionnalités principales

- authentification  
- JWT  
- gestion des rôles  
- CRUD véhicules  
- gestion images  
- dossiers clients  
- documents  

---

## 19. Auteur

Projet réalisé dans le cadre de la formation CDA / Bachelor Développeur d’Application.

Auteur : Bruno