import random


def random_ip():
    ip = "%s.%s.%s.%s" % (
        random.randint(1, 255), random.randint(1, 255),
        random.randint(1, 255), random.randint(1, 255))
    return ip
