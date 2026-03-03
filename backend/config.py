from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    port: int = 5000
    frontend_url: str
    node_env: str = "development"
    
    # JWT Settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Service URLs
    container_service_url: str
    ai_agent_service_url: str
    tunnel_service_url: str
    
    # Database
    database_path: str

    model_config = SettingsConfigDict(env_file=".env.example")

settings = Settings()