from fastapi import Cookie, HTTPException

from app.auth_utils import verify_token


def get_current_user(
    access_token: str = Cookie(None)
):

    if access_token is None:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    payload = verify_token(access_token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload
