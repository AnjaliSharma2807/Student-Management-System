from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Student Management APP")

# Temporary storage
students = {}
next_id = 1


# Pydantic model for validating student data
class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=1, lt=100)
    course: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=10)


# Home route
@app.get("/")
def home():
    return {"message": "Welcome to Student Management API"}


# 1. Create a student
@app.post("/students", status_code=201)
def create_student(student: Student):
    global next_id

    student_data = student.model_dump()
    students[next_id] = student_data

    created_id = next_id
    next_id += 1

    return {
        "message": "Student created successfully",
        "id": created_id,
        "data": student_data
    }


# 2. Read all students
@app.get("/students")
def read_students():
    return students


# 3. Read one student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]


# 4. Update a student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student_data = student.model_dump()
    students[student_id] = student_data

    return {
        "message": "Student updated successfully",
        "id": student_id,
        "data": student_data
    }


# 5. Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "data": deleted_student
    }