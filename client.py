import requests
import socket
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv()

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL")

def register_agent(): 
    machine_name = socket.gethostname()
    response = requests.post(f"{ORCHESTRATOR_URL}/register_agent",json={"machine_name": machine_name})
    if response.status_code == 200:
        print(f"Registered successfully")
        print(response.json().get("message"))
        return response.json().get("agent_id")
    else:
        print("Failed to register")
        return None
    
def get_agent_status(agent_id):
    agent_status = requests.get(f"{ORCHESTRATOR_URL}/get_agent_status/{agent_id}")
    return agent_status.json().get("stop_signal") 


def update_run_status(agent_id, run_status): 
    agent_status = requests.put(f"{ORCHESTRATOR_URL}/update_status",json={
    "unique_id": agent_id, 
    "status": 1,
    "job_status": run_status 
})

if __name__ == "__main__":
    response = register_agent()
    if response: 
        while(True): 
            agent_status = get_agent_status(response)
            
            if agent_status == 'stop': 
                # Add logic to stop all the bots
                print("Bot Stopped")
                update_run_status(response,"Idle")
                break
            elif agent_status == 'run': 
                print("Bot Running")
                update_run_status(response,"Processing")
                time.sleep(30)
    else:
        print("Server not found")
