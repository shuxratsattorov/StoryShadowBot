import pickle
from instagrapi import Client
# from instagrapi.types import Device
from instagrapi.exceptions import LoginRequired
from src.database.orm.session import get_session, create_or_update_session

cl = Client()


async def login_to_instagram(username: str, password: str) -> str:
    cl.set_locale('en_US')

    session = await get_session(username)

    try:
        if session:
            cl.load_settings(pickle.loads(session))
            cl.login(username, password)
            cl.user_info_by_username(username)
            return "✅ Instagramga mavjud sessiya orqali muvaffaqiyatli login qilindi."

        cl.login(username, password)
        await create_or_update_session(username, pickle.dumps(cl.get_settings()))
        return "✅ Yangi login qilindi va sessiya PostgreSQL'ga saqlandi."

    except LoginRequired:
        cl.login(username, password)
        await create_or_update_session(username, pickle.dumps(cl.get_settings()))
        return "✅ Sessiya yaroqsiz edi, qayta login qilindi va yangilandi."

    except Exception as e:
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