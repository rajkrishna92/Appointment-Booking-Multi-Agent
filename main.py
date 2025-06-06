from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from agent import supervisor
from langchain_core.messages import HumanMessage
from utils.helper import pretty_print_messages

app = FastAPI()

# Define Pydantic model to accept request body
class UserQuery(BaseModel):
    email: str
    messages: str

@app.post("/execute")
async def execute_agent(user_input: UserQuery):

    input = {
        "message":HumanMessage(content=user_input.messages)
    }

    response = supervisor.invoke(input, config={'configurable': {'thread_id': user_input.email}})
    return response["messages"][-1].content

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
