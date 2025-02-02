import asyncio
import aiohttp
import json
import signal
from matter_server.client.client import MatterClient
from chip.clusters import Objects as clusters

# Import the ability to turn objects into dictionaries, and vice-versa
from matter_server.common.helpers.util import dataclass_from_dict,dataclass_to_dict

async def set_wifi_credentials(client):
    ssid = input("Enter Wi-Fi SSID: ") 
    password = input("Enter Wi-Fi Password: ") 
    wifi_credentials = { "ssid": ssid, "password": password } 
    response = await client.set_wifi_credentials(wifi_credentials) 
    print("Wi-Fi credentials set response:") 
    print(json.dumps(response, indent=4))


async def set_thread_dataset(client):
    thread_dataset = input("Enter Thread TLV dataset: ")
    response = await client.set_thread_operational_dataset(thread_dataset)
    print("Thread dataset set response:")
    print(json.dumps(response, indent=4))


async def view_server_info(client):
    server_info = client.server_info 
    print("Server Status:") 
    print(json.dumps(dataclass_to_dict(server_info), indent=4))


async def get_nodes(client):
    nodes = client.get_nodes()
    print(f"Found {len(nodes)} nodes.")
    for node in nodes:
        print(f"Checking node: {node.node_id}, available: {node.available}")
        if not node.available:
            continue
        print(f"Node found: {node}")
        res = await client.node_diagnostics(node.node_id)
        print(f"Node diagnostics: {res}")
        
        break


async def get_node_clusters_detailed(client):
    node_id = int(input("Enter the node ID to view its endpoints and clusters: "))
    node = client.get_node(node_id)
    print(f"node retrieved: {node}")
     # Print the attributes of the node object 
     # print(f"Node attributes: {dir(node)}")
    
    if node:
        print(f"Node ID: {node_id} Endpoints:")
         # Print the endpoints attribute 
        print(f"Endpoints: {node.endpoints}")

        if node.endpoints:
            for endpoint_id, endpoint in node.endpoints.items():
                print(f"Endpoint ID: {endpoint_id}")
                print(f"Cluster keys: {endpoint.clusters.keys()}")
                print(f"Clusters: {endpoint.clusters}")
                for cluster_id, cluster in endpoint.clusters.items(): 
                    cluster_info = decode_cluster(cluster) 
                    print(f" Cluster ID: {cluster_id} - {cluster_info}")
    else: 
        print(f"Node with ID {node_id} not found.")

async def get_node_clusters(client):
    node_id = int(input("Enter the node ID to view its endpoints and clusters: "))
    node = client.get_node(node_id)
    print(f"node retrieved: {node}")
     # Print the attributes of the node object 
     # print(f"Node attributes: {dir(node)}")
    
    if node:
        for endpoint_id, endpoint in node.endpoints.items():
            print(f"Endpoint ID: {endpoint_id}") 
            print(f"Endpoint Object: {endpoint}") 
            # Access attributes of MatterEndpoint object 
            for cluster_id in endpoint.clusters: 
                print(f" Cluster ID: {cluster_id}")
            print("=" * 40)
    else: 
        print(f"Node with ID {node_id} not found.")

def decode_cluster(cluster):
    # Extract and format cluster attributes into a readable string
    attributes = vars(cluster)
    formatted_attributes = [f"{key}: {value}" for key, value in attributes.items()]
    return ", ".join(formatted_attributes)

async def send_command_to_node(client, node_id, endpoint_id, command): 
    node = client.get_node(node_id) 
    if node: 
        endpoint = node.endpoints.get(endpoint_id) 
        if endpoint: 
            cluster = endpoint.clusters.get(command.cluster_id) 
            if cluster:
                await client.send_device_command(node_id, endpoint_id, command) 
                print(f"Command {command} sent to node {node_id}, endpoint {endpoint_id}, cluster {command.cluster_id}") 
            else: 
                print(f"Cluster {command.cluster_id} not found in endpoint {endpoint_id}") 
        else: print(f"Endpoint {endpoint_id} not found in node {node_id}") 
    else: print(f"Node {node_id} not found")

async def commission_new_node(client):
    print("Commission a device using a QR Code or Manual Pairing Code.")
    setup_code = input("Enter the setup code for the new node: ")
    response = await client.commission_with_code(setup_code)
    print("Commissioning response:") 
    print(response.__dict__)


async def menu(client):
    while True:
        print("\nMenu:")
        print("1. Set Wi-Fi credentials")
        print("2. Set Thread dataset")
        print("3. View server info")
        print("4. Get nodes")
        print("5. Commission new node")
        print("6. Get node clusters") 
        print("7. Toggle light")
        print("8. Bind light and switch")
        print("9. Exit")


        choice = input("Choose an option: ")

        if choice == '1':
            await set_wifi_credentials(client)
        elif choice == '2':
            await set_thread_dataset(client)
        elif choice == '3':
            await view_server_info(client)
        elif choice == '4':
            await get_nodes(client)
        elif choice == '5':
            await commission_new_node(client)
        elif choice == '6':
            await get_node_clusters(client)
        elif choice == '7':
            node_id = int(input("Enter the node ID to send the command to: ")) 
            endpoint_id = int(input("Enter the endpoint ID of the light: "))
            command = clusters.OnOff.Commands.Toggle()
            print(command)
            await send_command_to_node(client, node_id, endpoint_id, command)
        elif choice == '8': 
            await bind_light_switch(client)
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")

async def bind_light_switch(client): 
    light_node_id = int(input("Enter the light node ID: "))
    light_endpoint_id = int(input("Enter the light endpoint ID: ")) 
    switch_node_id = int(input("Enter the switch node ID: "))
    switch_endpoint_id = int(input("Enter the switch endpoint ID: ")) 

    # Create an ACL for the switch on the light device 
    acl_entry = [{ 
        'fabricIndex': 1, # Assuming fabric index 1
        'privilege': 5,
        'authMode': 2,
        'subjects': [112233],
        'targets': None},
        {
        'fabricIndex': 1, # Assuming fabric index 1
        'privilege': 5,
        'authMode': 2,
        'subjects': [switch_node_id, 112233],
        'targets': [
            {"cluster": 6, "endpoint": light_endpoint_id, "deviceType": None},
            {"cluster": 8, "endpoint": light_endpoint_id, "deviceType": None}
        ]}   
    ] 

    # read the AccessControlList on endpoint 0, cluster 31
    res = await client.read_attribute(light_node_id, "0/31/0")
    print(f"{res}")
    # write the AccessControlList on endpoint 0, cluster 31
    res = await client.write_attribute(light_node_id, "0/31/0", acl_entry)
    print(f"{res}")
    # read the updated AccessControlList on endpoint 0, cluster 31
    res = await client.read_attribute(light_node_id, "0/31/0")
    print(f"{res}")

    # write Unicast binding to light switch 
    binding_entry = [
        {
        'fabricIndex': 1, # Assuming fabric index 1
        'node': light_node_id,
        'endpoint': light_endpoint_id,
        'cluster': 6,
        },
        {
        'fabricIndex': 1, # Assuming fabric index 1
        'node': light_node_id,
        'endpoint': light_endpoint_id,
        'cluster': 8,
        }
    ]
    # res = await client.read_attribute(switch_node_id, f"{switch_endpoint_id}/30/0")
    # print(f"{res}")
    res = await client.write_attribute(switch_node_id,f"{switch_endpoint_id}/30/0", binding_entry)
    print(f"{res}")



async def run_matter():
    # WebSocket URL of the Matter server 
    matter_server_url = "ws://192.168.1.153:5580/ws" 

    async with aiohttp.ClientSession() as session:
        try:
            async with MatterClient(matter_server_url, session) as client:
                try:
                    # start listening
                    print("starting to listen")
                    asyncio.create_task(client.start_listening())
                    # allow the client to initialize
                    await asyncio.sleep(10)
                    print("Matter client initialised.")

                    # Retrieve server status 
                    server_info = client.server_info 
                    print("Server Status:") 
                    print(json.dumps(dataclass_to_dict(server_info), indent=4))

                    if not server_info.wifi_credentials_set: 
                        user_input = input("Wi-Fi credentials are not set. Do you want to set them now? (y/n): ") 
                        if user_input.lower() == 'y': 
                            await set_wifi_credentials(client)
                    if not server_info.thread_credentials_set: 
                        user_input = input("Thread operational dataset is not set. Do you want to set it now? (y/n): ") 
                        if user_input.lower() == 'y': 
                            await set_thread_dataset(client)
                    # Show menu for further actions
                    await menu(client)
                except Exception as e:
                    print(f"Error during Matter client operation: {e}")
                finally: 
                    await client.disconnect() 
                    print("Disconnected from Matter server.")
        except Exception as e: 
            print(f"An error has occured: {e}")


# Run the main function 
def run_main(): 
    try: 
        asyncio.run(run_matter()) 
    except KeyboardInterrupt: 
        print("\nProgram terminated by user.") 

if __name__ == '__main__': 
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Ensure signal handling 
    run_main()