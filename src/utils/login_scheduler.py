import os

from instagrapi import Client
# from instagrapi.device import Device
from instagrapi.exceptions import LoginRequired

cl = Client()


SESSION_FILE = "src/sessions/login_session1.json"


def login_to_instagram1(username, password):
    try:
        cl.set_locale('en_US')
        # cl.set_device(Device.generate())

        if not os.path.exists(SESSION_FILE):
            cl.login(username, password)
            cl.dump_settings(SESSION_FILE)
            return "✅ Login OK"
        else:
            try:
                cl.load_settings(SESSION_FILE)
                cl.login(username, password)

                try:
                    cl.user_info_by_username(username)
                    return "✅ Sessiya OK"
                except LoginRequired:
                    os.remove(SESSION_FILE)
                    # cl.set_device(Device.generate())
                    cl.login(username, password)
                    cl.dump_settings(SESSION_FILE)
                    return "♻️ Sessiya yangilandi"
            except LoginRequired:
                os.remove(SESSION_FILE)
                # cl.set_device(Device.generate())
                cl.login(username, password)
                cl.dump_settings(SESSION_FILE)
                return "♻️ Sessiya buzilgan edi, qayta login qilindi"
            except Exception as e:
                return f"❌ Xatolik (sessiya): {e}"
    except Exception as e:
        return f"❌ Xatolik (asosiy): {e}"