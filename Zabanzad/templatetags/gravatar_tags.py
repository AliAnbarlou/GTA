from django import template
import hashlib

register = template.Library()

@register.filter(name='gravatar')
def gravatar(value, size=40):
    """Generates the gravatar url for an email address."""
    email = value.strip().lower()
    hash_email = hashlib.md5(email.encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_email}?s={size}&d=identicon"
