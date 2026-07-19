from fastapi import FastAPI, Path, HTTPException 
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John Doe",
        "age": 20,
        "major": "Computer Science"
    }
}

class Student(BaseModel):
    name: str
    age: int
    major: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    major: Optional[str] = None

@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(..., gt=0, description="Student ID")
):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    return students[student_id]


@app.get("/get-by-name/{student_id}")
def get_student_by_name(*, student_id: int, name: Optional[str]=None, test: int):
    if not name:
        raise HTTPException(status_code=400, detail="Name parameter is required")
    for student_id, student in students.items():
        if student["name"].lower() == name.lower():
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    students[student_id] = student.dict()
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    student_data = students[student_id]
    for field, value in student.dict(exclude_unset=True).items():
        student_data[field] = value

    return student_data

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    del students[student_id]
    return {"detail": "Student deleted successfully"}