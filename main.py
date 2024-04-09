from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://a1akashchauhanpersonal:heicuMmmOWSwt2hO@cluster0.jd1q1xj.mongodb.net/")
db = client["library_management"]
students_collection = db["students"]

# Models
class Student(BaseModel):
    name: str
    age: int
    address: dict

class UpdateStudent(BaseModel):
    name: str = None
    age: int = None
    address: dict = None


@app.post("/students", status_code=201)
async def create_student(student: Student):

    result = students_collection.insert_one(student.model_dump())
    return {"id": str(result.inserted_id)}

@app.get("/students", status_code=200)
async def list_students(country: str = Query(None), age: int = Query(None)):

    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}


    students = students_collection.find(query, {"_id": 0})

    return {"data": list(students)}

@app.get("/students/{id}", status_code=200)
async def get_student(id: str):

    student = students_collection.find_one({"_id": ObjectId(id)}, {"_id": 0})

    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: UpdateStudent):

    update_fields = {}
    if student.name is not None:
        update_fields["name"] = student.name
    if student.age is not None:
        update_fields["age"] = student.age
    if student.address is not None:
        update_fields["address"] = student.address

    # Update student record in MongoDB
    students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})

@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    # Delete student record from MongoDB
    result = students_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
