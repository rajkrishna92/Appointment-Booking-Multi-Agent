import re
from pydantic import BaseModel, Field, field_validator


class DateTimeModel(BaseModel):
    date:str=Field(description="Properly formatted date", pattern=r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$')
    
    @field_validator("date")
    def check_format_date(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$', v):  # Ensures 'DD-MM-YYYY HH:MM' format
            raise ValueError("The date should be in format 'DD-MM-YYYY HH:MM'")
        return v
    
class DateModel(BaseModel):
    date: str = Field(description="Properly formatted date", pattern=r'^\d{2}-\d{2}-\d{4}$')
    @field_validator("date")
    def check_format_date(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', v):  # Ensures DD-MM-YYYY format
            raise ValueError("The date must be in the format 'DD-MM-YYYY'")
        return v
     
class EmailModel(BaseModel):
    email: str = Field(
        description="Properly formatted email address",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )

    @field_validator("email")
    def check_format_email(cls, v: str) -> str:
        # This regex is a simple‐ish email check; you can swap in a more elaborate one if needed.
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
            raise ValueError("The email must be in a valid format, e.g. 'user@example.com'")
        return v
    