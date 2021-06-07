import random
import string

def generate_activation_code():
    activation_code = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    return activation_code