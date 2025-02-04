import re


def extract_urls(text):
    # Регулярное выражение для поиска URL
    url_pattern = r'(https?://[^\s]+|www\.[^\s]+)'

    return re.findall(url_pattern, text)
