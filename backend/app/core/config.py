from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GEMINI_API_KEY: str

    # Telegram integration settings
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ALLOWED_USER_ID: int
    DEVORA_USER_ID: int = 1

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # prevents crashes if extra variables exist in .env
    )


settings = Settings()