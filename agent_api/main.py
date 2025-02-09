import os
from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel, Field
from typing import List
import base64

from .models import Instructions, Slides, generate_presentation_html

from .agent import chat_agent, call_o3_mini

from icecream import ic

load_dotenv(dotenv_path=".env.local")


# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()


@app.post("/slides")
async def create_slides(request: Instructions):
    # Call O3-mini model to generate slides
    response = await call_o3_mini(request.instructions)
    ic(response)
    return {"response": generate_presentation_html(response.slides)}

    # Check if there's an error in the response
    if "error" in response:
        return {"error": response["error"], "details": response.get("details", "")}

    # Generate HTML from the Slides model
    slides = generate_presentation_html(response["slides"].slides)
    ic(slides)

    return {"response": slides}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
