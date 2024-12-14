from transliterate import translit
import re

def generate_slug_from_ru_text(text) -> str:
    slug = ''
    for word in translit(text, 'ru', reversed=True).split():
        word = re.sub(r'[^a-zA-Z]', '', word)
        slug += word[:1].upper() + word[1:].lower()

    return slug
