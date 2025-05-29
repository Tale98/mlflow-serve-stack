from fastapi import APIRouter, Depends, HTTPException
from dependencies.mlflow.mlflow import get_mlflow
from models.auth.user import User
from models.train.train_request import TrainRequestTable, TrainRequestStatus
from schemas.train.train_request import RequestTrain, RunTrain
from dependencies.auth.user import get_current_user

from sklearn.datasets import load_iris, load_wine, load_digits, load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

import matplotlib.pyplot as plt

from utils.folder.folder import TempFolder
from db.base import get_session
import os
router = APIRouter()

@router.post("/train_request")
def create_train_request(
    request: RequestTrain,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    train_request = TrainRequestTable(
        name=request.name,
        description=request.description,
        user_id=current_user.id,
        dataset_prototype=request.dataset_prototype,
        train_ratio=request.train_ratio
    )
    session.add(train_request)
    session.commit()
    session.refresh(train_request)
    
    return {"message": "Train request created successfully", "train_request_id": train_request.id}
@router.post("/run")
def run_train(
    request: RunTrain,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
    mlflow = Depends(get_mlflow)
):
    train_request = session.get(TrainRequestTable, request.id)
    if not train_request:
        return {"error": "Train request not found"}
    dict_dataset = {
        "iris": load_iris,
        "wine": load_wine,
    }
    mlflow.set_experiment(f"user_{current_user.id}_experiment")
    dataset_loader = dict_dataset.get(train_request.dataset_prototype)
    if not dataset_loader:
        return {"error": "Dataset prototype not supported"}
    train_request.status = TrainRequestStatus.IN_PROGRESS
    session.add(train_request)
    session.commit()
    session.refresh(train_request)
    X, y = dataset_loader(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_request.train_ratio)
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    with mlflow.start_run() as run:
        temp_folder = TempFolder(run.info.run_id)
        train_request.binded_run_uuid = run.info.run_id
        try:
            temp_folder.create()

            mlflow.log_param("n_estimators", 50)
            mlflow.log_param("dataset_prototype", train_request.dataset_prototype)
            mlflow.log_param("train_ratio", train_request.train_ratio)

            ## acc ##
            mlflow.log_metric("accuracy", acc)
            ## confusion matrix ##
            cm = confusion_matrix(y_test, model.predict(X_test))
            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title('Confusion Matrix')
            plt.colorbar()
            plt.xticks(ticks=range(len(model.classes_)), labels=model.classes_, rotation=45)
            plt.yticks(ticks=range(len(model.classes_)), labels=model.classes_)
            plt.xlabel('Predicted label')
            plt.ylabel('True label')
            plt.tight_layout()
            
            subfolder_path = temp_folder.create_subfolder('charts')
            plt.savefig(os.path.join(subfolder_path, "confusion_matrix.png"))
            plt.close()

            mlflow.sklearn.log_model(model, "model")
            
            # Register model
            model_name = f"user_{current_user.id}_model"
            model_uri = f"runs:/{run.info.run_id}/model"
            mlflow.register_model(model_uri=model_uri, name=model_name)
            
            ## log artifact ##
            subfolder_path = temp_folder.create_subfolder('datasets')
            X_train.to_csv(os.path.join(subfolder_path, "X_train.csv"), index=False)
            y_train.to_csv(os.path.join(subfolder_path, "y_train.csv"), index=False)
            X_test.to_csv(os.path.join(subfolder_path, "X_test.csv"), index=False)
            y_test.to_csv(os.path.join(subfolder_path, "y_test.csv"), index=False)

            mlflow.log_artifacts(temp_folder.path, artifact_path="data")
        except Exception as e:
            train_request.status = TrainRequestStatus.FAILED
            session.add(train_request)
            session.commit()
            session.refresh(train_request)
            raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")
        finally:
            temp_folder.delete()

    train_request.status = TrainRequestStatus.COMPLETED
    session.add(train_request)
    session.commit()
    session.refresh(train_request)
    return {"message": f"Training completed for request ID {request.id}"}