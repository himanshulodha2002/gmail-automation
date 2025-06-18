from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Gmail API settings
    gmail_client_id: str = Field(..., env='GMAIL_CLIENT_ID')
    gmail_client_secret: str = Field(..., env='GMAIL_CLIENT_SECRET')
    gmail_redirect_uri: str = Field(..., env='GMAIL_REDIRECT_URI')
    
    # Database settings
    database_url: str = Field(..., env='DATABASE_URL')
    
    # Logging settings
    log_level: str = Field('INFO', env='LOG_LEVEL')

    class Config:
        env_file = '.env'
        case_sensitive = True

settings = Settings()