import mlflow
import os
MLFLOW_PORT = os.getenv("MLFLOW_PORT")
def get_mlflow():
    mlflow.set_tracking_uri(f"http://mlflow:{MLFLOW_PORT}")  # Set the MLflow tracking URI
    return mlflow