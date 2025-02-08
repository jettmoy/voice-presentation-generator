import os
from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel, Field
from typing import List
import base64

from .types import Instructions, Slides, generate_presentation_html

from .agent import chat_agent

from icecream import ic

load_dotenv(dotenv_path="../.env.local")


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()



@app.post("/slides")
async def create_slides(request: Instructions):
    response = await chat_agent.run(request.instructions)
    ic(response)
    response.slides = generate_presentation_html(response)
    ic(response)
    return {"response": response.slides}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
