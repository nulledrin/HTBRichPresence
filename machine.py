#!/usr/bin/env python3
from typing import Dict, Any, List
from io import StringIO
import subprocess
import threading
import json
import os
import re

from exceptions import *


class Machine(object):
    """ Interact with a Hack the Box machine """
    
    def __init__(self, connection: Any, data: Dict[str, Any]):
        """ Build a machine object from API data """
        
        self.connection = connection
        
        # Standard data (should always exist)
        self.id: int = None
        self.name: str = None
        self.os: str = None
        self.ip: str = None
        self.avatar: str = None
        self.points: str = None
        self.release_date: str = None
        self.retire_date: str = None
        self.makers: List[Dict] = None
        self.rating: float = None
        self.user_owns: int = None
        self.root_owns: int = None
        self.free: bool = None
        self.analysis_path: str = None
        self.services: List[Service] = []
        self.knowns: Dict[str, Any] = {}
        
        self.update(data)
    
    def __repr__(self) -> str:
        return f"""<Machine id={self.id},name="{self.name}",ip="{self.ip}",os="{self.os}">"""
    
    def update(self, data: Dict[str, Any]):
        """ Update internal machine state from recent request """
        
        # Standard data (should always exist)
        self.id: int = data["id"]
        self.name: str = data["name"].lower()  # We don't like capitals :(
        self.os: str = data["os"]
        self.ip: str = data["ip"]
        self.avatar: str = data["avatar_thumb"]
        self.points: str = data["points"]
        self.release_date: str = data["release"]
        self.retire_date: str = data["retired_date"]
        self.makers: List[Dict] = [data["maker"]]
        self.rating: float = 0.0
        self.user_owns: int = data["user_owns"]
        self.root_owns: int = data["root_owns"]
        self.free: bool = False
        
        # May exist
        if "maker2" in data and data["maker2"] is not None:
            self.makers.append(data["maker2"])
    
    @property
    def hostname(self) -> str:
        return f"{self.name.lower()}.htb"
    
    @property
    def spawned(self) -> bool:
        """ Whether this machine has been spawned """
        
        spawned = self.connection._api("/machines/spawned", method="get", cache=True)
        
        return any([s["id"] == self.id for s in spawned])

    @property
    def assigned(self) -> bool:
        """ Whether this machine is currently assigned to the logged in user """
        
        machines = self.connection._api("/machines/assigned", method="get", cache=True)
        
        return any([m["id"] == self.id for m in machines])
    
    @property
    def owned_user(self) -> bool:
        """ Whether you have owned user on this machine """
        
        machines = self.connection._api("/machines/owns", method="get", cache=True)
        
        return any([m["id"] == self.id and m["owned_user"] for m in machines])
    
    @property
    def owned_root(self) -> bool:
        """ Whether you have owned root on this machine """
        
        machines = self.connection._api("/machines/owns", method="get", cache=True)
        
        return any([m["id"] == self.id and m["owned_root"] for m in machines])
    
    @property
    def ratings(self) -> bool:
        """ The difficulty rating for this machine """
        
        machines = self.connection._api(
            "/machines/difficulty", method="get", cache=True
        )
        
        try:
            return [m["difficulty_ratings"] for m in machines if m["id"] == self.id][0]
        except IndexError:
            return [0 for i in range(10)]
    
    @property
    def blood(self) -> Dict[str, str]:
        """ Grab machine blood information """
        r = self.connection._api(f"/machines/get/{self.id}", method="get", cache=True)
        return {"user": r["user_blood"], "root": r["root_blood"]}
    