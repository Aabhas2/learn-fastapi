from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated
 
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars',examples=['Nitish','Amit'])]   
    email: EmailStr
    linkedin: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)] 
    married: Annotated[bool, Field(default=None, description="Is the patient married or not")]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]  
    contact_details: Dict[str,str]


def insert_patient_data(patient: Patient): 
    print(patient.name)
    print(patient.age) 
    print("inserted")

def update_patient_data(patient: Patient): 
    print(patient.name)
    print(patient.age) 
    print("updated")

patient_info = {'name': 'niitsh', 'age': 30, 'weight': 75.2, 'married': True, 'allergies': ['pollen','dust'], 'contact_details': {'email':'abc@gmail.com','phone': '2345152155'}}
  
patient1 = Patient(**patient_info)

insert_patient_data(patient1)