from __future__ import annotations

from uuid import uuid4
from typing import List, Optional, Union
from pydantic import BaseModel, ValidationError

from pydantic_ai import Agent
from typing_extensions import TypedDict

from datetime import datetime
from .models import Slides, Instructions

import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from typing import Dict, Any

# Load environment variables from .env.local
load_dotenv('.env.local')

SYSTEM_PROMPT = """
You are a helpful assistant that generates informative slides from instructions
about a topic. Think step by step as an experienced instructor would to 
break a topic into clear and concise slides that build progressively.
If there are detail slides needed, create them as children of the main slide
with subection numbering; e.g 3.1, 3.2, 3.3 etc. 
"""

async def call_o3_mini(prompt: str, max_tokens: int = 300) -> Dict[str, Any]:
    """
    Call OpenAI's O3-mini model with a given prompt.
    
    Args:
        prompt (str): The input prompt for the model
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 300.
    
    Returns:
        Dict containing slide data or error information
    """
    try:
        # Initialize OpenAI client with API key from environment variable
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        )
        
        # Prepare the messages for the chat completion
        messages = [
            {
                "role": "system", 
                "content": """You are an expert presentation generator. 
                Generate a JSON response with the following structure:
                {
                    "title": "Presentation Title",
                    "slides": [
                        {
                            "title": "Slide Title",
                            "content": "Slide Content",
                            "bullets": ["Key Point 1", "Key Point 2"]
                        }
                    ]
                }
                Ensure the JSON is valid and the content is informative."""
            },
            {"role": "user", "content": prompt}
        ]
        
        # Make API call to O3-mini model using beta parsing
        response = client.beta.chat.completions.parse(
            model="o3-mini",  # Specify the O3-mini model
            messages=messages,
            # max_tokens=max_tokens,
            # temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Extract the JSON response
        response_text = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        slides_data = json.loads(response_text)
        
        return {
            "data": slides_data,
            "slides": slides_data  # Maintain compatibility with existing code
        }
    
    except json.JSONDecodeError as je:
        print(f"JSON Parsing Error: {je}")
        return {
            "error": "Failed to parse model response",
            "details": str(je)
        }
    
    except Exception as e:
        print(f"Error calling O3-mini model: {e}")
        return {
            "error": "An error occurred while generating the presentation",
            "details": str(e)
        }

# Example usage
if __name__ == "__main__":
    test_prompt = "Generate a brief introduction for a presentation about AI technology."
    result = call_o3_mini(test_prompt)
    print(result)

chat_agent = Agent(
    model="openai:gpt-4o-mini",
    result_type=Slides,
    # deps_type=WorkflowDeps,
    system_prompt=SYSTEM_PROMPT,
    retries=3
)
