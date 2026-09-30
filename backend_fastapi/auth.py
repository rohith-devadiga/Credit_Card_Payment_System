import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Must match Django's SIMPLE_JWT SIGNING_KEY / ALGORITHM so tokens issued
# by the Django auth service are also valid here.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-change-me")
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing user_id claim")
    return user_id
