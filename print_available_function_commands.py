import asyncio
import aiohttp
import json
import signal
from matter_server.client.client import MatterClient
from chip.clusters import Objects as clusters

# Import the ability to turn objects into dictionaries, and vice-versa
from matter_server.common.helpers.util import dataclass_from_dict,dataclass_to_dict

async def main():
    # Define the WebSocket server URL
    matter_server_url = "ws://localhost:5580/ws" 

    # Create an aiohttp session
    async with aiohttp.ClientSession() as aiohttp_session:
        # Create a Matter client instance with the required arguments
        client = MatterClient(matter_server_url, aiohttp_session)
        # Connect to the Matter server
        await client.connect()
        print("Connected to Matter server.")

    try: 
        # Print available methods and attributes 
        print(dir(client)) 
    except Exception as e: 
        print(f"An error occurred: {e}") 
    finally: 
        await client.disconnect() 
        print("Disconnected from Matter server.") 
        
# Run the main function 
asyncio.run(main())

