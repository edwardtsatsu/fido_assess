from pydantic import BaseModel, ConfigDict, Field, computed_field

from src.utils import decrypt_text


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    @computed_field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    model_config = ConfigDict(from_attributes=True)
