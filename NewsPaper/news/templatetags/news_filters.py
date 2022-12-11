from django import template
import re

register = template.Library()

RESTRICTED_WORDS = [
    'искусств',
    'демократ'
]

@register.filter()
def censor(text: str) -> str:
    """Цензурировать текст, маскируя запрещённые слова символом *"""
    if not isinstance(text, str):
        raise ValueError
    for r_word in RESTRICTED_WORDS:
        r_set = word_occurrences(text, r_word)
        for word in r_set:
            text = text.replace(word, word[0] + '*' * (len(word) - 1))
    return text

def word_occurrences(text, pattern):
    pattern = r'\w*%s\w*' % re.escape(pattern)
    return set(re.findall(pattern, text, flags=re.IGNORECASE))