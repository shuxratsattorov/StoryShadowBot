import pickle
from instagrapi import Client
# from instagrapi.types import Device
from instagrapi.exceptions import LoginRequired
from src.database.orm.session import get_session_data, create_or_update_session

cl = Client()


async def login_to_instagram(username: str, password: str) -> str:
    cl.set_locale('en_US')

    session = await get_session_data(username)

    try:
        if session:
            session_dict = pickle.loads(session)
            cl.load_settings(pickle.loads(session))
            cl.init()
            cl.account_info()
            return "✅ Sessiya orqali muvaffaqiyatli login qilindi."

        cl.login(username, password)
        await create_or_update_session(username, session_data=pickle.dumps(cl.get_settings()))
        return "✅ Yangi login qilindi va sessiya saqlandi."

    except LoginRequired:
        cl.login(username, password)
        await create_or_update_session(username, session_data=pickle.dumps(cl.get_settings()))
        return "✅ Sessiya yaroqsiz edi, qayta login qilindi va yangilandi."

    except Exception as e:
        return f"❌ Umumiy xatolik: {e}"



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




# SESSION_FILE = "src/sessions/session.json"


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