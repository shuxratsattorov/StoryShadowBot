import pickle
from instagrapi import Client
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from instagrapi.exceptions import (
    UserNotFound,
    LoginRequired,
    BadCredentials,
    TwoFactorRequired,
    ChallengeRequired,
    PleaseWaitFewMinutes,
    ReloginAttemptExceeded
)

from src.database.base import get_async_session
from src.database.orm.login import LoginToInstagramRepository, get_login_repo


# async def generate_device_profile():



# async def login_to_instagram(username: str, password: str) -> str:
#     cl.set_locale('en_US')

#     session = await get_session_data(username)

#     try:
#         if session:
#             session_dict = pickle.loads(session)
#             cl.load_settings(pickle.loads(session_dict))
#             cl.init()
#             cl.account_info()
#             return "✅ Sessiya orqali muvaffaqiyatli login qilindi."

#         cl.login(username, password)
#         await create_or_update_session(username, session_data=pickle.dumps(cl.get_settings()))
#         return "✅ Yangi login qilindi va sessiya saqlandi."

#     except LoginRequired:
#         cl.login(username, password)
#         await create_or_update_session(username, session_data=pickle.dumps(cl.get_settings()))
#         return "✅ Sessiya yaroqsiz edi, qayta login qilindi va yangilandi."

#     except Exception as e:
#         return f"❌ Umumiy xatolik: {e}"



# async def login_to_instagram1(username: str, password: str) -> str:
#     logger.info(f"🔍 {username} uchun sessiya tekshirilmoqda...")
#     cl.set_locale('en_US')

#     session_data = await get_session_data(username)

#     try:
#         if session_data:
#             settings_dict = pickle.loads(session_data)
#             cl.set_settings(settings_dict)

#             try:
#                 cl.account_info()
#             except LoginRequired:

#         cl.login(username, password)

#         session_bytes = pickle.dumps(cl.get_settings())

#         await create_or_update_session(username, session_bytes)

#     except Exception as e:
#         return f"❌ Umumiy xatolik: {e}"




# SESSION_FILE = "src/sessions/session2.json"


# def login_to_instagram(username, password):
#     try:
#         if not os.path.exists(SESSION_FILE):
#             cl.set_locale('en_US')
#             cl.login(username, password)
#             cl.dump_settings(SESSION_FILE)
#             return f"✅ Instagram login orqali muvaffaqiyatli ulandi va sessiya saqlandi!"
#         else:
#             try:
#                 cl.set_locale('en_US')
#                 cl.load_settings(SESSION_FILE)
#                 cl.login(username, password)
#                 cl.user_info_by_username(username)
#                 return f"✅ Instagram muvaffaqiyatli ulandi!"
#             except LoginRequired:
#                 os.remove(SESSION_FILE)
#                 cl.set_locale('en_US')
#                 cl.login(username, password)
#                 cl.dump_settings(SESSION_FILE)
#                 return "✅ Sessiya eskirgani sababli, o'chirilib qayta yaratildi."
#             except Exception as e:
#                 return f"❌ Umumiy xatolik: {e}"
#     except Exception as e:
#         return f"❌ Umumiy xatolik: {e}"
    

SESSION_FILE = "src/sessions/session2.json"

def generate_device_settings():
    return {
        "app_version": "269.0.0.18.68",
        "android_version": 28,
        "android_release": "9.0",
        "dpi": "480dpi",
        "resolution": "1080x1920",
        "manufacturer": "Samsung",
        "device": "heroqlte",
        "model": "SM-G930F",
        "cpu": "samsungexynos8890",
        "version_code": "314665256"
    }

def generate_user_agent(device_settings):
    return (
        f"Instagram {device_settings['app_version']} Android "
        f"({device_settings['android_version']}/{device_settings['android_release']}; "
        f"{device_settings['dpi']}; {device_settings['resolution']}; "
        f"{device_settings['manufacturer']}; {device_settings['model']}; "
        f"{device_settings['device']}; {device_settings['cpu']}; en_US; "
        f"{device_settings['version_code']})"
    )

def generate_uuids():
    return {
        "phone_id": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "client_session_id": str(uuid.uuid4()),
        "advertising_id": str(uuid.uuid4()),
        "device_id": f"android-{uuid.uuid4().hex[:16]}"
    }

def login_to_instagram(username, password):
    cl = Client()
    cl.set_locale('en_US')

    # Simulyatsiyalangan qurilma
    device_settings = generate_device_settings()
    user_agent = generate_user_agent(device_settings)
    uuids = generate_uuids()

    # Qurilma parametrlari ulab beriladi
    cl.device_settings = device_settings
    cl.user_agent = user_agent
    cl.uuid = uuids["uuid"]
    cl.phone_id = uuids["phone_id"]
    cl.advertising_id = uuids["advertising_id"]
    cl.client_session_id = uuids["client_session_id"]
    cl.device_id = uuids["device_id"]

    try:
        if not os.path.exists(SESSION_FILE):
            cl.login(username, password)
            cl.dump_settings(SESSION_FILE)
            return "✅ Simulyatsiya orqali login qilingan va sessiya saqlandi!"
        else:
            try:
                cl.load_settings(SESSION_FILE)
                cl.login(username, password)
                cl.user_info_by_username(username)
                return "✅ Sessiya mavjud edi, undan foydalangan holda muvaffaqiyatli login qilindi!"
            except LoginRequired:
                os.remove(SESSION_FILE)
                cl.login(username, password)
                cl.dump_settings(SESSION_FILE)
                return "♻️ Sessiya muddati o‘tgan, yangilandi va qaytadan login qilindi!"
            except Exception as e:
                return f"❌ Login xatosi (sessiya mavjud): {e}"
    except Exception as e:
        return f"❌ Login xatosi (yangi sessiya): {e}"
    

class LoginToInstagramService:
    def __init__(self, session: AsyncSession) -> None:
        self.cl = Client()
        self.repo = LoginToInstagramRepository(session=session)

    async def create_session(self, username: str, password: str) -> str:
        try:
            self.cl.login(username=username, password=password)
            self.repo.create_account(username=username, password=password)
            self.repo.create_session(account_id=username, session_data=pickle.dumps(self.cl.get_settings()))
            raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Login successful."
            )
        
        except BadCredentials:
            raise HTTPException(status_code=401, detail="Incorrect login or password.")
        
        except UserNotFound:
            raise HTTPException(status_code=404, detail="User not found.")
        
        except ChallengeRequired:
            raise HTTPException(status_code=403, detail="Challenge required. Please verify your identity.")
        
        except TwoFactorRequired:
            raise HTTPException(status_code=403, detail="Two-factor authentication required.")
        
        except PleaseWaitFewMinutes:
            raise HTTPException(status_code=429, detail="Too many login attempts. Please wait.")
        
        except ReloginAttemptExceeded:
            raise HTTPException(status_code=429, detail="The number of login attempts is limited. Please wait.")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")   
        

    async def refresh_session(self):
        pass


@lru_cache()
def get_login_service(
    session: AsyncSession = Depends(get_async_session),
    storage: LoginToInstagramRepository = Depends(get_login_repo)
) -> LoginToInstagramService:
    return LoginToInstagramService(session=session, storage=storage)