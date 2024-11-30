from pydantic import BaseModel


class Activities(BaseModel):
    activities: list[str]
