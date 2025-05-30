from fastapi import HTTPException, status, Request


async def get_token_from_cookies(request: Request) -> str:
    token = request.cookies.get('Authorization')
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Token is missing'
        )
    return token