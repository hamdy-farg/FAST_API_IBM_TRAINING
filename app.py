from fastapi import FastAPI, Request
from model import Student, db
import uuid
app = FastAPI()


@app.get("/student")
def get_all_student():
    """ get all student from db"""

    return {"student":db}, 200

@app.get("/student/{student_id}")
def get_student(student_id: int):
    """ get one student from db by id"""

    if (student_id in db):
        return {"student":db[student_id]}, 200
    else:
        return {"msg":"the student not foudn"}, 404
    


@app.post("/student")
async def  create_student( request: Request) :
    """ create one student with first and last name """

    if request.headers.get("content-length") == "0":
        return {"msg" : "include json body with first and last name"}
    #
    request_data = await  request.json()
    #
    if ("first_name" not in request_data and 
        "last_name" not in request_data):
        return {"msg": 
        "the request can not be resolved duo to missing data ('first_name', 'last_name')"}
    
    student_id = uuid.uuid4().hex

    #
    student = Student(
        first_name = request_data["first_name"],
        last_name = request_data["last_name"],
        student_id = student_id)
    #
    db[student_id] = student.model_dump()
    return {"student":db[student_id]}, 201


@app.put("/student/{student_id}")
async def  update_student(student_id: str, request: Request) :
    """ update one student by student id """

    request_data = await  request.json()
    
    if (student_id in db.keys()):
        #
        student = Student(
        first_name = request_data["first_name"] or db[student_id]["first_name"],
        last_name = request_data["last_name"] or db[student_id]["last_name"],
        student_id = student_id)
        #
        db[student_id] |= student.model_dump()
        return {"student":db[student_id]}, 200
    else:
        return {"msg":"the student not found"}, 404
    

@app.delete("/student/{student_id}")
async def  Delete_student(student_id: str, request: Request) :
    """ delete one student by student id """

    
    if (student_id in db.keys()):
        del db[student_id] 
        return {"msg":" deleted successfully"}, 200
    else:
        return {"msg":"the student not found"}, 404
    