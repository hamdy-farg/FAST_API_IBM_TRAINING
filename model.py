from pydantic import BaseModel

class Student(BaseModel):
    student_id : str 
    first_name : str
    last_name : str

db = {}