# from instagrapi.exceptions import LoginRequired
# from instagrapi import Client
# import uuid
# import os

# SESSION_FILE = "src/sessions/session_test.json"

# def generate_device_settings():
#     return {
#         "app_version": "269.0.0.18.68",
#         "android_version": 28,
#         "android_release": "9.0",
#         "dpi": "480dpi",
#         "resolution": "1080x1920",
#         "manufacturer": "Samsung",
#         "device": "heroqlte",
#         "model": "SM-G930F",
#         "cpu": "samsungexynos8890",
#         "version_code": "314665256"
#     }

# def generate_user_agent(device_settings):
#     return (
#         f"Instagram {device_settings['app_version']} Android "
#         f"({device_settings['android_version']}/{device_settings['android_release']}; "
#         f"{device_settings['dpi']}; {device_settings['resolution']}; "
#         f"{device_settings['manufacturer']}; {device_settings['model']}; "
#         f"{device_settings['device']}; {device_settings['cpu']}; en_US; "
#         f"{device_settings['version_code']})"
#     )

# def generate_uuids():
#     return {
#         "phone_id": str(uuid.uuid4()),
#         "uuid": str(uuid.uuid4()),
#         "client_session_id": str(uuid.uuid4()),
#         "advertising_id": str(uuid.uuid4()),
#         "device_id": f"android-{uuid.uuid4().hex[:16]}"
#     }

# def login_to_instagram(username, password):
#     cl = Client()
#     cl.set_locale('en_US')

#     device_settings = generate_device_settings()
#     user_agent = generate_user_agent(device_settings)
#     uuids = generate_uuids()

#     cl.device_settings = device_settings
#     cl.user_agent = user_agent
#     cl.uuid = uuids["uuid"]
#     cl.phone_id = uuids["phone_id"]
#     cl.advertising_id = uuids["advertising_id"]
#     cl.client_session_id = uuids["client_session_id"]
#     cl.device_id = uuids["device_id"]

#     try:
#         if not os.path.exists(SESSION_FILE):
#             cl.login(username, password)
#             cl.dump_settings(SESSION_FILE)
#             return cl, "✅ Simulyatsiya orqali login qilingan va sessiya saqlandi!"
#         else:
#             try:
#                 cl.load_settings(SESSION_FILE)
#                 cl.login(username, password)
#                 cl.user_info_by_username(username)
#                 return cl, "✅ Sessiya mavjud edi, undan foydalangan holda muvaffaqiyatli login qilindi!"
#             except LoginRequired:
#                 os.remove(SESSION_FILE)
#                 cl.login(username, password)
#                 cl.dump_settings(SESSION_FILE)
#                 return cl, "♻️ Sessiya muddati o‘tgan, yangilandi va qaytadan login qilindi!"
#             except Exception as e:
#                 return None, f"❌ Login xatosi (sessiya mavjud): {e}"
#     except Exception as e:
#         return None, f"❌ Login xatosi (yangi sessiya): {e}"

# def download_stories(cl, target_username, save_dir="downloaded_stories"):
#     try:
#         user_id = cl.user_id_from_username(target_username)
#         stories = cl.user_stories(user_id)
        
#         if not stories:
#             return f"ℹ️ '{target_username}' foydalanuvchining aktiv storieslari yo‘q."

#         os.makedirs(save_dir, exist_ok=True)
#         count = 0

#         for story in stories:
#             try:
#                 if story.media_type == 1:  # Photo
#                     cl.photo_download(story.pk, folder=save_dir)
#                 elif story.media_type == 2:  # Video
#                     cl.video_download(story.pk, folder=save_dir)
#                 else:
#                     print(f"⚠️ Noma’lum media turi: {story.media_type}, pk={story.pk}")
#                 count += 1
#             except Exception as media_err:
#                 print(f"❌ Story pk={story.pk} yuklashda xatolik: {media_err}")
#     except Exception as e:
#         return f"❌ Stories yuklashda xatolik yuz berdi: {e}"


# username = "strv.13"
# password = "shuhrat4ik13iq"
# target_user = "nzrvna_8880"

# cl, login_status = login_to_instagram(username, password)
# print(login_status)

# if cl:
#     result = download_stories(cl, target_user)
#     print(result)


from instagrapi import Client

cl = Client()

cl.challenge_resolve(code)
print(dir(cl))