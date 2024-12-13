from pydantic import BaseModel

class AgentStatusUpdate(BaseModel): 
    unique_id: str 
    status: bool
    job_status: str

class AgentCreate(BaseModel): 
    machine_name: str