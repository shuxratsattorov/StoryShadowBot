import os
import requests
import re

from instagrapi import Client
from instagrapi.exceptions import (
     BadPassword,
     LoginRequired,
     TwoFactorRequired,
     ChallengeRequired,
     PleaseWaitFewMinutes,
     ClientError,
     UserNotFound
)

cl = Client()


def login_to_instagram(username, password):
    try:
        cl.login(username, password)
        return "✅ Instagram muvaffaqiyatli ulandi!"

    except BadPassword:
        return "❌ ERROR: Login yoki parol noto‘g‘ri!"

    except TwoFactorRequired:
        return "⚠️ ERROR: Ikki bosqichli tasdiqlash (2FA) yoqilgan, kod kiritish kerak!"

    except ChallengeRequired:
        return "🔐 ERROR: Instagram akkauntingiz tasdiqlash (checkpoint) talab qiladi! Brauzerda kirib, tekshiring."

    except PleaseWaitFewMinutes:
        return "⏳ ERROR: Juda ko‘p urinish! Bir necha daqiqa kuting va qaytadan urinib ko‘ring."

    except LoginRequired:
        return "🚫 ERROR: Instagram akkauntingizga qayta kirish talab qilinadi!"

    except ClientError as e:
        return f"⚠️ ERROR: Instagram xatosi: {e}"

    except Exception as e:
        return f"⚠️ ERROR: Noma’lum xatolik: {e}"


def get_profile_info(username_or_url, save_path="users_media/"):

    match = re.search(r"instagram\.com/([a-zA-Z0-9_.]+)", username_or_url)
    if match:
        username = match.group(1).split("?")[0]
    else:
        username = username_or_url

    try:
        user_info = cl.user_info_by_username(username)
        profile_pic_url = user_info.profile_pic_url

        if not profile_pic_url:
            print("⚠️ Profil rasmi topilmadi!")
            return

        os.makedirs(save_path, exist_ok=True)

        file_name = os.path.join(save_path, f"{username}_profile.jpg")
        response = requests.get(profile_pic_url, stream=True)

        if response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"✅ Profil rasmi saqlandi: {file_name}")

    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")


def download_stories(username_or_url, save_path="stories_media/"):

    match = re.search(r"instagram\.com/([a-zA-Z0-9_.]+)", username_or_url)
    if match:
        username = match.group(1).split("?")[0]
    else:
        username = username_or_url

    try:
        user_id = cl.user_id_from_username(username)
        stories = cl.user_stories(user_id)

        if not stories:
            print("⚠️ Ushbu foydalanuvchida hikoyalar yo‘q!")
            return

        os.makedirs(save_path, exist_ok=True)

        for index, story in enumerate(stories):
            try:
                media_url = story.video_url or story.thumbnail_url
                if not media_url:
                    print(f"⚠️ {index + 1}-hikoya formati aniqlanmadi.")
                    continue

                file_extension = ".mp4" if story.video_url else ".jpg"
                file_name = os.path.join(save_path, f"{username}_story_{index + 1}{file_extension}")

                response = requests.get(media_url, stream=True)

                if response.status_code == 200:
                    with open(file_name, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    print(f"✅ {index + 1}-hikoya saqlandi: {file_name}")
                else:
                    print(f"❌ {index + 1}-hikoyani yuklab olishda xatolik!")

            except Exception as e:
                print(f"❌ {index + 1}-hikoyani yuklashda xatolik: {e}")

    except UserNotFound:
        print(f"❌ Foydalanuvchi topilmadi!")

    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")


login_result = login_to_instagram("anonymous.stories.ooo", "shuhrat4ik13iq")
print(login_result)


def main():
    if "✅" in login_result:
        while True:
            print("\nInstagram Story Yuklash Menyusi")
            print("1. Foydalanuvchi hikoyalarini yuklash")
            print("2. Chiqish")

            choice = input("Tanlang (1/2/3): ")

            if choice == "1":
                username_or_url = input("Instagram foydalanuvchi nomi yoki URL: ")
                download_stories(username_or_url)
            elif choice == "2":
                username_or_url = input("Instagram foydalanuvchi nomi yoki URL: ")
                get_profile_info(username_or_url)
            elif choice == "3":
                print("🚪 Dasturdan chiqildi!")
                break
            else:
                print("❌ Noto‘g‘ri tanlov! Iltimos, qaytadan urinib ko‘ring.")


if __name__ == '__main__':
    main()