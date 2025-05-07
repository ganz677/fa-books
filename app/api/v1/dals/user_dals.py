from typing import TYPE_CHECKING

from fastapi import HTTPException, status, Form, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.models import User
from auth import utils as auth_utils


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


http_bearer = HTTPBearer()


        
            
