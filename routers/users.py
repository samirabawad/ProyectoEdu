from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
from schema.userSchema import Token, TokenData
from fastapi.encoders import jsonable_encoder

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from schema import userSchema
from model import usersModel
import crud
from database import SessionLocal
from starlette.exceptions import HTTPException as StarletteHTTPException
from dependencies import get_token_header, get_query_token


router= APIRouter(
    tags=["users"],
    dependencies=[Depends(get_query_token)]
)

#token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# #obtiene usuario actual decodificando token
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# #verifica si el usuario actual esta activo
# async def get_current_active_user(
#     current_user: Annotated[UserIn, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# #obtiene usuario actual
# @router1.get("/users/me/", response_model=UserB)
# async def read_users_me(
#     current_user: Annotated[UserB, Depends(get_current_active_user)]
# ):
#     return current_user

# #obtiene items del usuario actual para sacar la password
# @router1.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[UserB, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]


# ###
# ###hash de password 
# ###
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # autentifica usuario
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def authenticate_user(fake_users_db, username: str, password: str):
#     user = get_user(fake_users_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# #crea token de acceso
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# genera el token
# @router1.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> Token:
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password) #se autentifica usuario
#     print(user)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     print(access_token_expires)
#     access_token = create_access_token( #se crea token de acceso
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     print(access_token)
#     return Token(access_token=access_token, token_type="bearer")