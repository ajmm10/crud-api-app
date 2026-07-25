import os

from fastapi import Header, HTTPException, status

API_KEY = os.environ.get("API_KEY", "dev-secret-key")


def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida o faltante",
        )
