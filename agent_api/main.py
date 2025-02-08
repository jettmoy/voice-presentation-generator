import os
from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel
import base64



load_dotenv(dotenv_path="../.env.local")


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()


class Question(BaseModel):
    question: str


@app.post("/image-info")
# @app.get("/image-info/{id}", response_class=HTMLResponse)
async def get_image(request: Question):
    with open("/Users/ecology/Downloads/PXL_20241026_201845590.jpeg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": request.question},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"},
                        },
                    ],
                }
            ],
            max_tokens=4096,
        )
    return {"response": response}


# @app.post("/upload")
# async def


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
