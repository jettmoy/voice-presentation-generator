from __future__ import annotations

from loguru import logger
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai

from agents.functions import AssistantFnc


load_dotenv(dotenv_path=".env.local")


async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    run_multimodal_agent(ctx, participant)

    logger.info("agent started")

def run_multimodal_agent(ctx: JobContext, participant: rtc.RemoteParticipant):
    logger.info("starting multimodal agent")

    model = openai.realtime.RealtimeModel(
        instructions=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice and image. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
        ),
        modalities=["audio", "text"],
        voice="echo"
    )
    assistant = MultimodalAgent(model=model, fnc_ctx=AssistantFnc())
    assistant.start(ctx.room, participant)


    session = model.sessions[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content="""
            Please begin the interaction with the user in a manner consistent with your instructions.
            Mention that you are a voice assistant working for SDx, operating out of the Launch Factory, before 
            listening for the user's instructions.
            If the user asks for the weather, you should respond with the weather 
            by calling the get_weather function for the user's location.
            """
        )
    )
    session.response.create()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )