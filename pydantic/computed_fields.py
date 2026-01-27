from pydantic import BaseModel, EmailStr
from typing import List, Dict 

class Patient(BaseModel): 
    name: str 
    email: EmailStr
    age: int 
    weight: float 
    height: float 
    married: bool 
    allergies: List[str] 
    contact_details: Dict[str,str]