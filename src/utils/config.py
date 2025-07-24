import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_config(key: str, default=None):
    """
    Retrieve a configuration value from environment variables.
    Args:
        key (str): The environment variable key.
        default: The default value if the key is not found.
    Returns:
        The value of the environment variable or the default.
    """
    return os.getenv(key, default) 