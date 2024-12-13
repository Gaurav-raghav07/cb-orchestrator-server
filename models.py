from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean

class Agent(Base): 
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    unique_id = Column(String(100),nullable=False)
    status = Column(Boolean, nullable=False)
    job_status = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    machine_name= Column(String(100),nullable=False)
    stop_signal = Column(String(30),nullable=False,default='')

class AgentStatuses(Base): 
    __tablename__ = "agentstatuses"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String(100),nullable=False)
    status = Column(Boolean, nullable=False)
    job_status = Column(String(100), nullable=False)
    last_connected = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)