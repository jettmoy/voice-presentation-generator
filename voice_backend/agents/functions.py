import aiohttp
from loguru import logger
from typing import Annotated
import json

from livekit.agents import llm
from livekit.rtc import Room


class AssistantFnc(llm.FunctionContext):
    def __init__(self, room: Room, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room

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
    async def create_slides(
        self,
        # by using the Annotated type, arg description and type are available to the LLM
        instructions: Annotated[
            str,
            llm.TypeInfo(
                description="Instructions on how to create slideshow presentation on a topic."
            ),
        ],
    ):
        """Instructions on how to create or modify slides on a topic."""
        logger.info("manipulating slides info")
        url = f"http://localhost:8000/slides"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json={"instructions": instructions}
            ) as response:
                if response.status == 200:
                    response = await response.json()
                    slides_data = response.get("response")
                    # response from the function call is returned to the LLM
                    # as a tool response. The LLM's response will include this data
                    print("slides_data: ", slides_data)
                    try:
                        participants = self.room.remote_participants
                        for participant in participants:
                            print(participant)
                            # Perform the RPC to request the user's location from the frontend
                            print("Sending RPC to ", participant)
                            response = await self.room.local_participant.perform_rpc(
                                destination_identity=participant,
                                method="navigate_to_slides",
                                payload=json.dumps({"slides": slides_data}),
                                # response_timeout=10.0 if high_accuracy else 5.0,
                                response_timeout=5.0,
                            )
                            print("sent RPC to ", participant, response)
                        # return response
                    except Exception as e:
                        print("Error sending RPC:", e)
                        # return f"Unable to retrieve user location: {str(e)}"
                    return {"slides": slides_data}
                else:
                    raise f"Failed  status code: {response.status}"
