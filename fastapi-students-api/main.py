from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS (allow all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read CSV and cache student records
students = []
with open("q-fastapi.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row["studentId"] = int(row["studentId"])  # Convert to int
        students.append(row)

@app.get("/api")
async def get_students(class_: list[str] = None):
    if class_:
        filtered = [s for s in students if s["class"] in class_]
        return {"students": filtered}
    return {"students": students}
