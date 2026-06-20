

import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import asyncio
async def main():
    #client will be interacting with servers
    client=MultiServerMCPClient({

        "math":{
            "command": sys.executable,
            "args":["mathserver.py"],
            "transport":"stdio",

        },
        "weather":{
            "url":"http://localhost:8000/mcp",
            "transport":"streamable_http",
        },
    })


    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
    tools=await client.get_tools()
    model=ChatGroq(model="llama-3.3-70b-versatile")
    agent=create_react_agent(
        model, tools
    )

    math_response=await agent.ainvoke(
        {"messages":[{"role":"user","content":"what is 2 x 4?"}]}
    )
    print("Math result:",math_response["messages"][-1].content)
    
    weather_response=await agent.ainvoke(
        {"messages":[{"role":"user","content":"what is weather in Shimla?"}]}
    )
    print("Weather result:",weather_response["messages"][-1].content)


asyncio.run(main())

