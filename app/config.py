from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    google_client_id: str
    google_client_secret: str
    facebook_client_id: str
    facebook_client_secret: str

    class Config:
        env_file = ".env"

settings = Settings()
