import aiohttp
from loguru import logger
from typing import Annotated

from livekit.agents import llm

class AssistantFnc(llm.FunctionContext):
    # the llm.ai_callable decorator marks this function as a tool available to the LLM
    # by default, it'll use the docstring as the function's description
    @llm.ai_callable()
    async def analyze_calendar(
        self,
        # by using the Annotated type, arg description and type are available to the LLM
        question: Annotated[
            str, llm.TypeInfo(description="A particular question about the calendar")
        ],
    ):
        """Called when the user asks about what's on the calendar. This function will return information about the calendar."""
        logger.info("getting calendar info")
        url = f"http://localhost:8000/image-info"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"question": question}) as response:
                if response.status == 200:
                    cal_data = await response.text()
                    # response from the function call is returned to the LLM
                    # as a tool response. The LLM's response will include this data
                    return f"The answer to the question is {cal_data}."
                else:
                    raise f"Failed to get cal data, status code: {response.status}"

    @llm.ai_callable()
    async def modify_slides(
        self,
        # by using the Annotated type, arg description and type are available to the LLM
        instructions: Annotated[
            str, llm.TypeInfo(description="Instructions on how to create or modify slides on a topic.")
        ],
    ):
        """Instructions on how to create or modify slides on a topic."""
        logger.info("manipulating slides info")
        url = f"http://localhost:8000/slides"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"instructions": instructions}) as response:
                if response.status == 200:
                    slides_data = await response.text()
                    # response from the function call is returned to the LLM
                    # as a tool response. The LLM's response will include this data
                    return {"slides": slides_data}
                else:
                    raise f"Failed  status code: {response.status}"