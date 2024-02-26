from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    """
    class for settings, allowing values to be overridden by environment variables.

    """

    IS_ON_DEV_MACHINE: bool = (
        True  # True if the service is running locally on developer machine.
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PROJECT_NAME = "jobs-py-crawling-service"
    SERVER_NAME: str = "EKS"
    VERSION: str = "1.0"
    DD_SERVICE_NAME: str = "jobs-py-crawling-service"
    DEBUG = False
    APP_ENV = "dev"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    OTEL_TRACES_EXPORTER = "otlp"
    OTEL_RESOURCE_ATTRIBUTES = "service.name=jobs-py-crawling-service,application=app"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
