import asyncio
import aiohttp
import json
import signal
from matter_server.client.client import MatterClient
from chip.clusters import Objects as clusters

# Import the ability to turn objects into dictionaries, and vice-versa
from matter_server.common.helpers.util import dataclass_from_dict,dataclass_to_dict

from api_functions import (
    set_wifi_credentials,
    set_thread_dataset,
    commission_with_code,
    open_commissioning_window,
    get_nodes,
    get_node,
    start_listening,
    read_attribute,
    write_attribute,
    device_command,
    add_node,
    remove_node,
    update_node,
    subscribe_to_events,
    unsubscribe_from_events,
    set_default_fabric_label,
    commission_on_network,
    discover_commissionable_nodes,
    interview_node,
    ping_node,
    check_node_update,
    update_node
)

async def menu(ws):
    global running
    while running:
        print("\nMenu:")
        # print("0. Get server state")
        print("1. Set WiFi Credentials")
        print("2. Set Thread Dataset")
        print("3. Commission with Code (QR)")
        print("4. Commission with Code (Manual)")
        print("5. Open Commissioning Window")
        print("6. Get Nodes")
        print("7. Get Node")
        print("8. Start Listening")
        print("9. Read Attribute")
        print("10. Write Attribute")
        print("11. Device Command")
        print("12. Add Node")
        print("13. Remove Node")
        print("14. Update Node")
        print("15. Subscribe to Events")
        print("16. Unsubscribe from Events")
        print("99. Exit")

        choice = input("Enter your choice: ")
        # if choice == '0':
        #     response = await get_server_state(ws)
        if choice == '1':
            ssid = input("Enter SSID: ")
            credentials = input("Enter WiFi Password: ")
            response = await set_wifi_credentials(ws, ssid, credentials)
        elif choice == '2':
            dataset = input("Enter Thread Dataset: ")
            response = await set_thread_dataset(ws, dataset)
        elif choice == '3':
            code = input("Enter Matter QR Code: ")
            response = await commission_with_code(ws, code)
        elif choice == '4':
            code = input("Enter Manual Pairing Code: ")
            response = await commission_with_code(ws, code, network_only=True)
        elif choice == '5':
            node_id = int(input("Enter Node ID: "))
            response = await open_commissioning_window(ws, node_id)
        elif choice == '6':
            response = await get_nodes(ws)
            result = response.get('result', [])
            if not result:
                print("No result data available.")
                return
            print(f"Number of nodes in result: {len(result)}")

            # Process each node in the result
            for node_idx, response in enumerate(result, start=1):
                print(f"\nProcessing Node {node_idx}:")
                node_id = response.get('node_id', 'Unknown')
                date_commissioned = response.get('date_commissioned', 'Unknown')
                last_interview = response.get('last_interview', 'Unknown')
                interview_version = response.get('interview_version', 'Unknown')
                available = response.get('available', 'Unknown')
                is_bridge = response.get('is_bridge', 'Unknown')

                print(f"  Node ID: {node_id}")
                print(f"  Date Commissioned: {date_commissioned}")
                print(f"  Last Interview: {last_interview}")
                print(f"  Interview Version: {interview_version}")
                print(f"  Available: {available}")
                print(f"  Is Bridge: {is_bridge}")


                attributes = response.get('attributes', {})
                if not attributes:
                    print("  No attributes available.")
                    continue

                print(f"  Number of attribute clusters: {len(attributes)}")


        elif choice == '7':
            node_id = int(input("Enter Node ID: "))
            response = await get_node(ws, node_id)
        elif choice == '8':
            response = await start_listening(ws)
        elif choice == '9':
            node_id = int(input("Enter Node ID: "))
            attribute_path = input("Enter Attribute Path: ")
            response = await read_attribute(ws, node_id, attribute_path)
        elif choice == '10':
            node_id = int(input("Enter Node ID: "))
            attribute_path = input("Enter Attribute Path: ")
            value = input("Enter Value: ")
            response = await write_attribute(ws, node_id, attribute_path, value)
        elif choice == '11':
            endpoint_id = int(input("Enter Endpoint ID: "))
            node_id = int(input("Enter Node ID: "))
            cluster_id = int(input("Enter Cluster ID: "))
            command_name = input("Enter Command Name: ")
            payload = input("Enter Payload (JSON format): ")
            response = await device_command(ws, endpoint_id, node_id, cluster_id, command_name, json.loads(payload))
        elif choice == '12':
            node_id = int(input("Enter Node ID: "))
            response = await add_node(ws, node_id)
        elif choice == '13':
            node_id = int(input("Enter Node ID: "))
            response = await remove_node(ws, node_id)
        elif choice == '14':
            node_id = int(input("Enter Node ID: "))
            new_info = input("Enter New Info (JSON format): ")
            response = await update_node(ws, node_id, json.loads(new_info))
        elif choice == '15':
            node_id = int(input("Enter Node ID: "))
            response = await subscribe_to_events(ws, node_id)
        elif choice == '16':
            node_id = int(input("Enter Node ID: "))
            response = await unsubscribe_from_events(ws, node_id)
        elif choice == '99':
            running = False
            break
        else:
            print("Invalid choice. Please try again.")
            continue

#        if response:
#            print(f"Response received: {json.dumps(response, indent=4)}")

async def run_matter():
    # WebSocket URL of the Matter server 
    matter_server_url = "ws://192.168.1.102:5580/ws" 

    async with aiohttp.ClientSession() as session:
        async with MatterClient(matter_server_url, session) as client:
            # start listening
            asyncio.create_task(client.start_listening())
            # allow the client to initialize
            await asyncio.sleep(10)
            # dump full node info on random (available) node
            for node in client.get_nodes():
                if not node.available:
                    continue
                print()
                print(node)
                res = await client.node_diagnostics(node.node_id)
                print(res)
                print()
                break

# Run the main function 
def run_main(): 
    try: 
        asyncio.run(run_matter()) 
    except KeyboardInterrupt: 
        print("\nProgram terminated by user.") 

if __name__ == '__main__': 
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Ensure signal handling 
    run_main()