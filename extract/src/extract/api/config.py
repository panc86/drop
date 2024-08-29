from pydantic import BaseModel, ConfigDict


class APIConfig(BaseModel):
    model_config = ConfigDict()
    description: str = "REST API to extract disaster based data"
    license_info: dict[str, str] = {
        "name": "Change me",
        "url": "https://example.com",
    }
    title: str = "DROP Extract API"
    version: str = "0.1.0"
