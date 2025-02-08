from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    question: str

class Instructions(BaseModel):
    instructions: str = Field(description="The instructions for the LLM on how to make slides")

class SlideContent(BaseModel):
    heading: str = Field(description="Heading of the slide")
    body: str = Field(description="Text of the slide")


class Slide(BaseModel):
    id: str = Field(description="The id of the slide")
    content: SlideContent = Field(description="The content of the slide")
    children: Optional[List[SlideContent]] = Field(description="The children slides, e.g 3, 3.1, 3.2")

class Slides(BaseModel):
    slides: List[Slide] = Field(description="The slides generated by the LLM")



def generate_slide_html(content: SlideContent) -> str:
    """Recursively generate HTML for a slide and its children."""
    html = ""
    if content.heading:
        html += f"<h1>{content.heading}</h1>"
    if content.body:
        html += f"<p>{content.body}</p>"

    return html

def generate_presentation_html(slides: List[Slide]) -> str:
    """Generate HTML for all slides in the presentation."""
    html = ""
    for slide in slides:
        html += f"<section>"
        html += generate_slide_html(slide.content)
        if slide.children:
            for child in slide.children:
                html += "<section>"
                html += generate_slide_html(SlideContent(heading=child.heading, body=child.body))
                html += "</section>"
        html += "</section>"
    return html