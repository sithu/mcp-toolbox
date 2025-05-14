import asyncio
import os

from llama_index.core.agent.workflow import AgentWorkflow

from llama_index.core.workflow import Context

# TODO(developer): replace this with another import if needed

from llama_index.llms.google_genai import GoogleGenAI

# from llama_index.llms.anthropic import Anthropic

from toolbox_llamaindex import ToolboxClient

prompt = """
  You're a helpful hotel assistant. You handle hotel searching, booking and
  cancellations. When the user searches for a hotel, mention it's name, id,
  location and price tier. Always mention hotel ids while performing any
  searches. This is very important for any operations. For any bookings or
  cancellations, please provide the appropriate confirmation. Be sure to
  update checkin or checkout dates if mentioned by the user.
  Don't ask for confirmations from the user.
"""

queries = [
    "Find hotels in Basel with Basel in it's name.",
    "Can you book the Hilton Basel for me?",
    "Oh wait, this is too expensive. Please cancel it and book the Hyatt Regency instead.",
    "My check in dates would be from April 10, 2024 to April 19, 2024.",
]

async def run_application():
    # TODO(developer): replace this with another model if needed
    # llm = GoogleGenAI(
    #     model="gemini-1.5-pro",
    #     vertexai_config={"project": "project-id", "location": "us-central1"},
    # )
    llm = GoogleGenAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-1.5-pro",
    )
    # llm = Anthropic(
    #   model="claude-3-7-sonnet-latest",
    #   api_key=os.getenv("ANTHROPIC_API_KEY")
    # )

    # Load the tools from the Toolbox server
    client = ToolboxClient("http://127.0.0.1:5000")
    tools = await client.aload_toolset()

    agent = AgentWorkflow.from_tools_or_functions(
        tools,
        llm=llm,
        system_prompt=prompt,
    )
    ctx = Context(agent)
    for query in queries:
         response = await agent.run(user_msg=query, ctx=ctx)
         print(f"---- {query} ----")
         print(str(response))

asyncio.run(run_application())
