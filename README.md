# mlflow-serve-stack
# Summary
  mlflow-serve-stack is an all-in-one, production-ready MLOps stack designed for fast local development and robust model tracking.
With this project, you can track experiments, train and register models, manage data, and inspect your metadata—all with a few Docker commands.
- MLflow: Experiment tracking, model registry, and artifact management
- FastAPI: Provides a modern, secure REST API to drive model training, dataset selection, and user management
- PostgreSQL: Robust database backend for metadata and user info
- MinIO: S3-compatible object storage for large artifacts, logs, and models
- pgAdmin: Easy GUI for PostgreSQL database management
- Docker Compose: Orchestrates all services for seamless setup

## This stack is ideal for:
- Data scientists and ML engineers who want an end-to-end, reproducible workflow
- Teams looking for a local or on-prem MLOps foundation before moving to the cloud
- Rapid prototyping, internal hackathons, and hands-on learning of real-world MLOps best practices

Just clone, configure .env, and spin up your entire ML platform.
## Services Overview

| Service   | URL                              | Default User/Pass    | Description            |
|-----------|----------------------------------|----------------------|------------------------|
| FastAPI   | http://localhost:8000/docs       | -                    | REST API / Swagger UI  |
| MLflow    | http://localhost:5050            | -                    | ML tracking/registry   |
| MinIO     | http://localhost:9001/login      | minioadmin/minioadmin| S3-like artifact store |
| pgAdmin   | http://localhost:8080            | admin@pgadmin.com/...| DB Management GUI      |
| Postgres  | db:5432 (internal container)     | postgresuser/...     | Metadata DB            |

## Features
  - Model Training & Tracking with MLflow
  - REST API for dataset selection, training, model registration (FastAPI)
  - S3-Compatible Storage for artifacts (MinIO)
  - PostgreSQL as metadata store
  - pgAdmin for easy DB management
  - Multi-service orchestration with Docker Compose
  - Quick local setup with .env configuration
## Quickstart
  1. Clone the Repository
  ```bash
  git clone <your-repo-url>
  cd mlflow-serve-stack
  ```
  2. Prepare Environment Variables
  ```bash
  cp .env.example .env
  ```
    Edit .env and set your secrets/passwords as desired.
    ## postgresql
    POSTGRES_PORT=5432
    POSTGRES_USER=postgresuser ## ostgres user for database
    POSTGRES_PASSWORD=postgrespassword ## db user password
    POSTGRES_DB=mlflow_db ## initial db name
    ## pgadmin ##
    PGADMIN_DEFAULT_EMAIL=admin@pgadmin.com ## default email for pgadmin
    PGADMIN_DEFAULT_PASSWORD=pgadminpassword ## efault password for pgadmin
    PGADMIN_PORT=8080
    ## fastapi ##
    SECRET_KEY=secretkey1234567890 ## secret for password hashing
    API_PORT=8000
    DATABASE_URL=postgresql://postgresuser:postgrespassword@db:5432/mlflow_db ## database url endpoint for connection from api to db
    ## mlflow ##
    # MLFLOW_TRACKING_URI=postgresql://mlflow:mlflow123@db:5432/mlflow_db ## database url endpoint for connection from mlflow to db
    MLFLOW_ARTIFACT_ROOT=s3://mlflow/ ## artifact bucket location
    AWS_ACCESS_KEY_ID=minioadmin ## minio root user
    AWS_SECRET_ACCESS_KEY=minioadmin ## minio root password
    MLFLOW_S3_ENDPOINT_URL=http://minio:9000
    AWS_REGION=us-east-1
    MLFLOW_PORT=5050
    ## minio ##
    MINIO_ROOT_USER=minioadmin ## minio root user
    MINIO_ROOT_PASSWORD=minioadmin ## minio root password
  3. Start All Services
  ```bash
  docker compose up -d --build
  ```
  check services from command
  ```bash
  docker ps
  ```
  <img width="1192" alt="image" src="https://github.com/user-attachments/assets/fe10bf69-0854-4dd5-8fa3-1620c423ed37" />
  or check via docker desktop
  <img width="1496" alt="image" src="https://github.com/user-attachments/assets/402740a9-555a-467d-b1b9-3ec7c73d92f5" />
  4. Register PostgreSQL Server in pgAdmin
    on brower open pgadmin link 
    http://localhost:{PGADMIN_PORT} for example http://localhost:8080 
    email, password is from .env file PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD 

<img width="1509" alt="image" src="https://github.com/user-attachments/assets/99df609c-007e-4397-ac27-c4ae9cc66b99" />

    click "Add New Server" and set connection name
    
<img width="1500" alt="image" src="https://github.com/user-attachments/assets/2432f2a6-446c-4381-94e0-106c5f28c2c1" />

    set conection postgres username/password then save
    
<img width="1494" alt="image" src="https://github.com/user-attachments/assets/e453fcc8-866f-4f14-b77b-8eea58b279b6" />

  5. Create mlflow bucket for artifact saving location
    on brower open minio link 
    for example http://localhost:9001/login
    email, password is from .env file MINIO_ROOT_USER and MINIO_ROOT_PASSWORD
<img width="1490" alt="image" src="https://github.com/user-attachments/assets/76789081-ec4e-4cf7-b839-2543f6b1be82" />

    create bocket named 'mlflow' same as config in .env MLFLOW_ARTIFACT_ROOT=s3://mlflow/
    
<img width="1505" alt="image" src="https://github.com/user-attachments/assets/b201fa32-1706-4701-8b48-c492bb096439" />
<img width="1494" alt="image" src="https://github.com/user-attachments/assets/167aced4-91ca-4928-a6ce-ddf4c74b584a" />
  6. Register user using FastAPI Swagger
    Swagger Link : http://localhost:8000/docs#/default
<img width="1491" alt="image" src="https://github.com/user-attachments/assets/698a6a64-aac1-4441-b2b1-5c3a9f2c313f" />
<img width="1494" alt="image" src="https://github.com/user-attachments/assets/dd5ca761-88ea-4546-8be2-7beb881a8bc1" />
    
    By default new registered user cant use protected route to secure API Route
    
<img width="1403" alt="image" src="https://github.com/user-attachments/assets/26cc1e03-f9b7-48e9-a15c-f32d2abadb4c" />

    You have to activate user from database using pgadmin
    On the left top connection open mlflow db
    
<img width="1507" alt="image" src="https://github.com/user-attachments/assets/ecf0932c-dd23-4cb7-bb24-829cc1d29bcb" />

    open query tool

<img width="1497" alt="image" src="https://github.com/user-attachments/assets/58a78756-5278-4687-ac10-2ef0b4ad2dfe" />

    execute query to update is_sctive registered user to true
    SQL : update users set is_active = true where username = 'admin';

<img width="1507" alt="image" src="https://github.com/user-attachments/assets/392604db-c051-4be3-b241-81bfd5b37b06" />

    click authorize on the top right
    
<img width="1462" alt="image" src="https://github.com/user-attachments/assets/adbb3a48-348e-4aa4-bba3-44d79d20a165" />
<img width="1488" alt="image" src="https://github.com/user-attachments/assets/16f03479-8249-43fa-81d5-0f2e87fae55c" />
<img width="1491" alt="image" src="https://github.com/user-attachments/assets/2807cec8-02aa-4483-ba83-311231f090d5" />


# Usage
- Use FastAPI for API calls: dataset selection, model training, etc. 
- MLflow UI for tracking experiments & registered models.
- MinIO UI for browsing model artifacts.
- pgAdmin for database inspection.

# FastAPI Services Overview

| Method | Route                 | Description                                  | Auth Required |
|--------|----------------------|----------------------------------------------|---------------|
| POST   | /auth/register        | Register a new user                          | ❌            |
| POST   | /auth/token           | Login & get JWT token                        | ❌            |
| GET    | /auth/users/me        | Get current user profile                     | ✅            |
| POST   | train/train_request        | Create a new train request (choose dataset)  | ✅            |
| POST   | train/run                  | Trigger training for existing request        | ✅            |

# Example
  1. create request training data from POST train/train_request
     <img width="1487" alt="image" src="https://github.com/user-attachments/assets/440a49d0-bdf7-478d-ab50-681d723873d1" />
     <img width="1445" alt="image" src="https://github.com/user-attachments/assets/d9fd5504-1ab2-420d-be08-3cfb67424e6e" />

  2. run created request from POST train/run
     <img width="1481" alt="image" src="https://github.com/user-attachments/assets/aca06df1-f76f-4a8d-99bd-41b1eaf64d6a" />
     <img width="1482" alt="image" src="https://github.com/user-attachments/assets/0348bbd8-781d-4884-99f2-3a2c8ec26e97" />
  
  3. Check result on mlflow gui via : http://localhost:5050/

     <img width="1499" alt="image" src="https://github.com/user-attachments/assets/0bdec991-d04d-486f-8988-e55c62ee64a1" />
     <img width="1500" alt="image" src="https://github.com/user-attachments/assets/40f19eab-6419-4958-9970-c5f2a45e3e8f" />
     <img width="1503" alt="image" src="https://github.com/user-attachments/assets/c4eb4008-99f1-401b-a755-09a8646517f3" />
# References
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MinIO Documentation](https://min.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation
](https://www.pgadmin.org/docs/)
# Contributors

- Apisit 
  - [GitHub](https://github.com/Tale98)
  - [LinkedIn](https://www.linkedin.com/in/apisit-chiamkhunthod-2a11221b4/)
  - Email: oh.oh.159852357@gmail.com

Feel free to reach out if you have any questions or want to collaborate!
