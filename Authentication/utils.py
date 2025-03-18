import hashlib

def get_gravatar_url(email, size=512):  # افزایش اندازه به 512px
    """دریافت آواتار گراواتار با ایمیل کاربر"""
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
