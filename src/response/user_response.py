from pydantic import BaseModel, ConfigDict, Field, computed_field


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)
