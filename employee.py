from pydantic import BaseModel


class Employee(BaseModel):
    name: str
    title: str
    salary: int
