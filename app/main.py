import os
import logging
from fastapi import FastAPI
from app.utils import logs
from app.config import Settings

# Init logs directory
if not os.path.exists("logs"):
    os.mkdir("logs")

logs.init_logging(file_path='logs/logfile.log', level='INFO')
logger = logging.getLogger(__name__)

logger.info("Starting WookieBooks")
SETTINGS = Settings()

from app.db import database, models

logger.info("Creating app")
app = FastAPI()

# Check if DB is not empty
session = next(database.get_db())
if session.query(models.UserORM).count() < 1:
    logger.warning("No users found in database. Initializing default user table")
    database.init_empty_user_db(session)
else:
    RESTIRCTED_USERS = session.query(models.UserORM.username).filter(models.UserORM.enabled == False).all()

from app.api import api_router
logger.info('Loading routers')
app.include_router(api_router.api_router)
