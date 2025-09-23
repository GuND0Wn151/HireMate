#create a config to get database url from env variable use pydantic
from pydantic import BaseModel, PostgresDsn, Field
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
      DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")
      DB_MIN_SIZE: int = Field(1, env="DB_MIN_SIZE")
      DB_MAX_SIZE: int = Field(10, env="DB_MAX_SIZE")
      User: str = Field(..., env="user")
      Password: str = Field(..., env="password")
      Host: str = Field(..., env="host")
      Port: str = Field(..., env="port")
      Dbname: str = Field(..., env="dbname")
      
      # JWT Settings
      SECRET_KEY: str = Field("your-secret-key-change-this-in-production", env="SECRET_KEY")
      ALGORITHM: str = Field("HS256", env="ALGORITHM")
      ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
      
      # Firecrawl
      FIRECRAWL_API_KEY: Optional[str] = Field(None, env="FIRECRAWL_API_KEY")
      
      class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"

settings = Settings()