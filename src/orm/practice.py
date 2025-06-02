import os
from dotenv import load_dotenv

load_dotenv()


def load_chats():
    chat_ids = os.getenv("CHAT_ID")
    if chat_ids:
        chat_ids = chat_ids.strip("[]").replace('"', '').replace("'", "").split(",")
        try:
            return list(map(int, map(str.strip, chat_ids)))
        except ValueError:
            return []
    return []


def save_chats(chat_ids):
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    chat_ids_str = "[" + ", ".join(map(str, chat_ids)) + "]"

    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    with open(env_path, "w", encoding="utf-8") as f:
        for line in lines:
            if not line.startswith("CHAT_ID = "):
                f.write(line)
        f.write(f"CHAT_ID = {chat_ids_str}\n")


def is_admin(user_id):
    admin_ids = {5146109604}
    return user_id in admin_ids


def add_admin(chat_id: str):
    chat_id = int(chat_id)
    chat_list = load_chats()

    if chat_id in chat_list:
        return f"⚠️ Bu chat allaqachon qo‘shilgan!"

    chat_list.append(chat_id)
    save_chats(chat_list)
    return f"✅ Admin {chat_id} qo‘shildi!"


def delete_admin(chat_id: str):
    chat_id = int(chat_id)
    chat_list = load_chats()

    if chat_id not in chat_list:
        return f"⚠️ Chat ID {chat_id} ro‘yxatda yo‘q!"

    chat_list.remove(chat_id)
    save_chats(chat_list)
    return f"✅ Chat ID {chat_id} o‘chirildi!"


def show_list_admin():
    chat_list = load_chats()
    if not chat_list:
        return f"⚠️ Adminlar ro‘yxati bo‘sh!"

    result = "***Adminlar ro‘yxati:***\n"
    for ids, chat_id in enumerate(chat_list, start=1):
        result += f"{ids}. {chat_id}\n"

    return result


def main():
    print("Oldingi CHAT_ID lar:", load_chats())
    print(add_admin("5146109624"))
    print(delete_admin("5146109623"))
    print(show_list_admin())


if __name__ == '__main__':
    main()