#!/usr/bin/env python3
from typing import Any, Dict, List


class VPN(object):

    US_FREE = "LAB Access (us-free)"
    US_VIP = "LAB Access (us-vip)"
    EU_FREE = "LAB Access (eu-free)"
    EU_VIP = "LAB Access (eu-vip )"
    AU_FREE = "LAB Access (au-free)"
    FORTRESS = "Fortress lab"
    RELEASE = "Release Arena"
    VALID_LABS = [US_FREE, US_VIP, EU_FREE, EU_VIP, AU_FREE, FORTRESS, RELEASE]

    def __init__(self, connection: Any, data: Dict[str, Any]):

        # Certain data is only available when connected
        if data["success"] == 0:
            self.ipv4: str = None
            self.ipv6: str = None
            self.rate_up: float = 0
            self.rate_down: float = 0
            self.user: str = None
            self.active: bool = False
        else:
            self.active: bool = True
            self.user: str = data["connection"]["name"]
            self.ipv4: str = data["connection"]["ip4"]
            self.ipv6: str = data["connection"]["ip6"]
            self.rate_up: float = data["connection"]["up"]
            self.rate_down: float = data["connection"]["down"]

        # Server information is always available
        self.hostname = data["server"]["serverHostname"]
        self.port = data["server"]["serverPort"]
        self.connection = connection

    @property
    def name(self) -> str:
        name_map = {
            "us-free": VPN.US_FREE,
            "us-vip": VPN.US_VIP,
            "eu-free": VPN.EU_FREE,
            "eu-vip": VPN.EU_VIP,
            "au-free": VPN.AU_FREE,
            "-fort-": VPN.FORTRESS,
            "-release-": VPN.RELEASE,
        }

        for piece in name_map:
            if piece in self.hostname:
                return name_map[piece]


    def __repr__(self) -> str:
        if self.active:
            return f"""<VPN ipv4="{self.ipv4}", up={self.rate_up}, down={self.rate_down}, server="{self.hostname}:{self.port}">"""
        else:
            return f"""<VPN active=False, server="{self.hostname}:{self.port}">"""
