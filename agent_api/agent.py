from __future__ import annotations

from uuid import uuid4
from typing import List, Optional, Union
from pydantic import BaseModel, ValidationError

from pydantic_ai import Agent, RunContext, Tool, ModelRetry
from typing_extensions import TypedDict

from datetime import datetime
from .types import Slides, Instructions



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
