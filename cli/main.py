import getpass
import json
from os import getenv

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .models.py import VM, Connection

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


connection = Connection()

new_vm = VM()


def get_user_input(prompt, default=None):
    value = input(prompt)
    return value.strip() if value.strip() else default


def create_vm():
    global new_vm, connection

    url = f"{connection.get_url}/api2/json/nodes/{new_vm.node}/qemu/{new_vm.template_id}/clone"
    headers = {
        "Authorization": f"PVEAPIToken={connection.get_api_key()}",
        "Content-Type": "application/json",
    }

    data = {
        "newid": new_vm.id,
    }

    try:
        print("Creating VM...")
        response = requests.post(
            url, headers=headers, data=json.dumps(data), verify=False
        )

        if response.status_code == 200:
            print("VM created successfully!")
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error creating VM: {e}")


def main():
    print("Proxmox VM Creator")
    print("------------------")
    global new_vm

    new_vm.id = get_user_input("Enter new VM ID (e.g., 105): ")
    new_vm.template_id = get_user_input(
        "Enter template VM ID to clone from (e.g., 100): "
    )
    new_vm.node = get_user_input(
        "Enter Proxmox node name (default: athena): ", "athena"
    )
    new_vm.name = get_user_input(
        "Enter new VM name (e.g., test-vm): ", f"vm-{new_vm.id}"
    )
    create_vm()


if __name__ == "__main__":
    main()
