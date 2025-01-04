import asyncio
import aiohttp
import json
import signal
from matter_server.client.client import MatterClient
from chip.clusters import Objects as clusters

# Import the ability to turn objects into dictionaries, and vice-versa
from matter_server.common.helpers.util import dataclass_from_dict,dataclass_to_dict

running = True

async def send_command(ws, command_data):
    try:
        command_data_str = json.dumps(command_data)
        print(f"Sending command: {command_data_str}")
        await ws.send_str(command_data_str)
        response = await ws.receive_str()
        response_data = json.loads(response)
        print(f"Response received: {json.dumps(response_data, indent=4)}")
        return json.loads(response)
    except Exception as e:
        print(f"Error sending command: {e}")
        return None

async def get_nodes(ws):
    command_data = {
        "message_id": "5",
        "command": "get_nodes",
        "args": {}
    }
    return await send_command(ws, command_data)

async def main():
    global running
    # WebSocket URL of the Matter server 
    matter_server_url = "ws://192.168.1.199:5580/ws" 

    async with aiohttp.ClientSession() as session:
        while running:
            try:
                async with session.ws_connect(matter_server_url) as ws:
                    # Check server state before starting the menu
                    state_response = await get_nodes(ws)
                    if state_response:
                        print("Server State:")
                        print(json.dumps(state_response, indent=4))
            except aiohttp.ClientConnectionError: 
                if not running:
                    break
                print("Connection lost, attempting to reconnect...") 
                await asyncio.sleep(5) # Wait for 5 seconds before reconnecting 
            except Exception as e: 
                if not running:
                    break
                print(f"An error occurred: {e}") 
                await asyncio.sleep(5) # Wait for 5 seconds before reconnecting

# Run the main function 
def run_main(): 
    global running 
    try: 
        asyncio.run(main()) 
    except KeyboardInterrupt: 
        running = False 
        print("\nProgram terminated by user.") 

if __name__ == '__main__': 
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Ensure signal handling 
    run_main()