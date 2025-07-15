from instagrapi import Client
from pathlib import Path

def instagram_login(username: str, password: str) -> Client:
    """
    Instagramga login bo'lish
    """
    cl = Client()
    cl.login(username, password)
    return cl

def download_stories_by_username(your_username: str, your_password: str, target_username: str, folder: str = "downloads"):
    """
    Foydalanuvchi username'iga qarab storylarni yuklab olish
    """
    # Login
    cl = instagram_login(your_username, your_password)

    # Target foydalanuvchi ID sini olish
    target_user_id = cl.user_id_from_username(target_username)

    # Storylar ro'yxatini olish
    stories = cl.user_stories_v1(str(target_user_id))
    print(f"{len(stories)} ta story topildi foydalanuvchi: @{target_username}")

    # Papkani yaratish
    Path(folder).mkdir(parents=True, exist_ok=True)

    # Storylarni yuklab olish
    for story in stories:
        file_path = cl.story_download(story.pk, folder=Path(folder))
        print(f"Yuklab olindi: {file_path}")

# ==== FOYDALANISH MISOLI ====
download_stories_by_username("anonymous.stories.ooo", "shuhrat4ik13iq", "strv.13")
