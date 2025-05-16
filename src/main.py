from logging.config import dictConfig

from fastapi import FastAPI

from src.core.logging_config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)

app = FastAPI(title="Business management system")
