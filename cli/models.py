from os import getenv


class Connection:
    def __init__(self):
        self.url = None

        self.api_key = getenv("PROXMOX_API_KEY")
        if not self.api_key:
            print(
                "Provide the Proxmox API Key (format: root@pam!cli=c33876a4-5a2a-4d1a-950d-2d9700cd4f41) :\n"
            )
            self.api_key = input().strip()

        self.url = getenv("PROXMOX_API_URL")
        if not self.url:
            print(
                "Provide the Proxmox API URL (e.g., https://hades.node.wmsdev.pl:8006) :\n"
            )
            self.url = input().strip()
        if self.url is None or self.url == "":
            self.url = "https://hades.node.wmsdev.pl:8006"

    def get_url(self):
        return self.url

    def get_api_key(self):
        return self.api_key


class Clone:
    def __init__(self):
        self.newid = None
        self.node = None
        self.template_id = None
        self.description = None
        self.full = True
        self.name = None
        self.pool = None
        self.storage = None
        self.target = None


class Disk:
    def __init__(self):
        self.size = "10G"
        self.storage = "ceph"
        self.interface = "scsi"
        self.index = 0


class IPConfig:
    def __init__(self):
        self.ip = None
        self.gateway = None


class NetworkInterface:
    def __init__(self):
        self.bridge = "vmbr0"
        self.firewall = True
        self.model = "virtio"


class VM:
    def __init__(self):
        self.clone = Clone()
        self.disks = []
        self.agent = True
        self.autostart = True
        self.cloudinit = None
        self.cores = 2
        self.ip = IPConfig()
        self.memory = 2048
        self.net = []
        self.onboot = True
        self.sockets = 1
        self.tags = []
