import os

from instagrapi import Client
# from instagrapi.types import Device
from instagrapi.exceptions import LoginRequired

cl = Client()


SESSION_FILE = "src/sessions/session.json"


def login_to_instagram(username, password):
    try:
        if not os.path.exists(SESSION_FILE):
            cl.set_locale('en_US')
            cl.login(username, password)
            cl.dump_settings(SESSION_FILE)
            return f"✅ Instagram login orqali muvaffaqiyatli ulandi va sessiya saqlandi!"
        else:
            try:
                cl.set_locale('en_US')
                cl.load_settings(SESSION_FILE)
                cl.login(username, password)
                cl.user_info_by_username(username)
                return f"✅ Instagram muvaffaqiyatli ulandi!"
            except LoginRequired:
                os.remove(SESSION_FILE)
                cl.set_locale('en_US')
                cl.login(username, password)
                cl.dump_settings(SESSION_FILE)
                return "✅ Sessiya eskirgani sababli, o'chirilib qayta yaratildi."
            except Exception as e:
                return f"❌ Umumiy xatolik: {e}"
    except Exception as e:
        return f"❌ Umumiy xatolik: {e}"