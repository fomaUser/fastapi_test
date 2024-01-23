from fastapi import APIRouter, Depends, HTTPException, Response

from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependecies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    """
    Register a new user.

    Args:
        user_data (SUserAuth): User authentication data.

    Returns:
        str: Success message if registration is completed successfully.

    Raises:
        HTTPException: If the user already exists.
    """
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email = user_data.email,password = hashed_password)
    return 'Registration completed successfully <3'

@router.post('login')
async def login_user(response:Response,user_data:SUserAuth):
    user = await authenticate_user(user_data.email,user_data.password)
    if not user:
        raise HTTPException(status_code=400,detail="Incorrect email or password")
    access_token = create_access_token({'sub':str(user.id)})
    response.set_cookie('You_have_access_token',access_token,httponly=True)
    return 'Login completed successfully <3'
