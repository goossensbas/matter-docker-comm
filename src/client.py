import asyncio
import aiohttp
import json
from matter_server.client.client import MatterClient
from chip.clusters import Objects as clusters
from api_functions import set_thread_dataset, get_nodes

# Import the ability to turn objects into dictionaries, and vice-versa
from matter_server.common.helpers.util import dataclass_from_dict,dataclass_to_dict

async def main():
    # WebSocket URL of the Matter server 
    matter_server_url = "ws://192.168.1.102:5580/ws" 

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(matter_server_url) as ws:

            # Example: Set Thread credentials (Thread dataset)
            dataset = "000300001a4a0300000b35060004001fffe00208687d5e1c30e8c3710708fdde6c9442e56b39051058278552405e0271edec681f01e6f82a030f4f70656e5468726561642d3532313601025216041065b9b48b2ae605b7a4bdc984b40061ce0c0402a0f7f80e080000000000010000"
            response = await set_thread_dataset(ws, dataset)
            if response:
                print("Set Thread Dataset Response:", response)

            # Example: Get Nodes
            response = await get_nodes(ws)
            if response:
                print("Get Nodes Response:", response)

# Run the main function
asyncio.run(main())
