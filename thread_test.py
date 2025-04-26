import asyncio
import aiohttp
import json
import signal
import secrets

BORDER_ROUTER_URL = 'http://192.168.1.152:8081'  # Replace with your actual endpoint
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

"""
Functions to commission over Thread
"""

async def get_diagnostics():
    try:
        async with aiohttp.ClientSession() as thread_session:
            async with thread_session.get(f"{BORDER_ROUTER_URL}/diagnostics", headers=HEADERS) as response:
                # Check if the response status code is 200 (Successful operation)
                if response.status == 200:
                    data = await response.json()  # Assuming the content is JSON as per schema
                    print ("response:", json.dumps(data, indent=4))
                    return
                else:
                    print(f"Failed to retrieve diagnostics: {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None

async def enable_commissioner():
    try:
        async with aiohttp.ClientSession() as thread_session:
            async with thread_session.get(f"{BORDER_ROUTER_URL}/node/commissioner/state", headers=HEADERS) as response:
                if response.status == 200:
                    data = await response.json()
                    # check the data for 'active' or 'disabled'
                    if "active" in data:
                        print("Commissioner is active!")
                    elif "disabled" in data:
                        print("Commissioner is disabled. Sending request to enable it.")
                        async with thread_session.put(f"{BORDER_ROUTER_URL}/node/commissioner/state", headers=HEADERS, json="enable") as put_response:
                            if put_response.status in [200, 204]:
                                print("Commissioner successfully enabled.")
                            elif put_response.status == 409:
                                print("Cannot enable commissioner: Border router state not active.")
                            else:
                                error = await put_response.text()
                                print(f"Failed to enable commissioner. Status: {put_response.status}, Error: {error}")
                else:
                    error = await response.text()
                    print(f"Failed to enable commissioner. Status: {response.status}, Error: {error}")
    except aiohttp.ClientError as e:
        print("Request failed:", str(e))


async def get_active_joiners():
    try:
        async with aiohttp.ClientSession() as thread_session:
            async with thread_session.get(f"{BORDER_ROUTER_URL}/node/commissioner/joiner", headers=HEADERS) as response:
                if response.status == 200:
                    data = await response.json()  # Parse the response as JSON
                    print("Active Joiners List:", json.dumps(data, indent=4))  # Pretty print the joiner list
                    return data
                else:
                    error = await response.text()
                    print(f"Failed to fetch joiners. Status: {response.status}, Error: {error}")
                    return None
    except aiohttp.ClientError as e:
        print("Request failed:", str(e))
        return None

async def add_joiner(joiner_data):
    try:
        async with aiohttp.ClientSession() as thread_session:
            async with thread_session.post(f"{BORDER_ROUTER_URL}/node/commissioner/joiner", headers=HEADERS, json=joiner_data) as response:
                if response.status == 200:
                    data = await response.json()
                    print("Successfully added joiner:", json.dumps(data, indent=4))
                    return data
                elif response.status == 400:
                    print("Invalid request body. Please verify the joiner data.")
                elif response.status == 409:
                    print("Adding joiner rejected: Commissioner is not active.")
                elif response.status == 507:
                    print("Failed to add joiner: Commissioner cannot support additional joiners.")
                else:
                    error = await response.text()
                    print(f"Unexpected error. Status: {response.status}, Error: {error}")
                    return None
    except aiohttp.ClientError as e:
        print("Request failed:", str(e))
        return None
async def thread_menu():
    while True:
        print("\nThread Menu:")
        print("1. Get Thread diagnostics")
        print("2. Enable Commissioner")
        print("3. Add Joiner")
        print("4. Get active joiners")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Example: Call a function to get Thread diagnostics
            print("Fetching Thread diagnostics...")
            await get_diagnostics()
        elif choice == "2":
            # Example: Call a function to configure Thread settings
            print("Configuring Commissioner...")
            await enable_commissioner()
        elif choice == "3":
            # Example: Call a function to configure Thread settings
            eui64 = input("Enter the EUI64: ").strip()
            eui64= eui64.replace(":", "")
            pskd = input("Enter the Pre-shared key (Pskd): ").strip()
            # Form JOINER_DATA with timeout set to 5 minutes (300 seconds)
            joiner_data = {
                "Eui64": eui64,
                "Pskd": pskd,
                "Timeout": 300  # 5 minutes
            }
            print(f"Attempting to add joiner with data: {joiner_data}")
            await add_joiner(joiner_data)
        elif choice == "4":
            # Example: Call a function to configure Thread settings
            print("Get active joiners...")
            await get_active_joiners()
        elif choice == "5":
            # Exit Thread menu to return to main menu
            break
        else:
            print("Invalid choice, please try again.")

def run_main(): 
    try: 
        asyncio.run(thread_menu())
    except KeyboardInterrupt: 
        print("\nProgram terminated by user.") 

if __name__== '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Ensure signal handling 
    run_main()