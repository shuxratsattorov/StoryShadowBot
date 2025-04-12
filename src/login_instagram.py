from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    LoginRequired,
    TwoFactorRequired,
    ChallengeRequired,
    PleaseWaitFewMinutes,
    ClientError
)

cl = Client()


def login_to_instagram(username, password):
    try:
        cl.login(username, password)
        return f"✅ Instagram muvaffaqiyatli ulandi!"

    except BadPassword:
        return f"❌ ERROR: Login yoki parol noto‘g‘ri!"

    except TwoFactorRequired:
        return f"⚠️ ERROR: Ikki bosqichli tasdiqlash (2FA) yoqilgan, kod kiritish kerak!"

    except ChallengeRequired:
        return f"🔐 ERROR: Instagram akkauntingiz tasdiqlash (checkpoint) talab qiladi! Brauzerda kirib, tekshiring."

    except PleaseWaitFewMinutes:
        return f"⏳ ERROR: Juda ko‘p urinish! Bir necha daqiqa kuting va qaytadan urinib ko‘ring."

    except LoginRequired:
        return f"🚫 ERROR: Instagram akkauntingizga qayta kirish talab qilinadi!"

    except ClientError as e:
        return f"⚠️ ERROR: Instagram xatosi: {e}"

    except Exception as e:
        return f"⚠️ ERROR: Noma’lum xatolik: {e}"