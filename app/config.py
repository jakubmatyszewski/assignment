import os
import secrets
import logging
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        self.SECRET_KEY = secrets.token_urlsafe(32)
        self.DB_ADDRESS = None
        self.DB_NAME = None
        self.DB_USER = None
        self.DB_PASSWORD = None
        
        load_dotenv()
        self.load_env_variables()

        # Validate loaded db data
        for var in ['DB_ADDRESS', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']:
            if getattr(self, var, None) is None:
                logger.error(f'{var} must be defined')


    def load_env_variables(self):
        # List of environment variables to load
        env_vars = ['DB_ADDRESS', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']

        for var in env_vars:
            if os.getenv(var) is not None:
                setattr(self, var, os.getenv(var))

logger = logging.getLogger('settings')
