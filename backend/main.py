from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Dict, List
import asyncio
import json
from pytz import utc


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a model for the Case
class Case(BaseModel):
    id: int
    created_at: datetime
    status: str

# Initialize an empty list to store cases
cases_db: Dict[int, Case] = {}

# Counter for generating unique IDs
case_id_counter = 1

# Create a case
@app.post("/cases/", response_model=Case)
async def create_case():
    global case_id_counter
    # Get the current datetime in UTC timezone
    created_at = datetime.now(utc)
    new_case = Case(id=case_id_counter, created_at=created_at, status="submitted")
    cases_db[case_id_counter] = new_case
    case_id_counter += 1
    asyncio.create_task(update_case_status(new_case.id))
    return new_case

# Get a single case by ID
@app.get("/cases/{case_id}", response_model=Case)
async def read_case(case_id: int):
    case = cases_db.get(case_id)
    if case:
        return case
    else:
        raise HTTPException(status_code=404, detail="Case not found")

# Get all cases
@app.get("/cases/", response_model=List[dict])
async def read_cases():
    response = []
    for case in cases_db.values():
        response.append(get_response_json(case))
    return response

async def update_case_status(case_id: int):
    await asyncio.sleep(10)  # Wait for 10 seconds
    case = cases_db.get(case_id)
    if case:
        case.status = "processing"
        await asyncio.sleep(20)  # Wait for additional 20 seconds
        case.status = "complete"

# Load response JSON files
def load_response_json(filename: str, case: Case) -> dict:
    with open(filename, "r") as file:
        response = json.load(file)
    response["id"] = case.id
    response["created_at"] = case.created_at.isoformat()
    response["status"] = case.status
    return response

# Define a function to return the appropriate response JSON based on case status
def get_response_json(case: Case) -> dict:
    print("case status", case.status)
    if case.status == "submitted":
        return load_response_json("./assets/response-1.json", case)
    elif case.status == "processing":
        return load_response_json("./assets/response-2.json", case)
    elif case.status == "complete":
        return load_response_json("./assets/response-3.json", case)

# Endpoint to retrieve case details with dynamic response based on status
@app.get("/cases/{case_id}/details", response_model=dict)
async def get_case_details(case_id: int):
    print('running this case on case/case_id')
    case = cases_db.get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return get_response_json(case)
