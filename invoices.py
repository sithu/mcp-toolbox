import asyncio
import os

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context

# TODO(developer): replace this with another import if needed
from llama_index.llms.google_genai import GoogleGenAI
# from llama_index.llms.anthropic import Anthropic

from toolbox_llamaindex import ToolboxClient

prompt = """
  You're a helpful invoice management assistant. You handle listing invoices, 
  creating new invoices, updating invoice details, and marking invoices as paid.
  
  When listing invoices, always include the invoice id, hotel id, guest name, 
  amount, and payment status. Always mention invoice ids while performing any
  operations. This is very important for any operations.
  
  You have the following capabilities:
  1. List all invoices or filter by hotel_id
  2. Create new invoices for hotels with guest name and amount
  3. Mark invoices as paid or unpaid by invoice_id
  
  For filtering unpaid invoices, use the list-invoices tool and then filter the results.
  
  For any invoice creation or updates, please provide appropriate confirmation.
  Be professional and concise in your responses.
  Don't ask for confirmations from the user.
"""

queries = [
    "List all invoices in the system.",
    "List invoices for hotel H123.",
    "Create a new invoice for hotel H456 for guest Michael Brown with amount $299.99.",
    "Mark invoice #1 as paid.",
    "Show me all unpaid invoices.",
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
    tools = await client.aload_toolset("my-toolset")

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