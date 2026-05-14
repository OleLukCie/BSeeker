import os   # for environment variables
from dotenv import load_dotenv  # for loading .env files


def load_env():
    '''
    Locate and load environment variables from the .env file in the project root.
    Automatically finds the project root directory
    '''
    # Get the absolute path to the project root directory
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Build full path to the .env file
    env_path = os.path.join(base, '.env')
    load_dotenv(env_path)


def get(key, default=None):
    '''
    Get an environment variable as a string.
    Automatically loads the .env file before reading.

    Args:
        key (str): Environment variale name
        default: Value to return if the key is not found

    Returns:
        str or None
    '''
    load_env()
    return os.getenv(key, default)


def get_int(key, default=0):
    '''
    Get an environment variable and convert it to an integer.

    Args:
        key (str): Environment variable name
        default (int): Default integer value if key is missing or invalid

    Returns: 
        int: Parsed integer value
    '''
    val = get(key, default)
    return int(val) if val is not None else default


def get_float(key, default=0.0):
    '''
    Get an environment variable and convert it to a float.

    Args:
        key (str): Environment variable name
        default (float): Default float value if key is missing or invalid

    Returns:
        float: Parsed float value
    '''
    val = get(key, default)
    return float(val) if val is not None else default


def get_bool(key, default=False):
    '''
    Get an environment variable and safely convert it to a boolean.
    Recognizes: 'true', '1', 'yes', 'on' as True

    Args:
        key(str): Environment variable name
        default (bool): Default boolean value if key is missing

    Returns:
        bool: Parsed boolean value
    '''
    val = get(key, str(default).lower())
    return val.lower() in ('true', '1', 'yes', 'on')
