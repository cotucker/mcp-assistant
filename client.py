import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import json
from typing import Any
import enum
from google.protobuf.message import Message

from anthropic import Anthropic
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, config
from asr import asr
from tts_google import generate
from input import get_query
import os, logging, json, simpleaudio as sa

load_dotenv()
logging.basicConfig(level=logging.INFO)

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.gemini = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""

        response = await self.session.list_tools()

        tools = [
            types.Tool(
                function_declarations=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            k: v
                            for k, v in tool.inputSchema.items()
                            if k not in ["additionalProperties", "$schema"]
                        },
                    }
                ]
            )
            for tool in response.tools
        ]

        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=query)]
            ),
        ]

        config = types.GenerateContentConfig(tools = tools)
        response = await self.gemini.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config
        )

        response = response.candidates[0]

        final_text = ''

        content = response.content
        for part in content.parts:
            if part.function_call:
                function_call_object = part.function_call
                tool_name = function_call_object.name
                tool_args = function_call_object.args
                if not isinstance(tool_args, dict):
                    tool_args = dict(tool_args)
                result = await self.session.call_tool(
                    name=tool_name,
                    arguments=tool_args,
                )
                logging.info(f'[Calling tool {tool_name} with args {tool_args}]\n')
                final_text += result.structuredContent['result']

            elif part.text:
                final_text += part.text

        return final_text

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = asr()
                # query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)


                # generate(response)
                # wave_obj = sa.WaveObject.from_wave_file("audio\speech_0.wav")
                # play_obj = wave_obj.play()
                # play_obj.wait_done()


                    
            except Exception as e:
                import traceback
                error_info = traceback.format_exc()
                print(f"\nError (Client): {str(e)}")
                print(f"\nError Details:\n{error_info}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())