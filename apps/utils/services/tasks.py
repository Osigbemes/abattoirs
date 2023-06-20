import random
from django.utils import timezone

def generate_code():
    random_number = random.SystemRandom().randrange(100000, 999999)
    random_code = random_number, '_' + str(timezone.now())
    return random_code