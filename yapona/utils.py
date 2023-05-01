import random
import string

kAppName = "yapona"

def generate_id(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
