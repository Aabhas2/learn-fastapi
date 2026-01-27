from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict 

class Patient(BaseModel): 
    name: str 
    email: EmailStr
    age: int 
    weight: float  #kg 
    height: float  #mtr 
    married: bool 
    allergies: List[str] 
    contact_details: Dict[str,str]

    @computed_field
    @property
    def calculate_bmi(self) -> float: 
        bmi = round(self.weight/(self.height**2),2)


def update_patient_data(patient: Patient): 

    print(patient.name)
    print(patient.age) 
    print(patient.allergies)
    print(patient.married)
    print('updated')