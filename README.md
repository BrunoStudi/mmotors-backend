# M-Motors — Backend API

Backend de l’application **M-Motors**, développé avec **Python FastAPI**.

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

depuis le terminal de votre IDE tapez les commandes suivantes:

git clone https://github.com/BrunoStudi/mmotors-backend.git
cd mmotors-backend

---

## 3. Créer et activer l’environnement virtuel

Sur Windows:

Entrez ces commandes dans le terminal:

python -m venv venv
venv\Scripts\activate

Sur Linux / Mac:

python3 -m venv venv
source venv/bin/activate

---

## 4. Installer les dépendances

Entrez cette commande dans le terminal:

pip install -r requirements.txt

---

## 5. Configuration des variables d’environnement

Créer un fichier .env à la racine du projet et y mettre le contenu suivant:

DATABASE_URL=postgresql://postgres:motdepasse@localhost:5432/mmotors
SECRET_KEY=change_me_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Adapter les valeurs selon votre configuration PostgreSQL locale.

Exemple :

DATABASE_URL=postgresql://postgres:admin@localhost:5432/mmotors

---

## 6. Création des bases de données

Créer deux bases PostgreSQL :

une base pour le développement local ;
une base dédiée aux tests.

Exemple dans PostgreSQL:

CREATE DATABASE mmotors;
CREATE DATABASE mmotors_test;

(Vous pouvez aussi utiliser pgAdmin4 et utiliser Querrytools 
pour entrez les commandes et appuyer sur le "play vert" pour valider les commandes)

La base mmotors est utilisée pour l’application locale.
La base mmotors_test est utilisée uniquement pour les tests automatisés.

---

## 7. Création des tables

Le projet utilise SQLAlchemy pour la définition des modèles.

Pour créer les tables en local, lancer Python depuis la racine du projet :
Dans le terminal entrez cette commande:

python

Puis un fois dans l'interface python exécuter ce code :

from app.database import Base, engine
Base.metadata.create_all(bind=engine)
exit()

Les tables suivantes sont créées :

- users
- vehicles
- vehicle_images
- dossiers
- documents

---

## 8. Jeu de données local

Pour tester l’application, il est possible de créer un compte administrateur depuis un shell Python.
Entrez cette commande dans le terminal:

python

Puis une fois dans l'interface python executez ce code :

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

Compte administrateur local :

Email : admin@mmotors.fr
Mot de passe : Admin1234

Un compte client peut être créé directement depuis l’interface front-end ou via Swagger.

---

## 9. Lancer le backend en local

depuis votre terminal de l'ide ou autre entrez cette commande :

uvicorn main:app --reload

L’API est disponible sur :

http://127.0.0.1:8000

La documentation Swagger est disponible sur :

http://127.0.0.1:8000/docs

---

## 10. Endpoints principaux

Authentification:

POST /auth/register
POST /auth/login

Véhicules:

GET    /vehicles/
GET    /vehicles/{vehicle_id}
POST   /vehicles/
PUT    /vehicles/{vehicle_id}
DELETE /vehicles/{vehicle_id}
POST   /vehicles/{vehicle_id}/images
DELETE /vehicles/images/{image_id}

Dossiers:

POST /dossiers/
GET  /dossiers/me
GET  /dossiers/
PUT  /dossiers/{dossier_id}

Documents:

POST /documents/{dossier_id}/documents
GET  /documents/{dossier_id}

---

## 11. Lancement des tests

Les tests automatisés sont réalisés avec Pytest.
Depuis votre terminal entrez cette commande :

pytest

Pour afficher la couverture de test entrez cette commande :

pytest --cov=app

La couverture obtenue sur le projet est supérieure à 80 %, conformément à l’objectif demandé.

Les tests couvrent notamment :

l’authentification ;
la sécurité des mots de passe ;
la gestion des véhicules ;
la création et le suivi des dossiers ;
l’upload et la consultation des documents ;
les contrôles d’accès selon les rôles.

---

## 12. Base de données de test

Les tests ne doivent pas dépendre d’identifiants fixes existants en base.

Une base dédiée mmotors_test est prévue pour les tests automatisés.

Les tests doivent créer leurs propres données avant exécution :

utilisateur client ;
utilisateur administrateur ;
véhicule ;
dossier ;
document.

Cette approche évite les tests fragiles basés sur des IDs codés en dur.

---

## 13. Sécurité

Plusieurs mesures de sécurité sont mises en place :

hachage des mots de passe avec bcrypt ;
authentification par JWT ;
routes protégées par dépendances FastAPI ;
contrôle d’accès par rôle ;
séparation des droits client / administrateur ;
contrôle d’accès aux dossiers et documents ;
configuration CORS limitée aux origines autorisées.

En production, seules les URLs nécessaires sont autorisées dans la configuration CORS.

---

## 14. Gestion des fichiers

Les images des véhicules et les documents des dossiers sont stockés dans le dossier :

uploads/

En environnement local, ce stockage permet de tester simplement la fonctionnalité de dépôt de fichiers.

Limite connue :

Sur Heroku, le système de fichiers est éphémère (donc les images et/ou dossiers peuvent ne plus exister apres 24h
il faut alors reuploader les images ou documents en editant la donnée ou en creant une nouvelle).

Pour une version de production complète, un stockage externe serait recommandé :

Amazon S3 ;
Cloudinary ;
Supabase Storage ;
autre service équivalent.

---

## 15. Déploiement

Le backend est prévu pour être déployé sur Heroku.

Fichiers nécessaires :

Procfile
requirements.txt

Contenu du Procfile :

web: gunicorn main:app -k uvicorn.workers.UvicornWorker

Heroku utilise la variable d’environnement DATABASE_URL pour se connecter à PostgreSQL.

---

## 16. Commandes utiles Heroku

Afficher les logs entrez ces differentes commandes dans votre terminal :

heroku logs --tail -a nom-application-heroku

Ouvrir un shell distant :

heroku run bash -a nom-application-heroku

Créer les tables sur Heroku :

heroku run python -a nom-application-heroku

Puis une fois dans l'interface python :

from app.database import Base, engine
Base.metadata.create_all(bind=engine)
exit()

---

## 17. Structure du projet

mmotors-backend/
│
├── app/
│   ├── core/
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── vehicle.py
│   │   ├── vehicle_image.py
│   │   ├── dossier.py
│   │   └── document.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── vehicle.py
│   │   ├── dossier.py
│   │   └── document.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── vehicle.py
│   │   └── dossier.py
│   │
│   ├── database.py
│   └── dependencies.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_vehicles.py
│   ├── test_dossiers.py
│   ├── test_documents.py
│   ├── test_security.py
│   └── test_full_flow.py
│
├── uploads/
├── main.py
├── requirements.txt
├── Procfile
├── .env
└── README.md

---

## 18. Fonctionnalités principales

Le backend permet :

l’inscription et la connexion des utilisateurs ;
la sécurisation des routes par JWT ;
la gestion des rôles client et administrateur ;
la création, modification et suppression des véhicules ;
l’ajout et la suppression d’images de véhicules ;
le dépôt de dossiers client ;
le suivi du statut des dossiers ;
la validation ou le refus des dossiers par l’administrateur ;
l’upload et la consultation de documents liés aux dossiers.

---

## 19. Auteur

Projet réalisé dans le cadre de la formation CDA / Bachelor Développeur d’Application.

Auteur : Bruno