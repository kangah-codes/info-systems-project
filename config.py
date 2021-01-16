import random
import string

def gen_session():
	chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
	return ''.join(random.choice(chars) for _ in range(10))+'-'+''.join(random.choice(chars) for _ in range(10))

def gen_pass():
	chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
	return ''.join(random.choice(chars) for _ in range(5))

def gen_id(typeOf):
    if typeOf == 1:
        chars = string.ascii_uppercase+string.digits
        return 'PAT-'+''.join(random.choice(chars) for _ in range(6))
    elif typeOf == 3:
        chars = string.digits
        return 'BAT-'+''.join(random.choice(chars) for _ in range(6))
    elif typeOf == 4:
        chars = string.ascii_uppercase+string.ascii_lowercase
        return 'STF-'+''.join(random.choice(chars) for _ in range(3))
    elif typeOf == 5:
        chars = string.digits
        return 'APT-'+''.join(random.choice(chars) for _ in range(3))
    elif typeOf == 6:
        chars = string.digits+string.ascii_lowercase
        return 'PRS-'+''.join(random.choice(chars) for _ in range(3))
    return None

#print(gen_session())
