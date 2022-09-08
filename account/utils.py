from string import ascii_lowercase, digits
import secrets


def random_chars(size):
    res = ''.join(secrets.SystemRandom().choices(ascii_lowercase + digits, k=size))
    return res
