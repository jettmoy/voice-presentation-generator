from __future__ import annotations

from uuid import uuid4
from typing import List, Optional, Union
from pydantic import BaseModel, ValidationError

from pydantic_ai import Agent
from typing_extensions import TypedDict

from datetime import datetime
from .models import Slides, Instructions, Message



SYSTEM_PROMPT = """
You are a helpful assistant that generates informative slides from instructions
about a topic. Think step by step as an experienced instructor would to 
break a topic into clear and concise slides that build progressively.
If there are detail slides needed, create them as children of the main slide
with subection numbering; e.g 3.1, 3.2, 3.3 etc. 
"""



chat_agent = Agent(
    model="openai:o3-mini",
    result_type=Slides,
    # deps_type=WorkflowDeps,
    system_prompt=SYSTEM_PROMPT,
    retries=3
)

async def chat_with_agent(instructions: str, history: List[Message]):
    """
    Calls the agent while maintaining chat history.
    """
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": instructions})

    response = await chat_agent.run(instructions, history=messages)

    return response
