import pickle
from instagrapi import Client
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from instagrapi.exceptions import (
    UserNotFound,
    BadCredentials,
    TwoFactorRequired,
    ChallengeRequired,
    PleaseWaitFewMinutes,
    ReloginAttemptExceeded
)

from src.database.base import get_async_session
from src.database.orm.login import LoginToInstagramRepository, get_login_repo


client_store = {}


def manual_input_code(self, challenge):
    raise Exception("CODE_REQUIRED")


class LoginToInstagramService:
    def __init__(self, storage) -> None:
        self.storage = storage

    async def login(self, username: str, password: str, code: str | None = None) -> str:
        try:
            if code:
                if username not in client_store:
                    raise HTTPException(status_code=400, detail="No challenge in progress for this user.")
                
                cl = client_store[username]
                cl.challenge_code_handler = lambda self, challenge: code
                await self.storage.create_account(username=username, password=password)
                await self.storage.create_session(username=username, session_data=pickle.dumps(cl.get_settings()))
                del client_store[username]
                raise HTTPException(status_code=200, detail="Code verified and login completed.")

            cl = Client()
            cl.challenge_code_handler = manual_input_code
            cl.login(username=username, password=password)

            await self.storage.create_account(username=username, password=password)
            await self.storage.create_session(username=username, session_data=pickle.dumps(cl.get_settings()))
            raise HTTPException(status_code=200, detail="Login successful.")

        except HTTPException as http_exc:
            raise http_exc

        except ChallengeRequired:
            client_store[username] = cl
            raise HTTPException(
                status_code=403,
                detail="Code required. Please POST it to this endpoint with 'code'."
            )
        except Exception as e:
            if "CODE_REQUIRED" in str(e):
                client_store[username] = cl
                raise HTTPException(status_code=403, detail="Code required. Please POST it to this endpoint with 'code'.111111111111")
            
            elif isinstance(e, BadCredentials):
                raise HTTPException(status_code=401, detail="Incorrect login or password.")
            
            elif isinstance(e, UserNotFound):
                raise HTTPException(status_code=404, detail="User not found.")
            
            elif isinstance(e, TwoFactorRequired):
                raise HTTPException(status_code=403, detail="Two-factor authentication required.")
            
            elif isinstance(e, PleaseWaitFewMinutes):
                raise HTTPException(status_code=429, detail="Too many login attempts. Please wait.")
            
            elif isinstance(e, ReloginAttemptExceeded):
                raise HTTPException(status_code=429, detail="Relogin attempts exceeded.")
            
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        

    async def refresh_session(self):
        pass


def get_login_service(
    storage: LoginToInstagramRepository = Depends(get_login_repo)
) -> LoginToInstagramService:
    return LoginToInstagramService(storage=storage)