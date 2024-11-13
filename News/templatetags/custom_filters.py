from django import template


register = template.Library()

ILLEGAL_WORDS = ['викинги', 'Викинги', 'викингов',
                 'лидер', 'Лидер']

@register.filter()
def censor(value, bad_word=None):

    splitted_text = value.split()
    censored_text = []

    for word in splitted_text:
        for bad_word in ILLEGAL_WORDS:
            if word.startswith(bad_word):
                censored_word = word[0] + '*'*(len(word) - 1)
                censored_text.append(censored_word)
                break
        else:
            censored_text.append(word)

    return ' '.join(censored_text)



