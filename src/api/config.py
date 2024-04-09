"""
Application's and its environment's configuration.
"""

import dotenv
import os

dotenv.load_dotenv()


class AuthConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", ...)
    ALGORITHM = os.getenv("ALGORITHM", ...)
    ACCESS_TOKEN_EXPIRE_MINUTES: float = float(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", ...)
    )


class DBConfig:
    """Database configuration."""

    DB_DRIVERNAME = os.getenv("DB_DRIVERNAME", ...)
    DB_USERNAME = os.getenv("DB_USERNAME", ...)
    DB_PASSWORD = os.getenv("DB_PASSWORD", ...)
    DB_HOST = os.getenv("DB_HOST", ...)
    DB_PORT: int = int(os.getenv("DB_PORT", ...))
    DB_DATABASE = os.getenv("DB_DATABASE", ...)


class SendGridConfig:
    """Send Grid configuration."""

    API_KEY = os.getenv("SENDGRID_API_KEY", ...)
    EMAIL = os.getenv("SENDGRID_EMAIL", ...)


class Config:
    """Base configuration."""

    ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
    DEBUG = ENVIRONMENT == "DEV"
    TESTING = ENVIRONMENT == "TEST"

    HOST = os.getenv("APPLICATION_HOST", "127.0.0.1")
    PORT = int(os.getenv("APPLICATION_PORT", "3000"))
    WORKERS_COUNT = int(os.getenv("WORKERS_COUNT", "1"))
    RELOAD = os.getenv("RELOAD", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    APPLICATION_ROOT = os.getenv("APPLICATION_ROOT", "")

    DB_CONFIG: DBConfig = DBConfig()
    SENDGRID_CONFIG: SendGridConfig = SendGridConfig()
    AUTH: AuthConfig = AuthConfig()
