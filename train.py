"""
Prediction de la survie d'un individu sur le Titanic
"""

import argparse
import pathlib
import pandas as pd
from joblib import dump

from sklearn.model_selection import GridSearchCV


from src.data.import_data import import_yaml_config
from src.pipeline.build_pipeline import split_train_test, create_pipeline
from src.models.train_evaluate import evaluate_model
from src.features.build_features import feature_engineering
import src.models.log as mlog


parser = argparse.ArgumentParser(description="Paramètres du random forest")
parser.add_argument("--n_trees", type=int, default=20, help="Nombre d'arbres")
parser.add_argument("--appli", type=str, default="appli22", help="Application number")
parser.add_argument("--experiment_name", type=str, default="titanicml", help="Name of experiment")

args = parser.parse_args()

n_trees = args.n_trees

URL_RAW = "https://minio.lab.sspcloud.fr/mthomassin/ensae-reproductibilite/data/raw/data.csv"
config = import_yaml_config("configuration/config.yaml")
print("-----------------------------------")
print("URL_RAW=" + URL_RAW)
data_path = config.get("data_path", URL_RAW)
print("-----------------------------------")
print("data_path=" + data_path)
data_train_path = config.get("train_path", "data/derived/train.csv")
data_test_path = config.get("test_path", "data/derived/test.csv")

MAX_DEPTH = None
MAX_FEATURES = "sqrt"


print("# IMPORT ET STRUCTURATION DONNEES --------------------------------")

p = pathlib.Path("data/derived/")
p.mkdir(parents=True, exist_ok=True)

titanic_raw = pd.read_csv(data_path)

# Create a 'Title' variable
TrainingData = feature_engineering(titanic_raw)

X_train, X_test, y_train, y_test = split_train_test(
    TrainingData, test_size=0.1,
    train_path=data_train_path,
    test_path=data_test_path
)


print("# PIPELINE ----------------------------")


print("# Create the pipeline")
pipe = create_pipeline(
    n_trees, max_depth=MAX_DEPTH, max_features=MAX_FEATURES
)


param_grid = {
    "classifier__n_estimators": [10, 20, 50],
    "classifier__max_leaf_nodes": [5, 10, 50],
}


pipe_cross_validation = GridSearchCV(
    pipe,
    param_grid=param_grid,
    scoring=["accuracy", "precision", "recall", "f1"],
    refit="f1",
    cv=5,
    n_jobs=5,
    verbose=1,
)


print("# ESTIMATION ET EVALUATION ----------------------")
pipe_cross_validation.fit(X_train, y_train)
pipe = pipe_cross_validation.best_estimator_


mlog.log_gsvc_to_mlflow(pipe_cross_validation, EXPERIMENT_NAME, APPLI_ID)

dump(pipe, 'api/model.joblib')

print("# Evaluate the model")
score, matrix = evaluate_model(pipe, X_test, y_test)
print(f"{score:.1%} de bonnes réponses sur les données de test pour validation")
print(20 * "-")
print("matrice de confusion")
print(matrix)
