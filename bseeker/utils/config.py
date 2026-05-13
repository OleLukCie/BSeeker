import os
from dotenv import load_dotenv


def load_env():
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(base, '.env')
    load_dotenv(env_path)


def get(key, default=None):
    load_env()
    return os.getenv(key, default)


def get_int(key, default=0):
    val = get(key, default)
    return int(val) if val is not None else default


def get_float(key, default=0.0):
    val = get(key, default)
    return float(val) if val is not None else default


def get_bool(key, default=False):
    val = get(key, str(default).lower())
    return val.lower() in ('true', '1', 'yes', 'on')
