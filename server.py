from fastapi import FastAPI, Depends
import models
import schemas
from database import engine, get_db
from sqlalchemy.orm import Session
from uuid import uuid4
app =  FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root(): 
    return {"Hello" : "World"}

@app.post("/register_agent")
def register_agent(agentCreate: schemas.AgentCreate, session: Session = Depends(get_db)): 
    agent = dict()
    agent["unique_id"] = uuid4()
    agent["status"] = True
    agent["job_status"] = "Idle"
    all_agents = session.query(models.Agent).filter(models.Agent.machine_name == agentCreate.machine_name).one()
    if all_agents: 
        return {"message": "Agent already registered exists in the database", "agent_id": all_agents.unique_id}
    else: 
        new_agent = models.Agent(status=agent["status"],job_status=agent["job_status"],unique_id=agent["unique_id"],machine_name=agentCreate.machine_name, stop_signal='')
        session.add(new_agent)
        new_update = models.AgentStatuses(status=agent["status"],job_status=agent["job_status"],unique_id=agent["unique_id"])
        session.add(new_update)
        session.commit()
        return {"message": "Agent registered successfully", "agent_id": agent['unique_id']}

@app.get('/get_agent_status/{agent_id}')
def get_agent_status(agent_id: str, session: Session = Depends(get_db)):
    agent = session.query(models.Agent).filter(models.Agent.unique_id == agent_id).one()
    return agent

@app.put("/update_status")
def update_agent_status(agentUpdate: schemas.AgentStatusUpdate,session: Session = Depends(get_db)): 
    
    # Adding a new row to agent statuses table
    new_update = models.AgentStatuses(**agentUpdate.model_dump())
    session.add(new_update)

    # Updating agent table
    agent = session.query(models.Agent).filter(models.Agent.unique_id == agentUpdate.unique_id).one()
    agent.status = agentUpdate.status
    agent.job_status = agentUpdate.job_status
    session.commit()

    session.refresh(new_update)
    return new_update

@app.get("/getallagents")
def get_all_agents(session: Session = Depends(get_db)): 
    agents = session.query(models.Agent).all()
    return agents


@app.put("/sendstopreqeusts/{agent_id}")
def sendstoprequests(agent_id: str, session: Session = Depends(get_db)): 
    agent = session.query(models.Agent).filter(models.Agent.unique_id == agent_id).one()
    agent.stop_signal = "stop"
    session.commit()
    session.refresh(agent)
    return {"message" : "Updated stop command", "agent": agent}

@app.put("/sendrunreqeusts/{agent_id}")
def sendstoprequests(agent_id: str, session: Session = Depends(get_db)): 
    agent = session.query(models.Agent).filter(models.Agent.unique_id == agent_id).one()
    agent.stop_signal = "run"
    session.commit()
    session.refresh(agent)
    return {"message" : "Updated stop command", "agent": agent}

    

    