from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data from the JSON file
with open("q-vercel-python.json") as f:
    data = json.load(f)

# Convert to dictionary for fast lookup
marks_dict = {entry["name"]: entry["marks"] for entry in data}

@app.get("/api")
def get_marks(name: list[str] = []):
    result = [marks_dict.get(n, None) for n in name]
    return {"marks": result}
