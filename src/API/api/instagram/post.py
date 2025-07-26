import logging
from fastapi import Depends

from src.API.api.instagram.router import router
from src.API.schemas.instagram import LoginRequest
from src.API.services.instagram import LoginToInstagramService, get_login_service


logging.basicConfig(level=logging.INFO)

@router.post("/login-to-instagram")
async def add_to_cart(
    data: LoginRequest, 
    # user: UserSchemaResponse = Depends(UserHandling().user),
    service: LoginToInstagramService = Depends(get_login_service)):

    result =  await service.login(
        username=data.username, 
        password=data.password,
        code=data.code
    )
    logging.info(result)
    return result