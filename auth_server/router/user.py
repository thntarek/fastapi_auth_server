from fastapi import APIRouter

from auth_server.schemas import UserResponse
from auth_server.security import current_user_dependency

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/home", response_model=UserResponse)
async def get_user_home(current_user: current_user_dependency):
    return current_user
