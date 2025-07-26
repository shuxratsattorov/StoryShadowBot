import logging

from instagrapi import Client
# from instagrapi.device import Device
from instagrapi.exceptions import LoginRequired
import pickle
from instagrapi import Client
# from instagrapi.types import Device
from instagrapi.exceptions import LoginRequired
from src.database.orm.session import get_session_data, create_or_update_session


logger = logging.getLogger(__name__)
cl = Client()


async def login_to_instagram1(username: str, password: str) -> str:
    logger.info(f"🔍 {username} uchun sessiya tekshirilmoqda...")
    cl.set_locale('en_US')

    session_data = await get_session_data(username)

    try:
        if session_data:
            logger.info(f"📦 Sessiya mavjud, tiklanyapti...")
            settings_dict = pickle.loads(session_data)
            logger.debug(f"📄 Sessiya tarkibi: {settings_dict.keys()}")
            print(f"ffffffffffffffffffffffffffffffffffffffffffffffff{settings_dict}")
            cl.set_settings(settings_dict)

            try:
                cl.account_info()  # sessiya to‘g‘ri ishlayotganini tekshirish
                logger.info(f"✅ {username} sessiyasi valid, login qilindi.")
                return "✅ Sessiya orqali muvaffaqiyatli login qilindi."
            except LoginRequired:
                logger.warning(f"⚠️ Sessiya eskirgan. Qayta login qilinmoqda...")

        # 🔐 Yangi login
        logger.info(f"🔐 {username} uchun login bajarilmoqda...")
        cl.login(username, password)

        # 💾 Sessiyani pickle qilib saqlash
        session_bytes = pickle.dumps(cl.get_settings())
        logger.debug(f"🧠 Saqlanayotgan sessiya turi: {type(session_bytes)}")
        logger.debug(f"📄 Sessiya kalitlari: {pickle.loads(session_bytes).keys()}")

        await create_or_update_session(username, session_bytes)
        logger.info(f"✅ {username} login qilindi va sessiya yangilandi.")
        return "✅ Yangi login qilindi va sessiya saqlandi."

    except Exception as e:
        logger.error(f"❌ {username} loginida xatolik: {e}")
        return f"❌ Umumiy xatolik: {e}"

# SESSION_FILE = "src/sessions/login_session1.json"


# def login_to_instagram1(username, password):
#     try:
#         cl.set_locale('en_US')
#         # cl.set_device(Device.generate())

#         if not os.path.exists(SESSION_FILE):
#             cl.login(username, password)
#             cl.dump_settings(SESSION_FILE)
#             return "✅ Login OK"
#         else:
#             try:
#                 cl.load_settings(SESSION_FILE)
#                 cl.login(username, password)

#                 try:
#                     cl.user_info_by_username(username)
#                     return "✅ Sessiya OK"
#                 except LoginRequired:
#                     os.remove(SESSION_FILE)
#                     # cl.set_device(Device.generate())
#                     cl.login(username, password)
#                     cl.dump_settings(SESSION_FILE)
#                     return "♻️ Sessiya yangilandi"
#             except LoginRequired:
#                 os.remove(SESSION_FILE)
#                 # cl.set_device(Device.generate())
#                 cl.login(username, password)
#                 cl.dump_settings(SESSION_FILE)
#                 return "♻️ Sessiya buzilgan edi, qayta login qilindi"
#             except Exception as e:
#                 return f"❌ Xatolik (sessiya): {e}"
#     except Exception as e:
#         return f"❌ Xatolik (asosiy): {e}"