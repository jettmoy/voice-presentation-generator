import os
from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel, Field
from typing import List
import base64

from .models import Instructions, Slides, generate_presentation_html, Message

from .agent import chat_agent

from icecream import ic

load_dotenv(dotenv_path=".env.local")


# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()



@app.post("/slides")
async def create_slides(request: Instructions):
    # Convert chat history into a structured format
    history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in request.history])
    
    # Combine history and new instructions into a single prompt
    if history_text:
        full_prompt = f"{history_text}\nuser: {request.instructions}"
    else:
        full_prompt = request.instructions

    # Send the formatted prompt to the chat agent
    response = await chat_agent.run(full_prompt)
    
    response.slides = generate_presentation_html(response.data.slides)

    # Convert slides to a readable text format
    # slides_text = "\n".join([f"{slide.id}. {slide.content}" for slide in response.data.slides])

    # Append the new messages to history
    request.history.append(Message(role="user", content=request.instructions))
    request.history.append(Message(role="assistant", content=response.slides))  # Store slides as string

    return {
        "response": response.slides,  
        "history": request.history  # Return updated history for follow-ups
    }



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
