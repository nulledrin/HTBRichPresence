#!/usr/bin/env python3
from typing import Any, Dict, List, Union, Callable
from configparser import ConfigParser
import threading
import requests
import time
import json
import re

from vpn import VPN
from machine import Machine
from exceptions import *

class Connection(object):

    BASE_URL = "https://www.hackthebox.eu"
        
    def __init__(
        self,
        api_token: str,
        subscribe: bool = False,
        analysis_path=None
    ):

        # Save the API key
        self.api_token: str = api_token
        
        self._cache: Dict[str, Any] = {}
        self.cache_timeout: float = 60

        self._machines: Dict[int, Machine] = {}
        self.analysis_path = analysis_path

    def _api(self, endpoint, args={}, method="post", cache=False, **kwargs) -> Dict:
        # If requested, attempt to cache the response for up to `self.cache_timeout` seconds
        if cache and endpoint in self._cache and method in self._cache[endpoint]:
            if (time.time() - self._cache[endpoint][method][0]) < self.cache_timeout:
                return self._cache[endpoint][method][1]

        # Construct necessary parameters for request
        url = f"{Connection.BASE_URL}/api/{endpoint.lstrip('/')}"
        headers = {
            "User-Agent": "https://github.com/nulledrin/HTBRichPresence",
            "Authorization": f"Bearer {self.api_token}",
        }
        methods = {"post": requests.post, "get": requests.get}
        args.update({"api_token": self.api_token})

        # Request failed
        r = methods[method.lower()](
            url, params=args, headers=headers, allow_redirects=False, **kwargs
        )
        if r.status_code != 200:
            raise AuthFailure

        # Grab response data
        response = r.json()

        # It's an integer but they always send it as a string :(
        if "success" in response:
            if isinstance(response["success"], str):
                response["success"] = int(response["success"])

        # Save the response for future cache reuse
        if cache:
            if endpoint not in self._cache:
                self._cache[endpoint] = {}
            self._cache[endpoint][method] = (time.time(), response)

        return response

    def lab(self) -> VPN:
        r = self._api("/users/htb/connection/status")
        return VPN(self, r)

    def release(self) -> VPN:
        r = self._api("/users/htb/release/connection/status")
        return VPN(self, r)
    def fortress(self) -> VPN:
        r = self._api("/users/htb/fortress/connection/status")
        return VPN(self, r)

    def lab_status(self) -> None:

        lab = self.lab()
        release = self.release()
        fortress = self.fortress()

        output = []

        if lab.active:
            output.append(
                f"Server: {lab.name}"
            )
        elif release.active:
            output.append(
                f"Server: {release.name}"
            )
        elif fortress.active:
            output.append(
                f"Server: {fortress.name}"
            )

        if lab.active or release.active or fortress.active:
            output.append(
                f"Status: Connected"
            )
        else:
            output.append(
                f"Status: Disconnected"
            )

        return output
    
    def spawned(self) -> bool:  # VIP Only
        spawned = self._api("/machines/spawned", method="get", cache=True)
        return spawned

    def machines(self) -> List[Machine]:
        # Request all the machine information
        data = self._api("/machines/get/all", method="get", cache=True)
        # Build internal machine list
        for datum in data:
            if int(datum["id"]) in self._machines:
                self._machines[int(datum["id"])].update(datum)
            else:
                self._machines[int(datum["id"])] = Machine(self, datum)
        # Create machine objects for all the machine information
        #items = [m for _, m in self._machines.items()]
        return data

    def owned_user(self) -> bool:
        machines = self._api("/machines/owns", method="get", cache=True)
        #return any([m["id"] == self.id and m["owned_user"] for m in machines])
        return machines
    
    def owned_root(self) -> bool:
        machines = self._api("/machines/owns", method="get", cache=True)
        #return any([m["id"] == self.id and m["owned_root"] for m in machines])
        return machines