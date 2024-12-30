import asyncio
import aiohttp
import json
from matter_server.client.client import MatterClient
from chip.clusters import Objects as clusters

# Import the ability to turn objects into dictionaries, and vice-versa
from matter_server.common.helpers.util import dataclass_from_dict,dataclass_to_dict

async def main():
    # WebSocket URL of the Matter server 
    matter_server_url = "ws://192.168.1.102:5580/ws"    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(matter_server_url) as ws:
            
            # Example: Set Thread credentials (Thread dataset)
            """
            command_data = {
                "message_id": "1",
                "command": "set_thread_dataset", 
                "args": {
                    "dataset": "000300001a4a0300000b35060004001fffe00208687d5e1c30e8c3710708fdde6c9442e56b39051058278552405e0271edec681f01e6f82a030f4f70656e5468726561642d3532313601025216041065b9b48b2ae605b7a4bdc984b40061ce0c0402a0f7f80e080000000000010000"
                    }
                }

            """
            # Example: Get Nodes (simple command)
            command_data = {
                "message_id": "1",  # Ensure message_id is a string if needed
                "command": "get_nodes",  # Simple command as string
                "args": {}
            }

            command_data_str = json.dumps(command_data)
            print(f"Type of command_data: {type(command_data_str)}")
            print(f"Command Data: {command_data_str}")  # Log command data to debug

            await ws.send_str(command_data_str)
            response = await ws.receive_str()
            print("Response:", response)


# Run the main function
asyncio.run(main())
