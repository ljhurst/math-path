import os

DATABRICKS_PAT_ENV_VAR = "DATABRICKS_TOKEN"


def get_pat() -> str:
    pat = os.getenv(DATABRICKS_PAT_ENV_VAR)

    if not pat:
        raise ValueError(
            f"Please set {DATABRICKS_PAT_ENV_VAR} with your Databricks Personal Access Token."
        )

    return pat
