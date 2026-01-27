from pydantic import BaseModel, EmailStr, Field, AnyUrl, field_validator 
from typing import List, Dict, Optional, Annotated 


class Patient(BaseModel): 
    name: str 
    email: EmailStr
    age: int 
    weight: float 
    married: bool 
    allergies: List[str] 
    contact_details: Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value): 
        valid_domains = ['hdfc.com','icici.com']
        domain_name = value.split("@")[1]
        if domain_name not in valid_domains: 
            raise ValueError("Not a valid domain")
        return value 

    @field_validator('name')
    @classmethod
    def transform_name(cls, value): 
        return value.upper()

def update_patient_data(patient: Patient): 
    
    print(patient.name)
    print(patient.age) 
    print(patient.allergies)                
    print(patient.married) 
    print('updated')


patient_info = {'name':'nitish','email':'abc@gmail.com','age':'30','weight':72.4,'married':True,'allergies':['pollen','dust'],'contact_details':{'phone':'23515123'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1) 