# api_functions.py

import json
import asyncio

async def send_command(ws, command_data):
    try:
        command_data_str = json.dumps(command_data)
        print(f"Sending command: {command_data_str}")
        await ws.send_str(command_data_str)
        response = await ws.receive_str()
        return json.loads(response)
    except Exception as e:
        print(f"Error sending command: {e}")
        return None

async def set_wifi_credentials(ws, ssid, credentials):
    command_data = {
        "message_id": "1",
        "command": "set_wifi_credentials",
        "args": {
            "ssid": ssid,
            "credentials": credentials
        }
    }
    return await send_command(ws, command_data)

async def set_thread_dataset(ws, dataset):
    command_data = {
        "message_id": "2",
        "command": "set_thread_dataset",
        "args": {
            "dataset": dataset
        }
    }
    return await send_command(ws, command_data)

async def commission_with_code(ws, code, network_only=False):
    command_data = {
        "message_id": "3",
        "command": "commission_with_code",
        "args": {
            "code": code,
            "network_only": network_only
        }
    }
    return await send_command(ws, command_data)

async def open_commissioning_window(ws, node_id):
    command_data = {
        "message_id": "4",
        "command": "open_commissioning_window",
        "args": {
            "node_id": node_id
        }
    }
    return await send_command(ws, command_data)

async def get_nodes(ws):
    command_data = {
        "message_id": "5",
        "command": "get_nodes",
        "args": {}
    }
    return await send_command(ws, command_data)

async def get_node(ws, node_id):
    command_data = {
        "message_id": "6",
        "command": "get_node",
        "args": {
            "node_id": node_id
        }
    }
    return await send_command(ws, command_data)

async def start_listening(ws):
    command_data = {
        "message_id": "7",
        "command": "start_listening",
        "args": {}
    }
    return await send_command(ws, command_data)

async def read_attribute(ws, node_id, attribute_path):
    command_data = {
        "message_id": "8",
        "command": "read_attribute",
        "args": {
            "node_id": node_id,
            "attribute_path": attribute_path
        }
    }
    return await send_command(ws, command_data)

async def write_attribute(ws, node_id, attribute_path, value):
    command_data = {
        "message_id": "9",
        "command": "write_attribute",
        "args": {
            "node_id": node_id,
            "attribute_path": attribute_path,
            "value": value
        }
    }
    return await send_command(ws, command_data)

async def device_command(ws, endpoint_id, node_id, cluster_id, command_name, payload={}):
    command_data = {
        "message_id": "10",
        "command": "device_command",
        "args": {
            "endpoint_id": endpoint_id,
            "node_id": node_id,
            "cluster_id": cluster_id,
            "command_name": command_name,
            "payload": payload
        }
    }
    return await send_command(ws, command_data)

async def add_node(ws, node_id):
    command_data = {
        "message_id": "11",
        "command": "add_node",
        "args": {
            "node_id": node_id
        }
    }
    return await send_command(ws, command_data)

async def remove_node(ws, node_id):
    command_data = {
        "message_id": "12",
        "command": "remove_node",
        "args": {
            "node_id": node_id
        }
    }
    return await send_command(ws, command_data)

async def update_node(ws, node_id, new_info):
    command_data = {
        "message_id": "13",
        "command": "update_node",
        "args": {
            "node_id": node_id,
            "new_info": new_info
        }
    }
    return await send_command(ws, command_data)

async def subscribe_to_events(ws, node_id):
    command_data = {
        "message_id": "14",
        "command": "subscribe_to_events",
        "args": {
            "node_id": node_id
        }
    }
    return await send_command(ws, command_data)

async def unsubscribe_from_events(ws, node_id):
    command_data = {
        "message_id": "15",
        "command": "unsubscribe_from_events",
        "args": {
            "node_id": node_id
        }
    }
    return await send_command(ws, command_data)
