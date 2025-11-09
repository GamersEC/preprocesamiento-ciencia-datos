from typing import Optional, List, Union

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


def load_csv(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


def build_preprocessing_pipeline(
    numeric_features: List[str],
    categorical_features: List[str],
    categorical_strategy: str = "onehot",
    numeric_impute_strategy: str = "median",
    categorical_impute_strategy: str = "most_frequent",
    scale_numeric: bool = True,
) -> ColumnTransformer:
    # Pipeline numérico
    num_steps = []
    if numeric_impute_strategy:
        num_steps.append(("imputer", SimpleImputer(strategy=numeric_impute_strategy)))
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))

    numeric_pipeline = Pipeline(steps=num_steps) if num_steps else None

    # Pipeline categórico
    cat_steps = []
    if categorical_impute_strategy:
        cat_steps.append(("imputer", SimpleImputer(strategy=categorical_impute_strategy)))
    if categorical_strategy == "onehot":
        cat_steps.append(("encoder", OneHotEncoder(handle_unknown="ignore", sparse=False)))
    else:
        cat_steps.append(("encoder", OrdinalEncoder()))

    categorical_pipeline = Pipeline(steps=cat_steps)

    transformers = []
    if numeric_pipeline is not None and numeric_features:
        transformers.append(("num", numeric_pipeline, numeric_features))
    if categorical_features:
        transformers.append(("cat", categorical_pipeline, categorical_features))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    return preprocessor


def preprocess_dataframe(
    df: pd.DataFrame,
    target_column: Optional[str] = None,
    numeric_features: Optional[List[str]] = None,
    categorical_features: Optional[List[str]] = None,
    categorical_strategy: str = "onehot",
    numeric_impute_strategy: str = "median",
    categorical_impute_strategy: str = "most_frequent",
    scale_numeric: bool = True,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    df_copy = df.copy()

    if target_column is not None:
        if target_column not in df_copy.columns:
            raise ValueError(f"target_column '{target_column}' no existe en el DataFrame")
        y = df_copy[target_column]
        X = df_copy.drop(columns=[target_column])
    else:
        y = None
        X = df_copy

    # Inferir features si no se pasan
    if numeric_features is None:
        numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
    if categorical_features is None:
        categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

    preprocessor = build_preprocessing_pipeline(
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        categorical_strategy=categorical_strategy,
        numeric_impute_strategy=numeric_impute_strategy,
        categorical_impute_strategy=categorical_impute_strategy,
        scale_numeric=scale_numeric,
    )

    # Ajustar y transformar
    X_transformed = preprocessor.fit_transform(X)

    # Dividir
    if y is not None:
        X_train, X_test, y_train, y_test = train_test_split(
            X_transformed, y, test_size=test_size, random_state=random_state
        )
        return {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "preprocessor": preprocessor,
        }
    else:
        return {"X": X_transformed, "preprocessor": preprocessor}


if __name__ == "__main__":
    # Ejemplo de uso simple
    try:
        df = load_csv("data/sample.csv")
    except Exception:
        print("No se encontró data/sample.csv — este es solo un ejemplo de uso.")
    else:
        res = preprocess_dataframe(df)
        print("Preprocesamiento completado. Claves devueltas:", list(res.keys()))
