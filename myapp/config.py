from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Sets the base directory path
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected env variable '{}' not set.".format(name)
        raise Exception(message)

@dataclass
class ApplicationConfig(object):
    DB_TRACK_MODIFICATIONS = get_env_variable("DB_TRACK_MODIFICATIONS")
    DATABASE_URI: str = get_env_variable('DB_URI')