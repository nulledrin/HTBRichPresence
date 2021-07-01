from os import name
from pypresence import Presence
import time
import json
import sys
from connection import Connection

rpc = Presence(855129833826680892)
rpc.connect() 

activebox=None
api_token=None
profileurl="https://app.hackthebox.eu/profile/id"

if api_token is None:
    print("enter api_token!!!")
    sys.exit()

cnxn: Connection = Connection(
    api_token=api_token,
    subscribe=True,
)

if len(sys.argv)==1:
    amachine = None
elif "--help" in sys.argv[1]:
    print("Usage: python3 {} [active_machine], [--help]".format(sys.argv[0]))
    sys.exit()
else:
    amachine = sys.argv[1]

print(cnxn.lab_status())

if amachine is not None:
    machinelist=cnxn.machines()
    activebox = next((i for i in machinelist if i["name"]==amachine), None)
    if activebox is not None:
        idbox = "id"+str(activebox['id'])
        osbox = str(activebox['os'])
        print(osbox)
        namebox = str(activebox['name'])
        if str(activebox['id']) in str(cnxn.owned_root()):
            details = namebox+" (root)"
        elif str(activebox['id']) in str(cnxn.owned_user()):
            details = namebox+" (User)"
        else:
            details = namebox+" (foothold)"

status = cnxn.lab_status()

while(True):
    ts = time.time()
    while("Fortress" in str(cnxn.lab_status())): # Fortress
        print("Fortress")
        try:
            rpc.update(
                large_image="htb_icon",
                large_text="HackTheBox",  
                start=ts,
                state="{}".format(status[0]),
                details="Doing: "+amachine,
                buttons=[
                {
                        "label": "Profile",
                        "url": profileurl
                    }
                ]
            )

        except Exception as e:
            print(f"Cannot be displayed! Error: {e}")
        time.sleep(15)
    ts = time.time()
    while("Disconnected" in str(cnxn.lab_status())): #Disconnected
        print("Disconnected")
        try:
            rpc.update(
                large_image="htb_icon",
                large_text="HackTheBox", 
                start=ts,
                state="Status: Disconnected",
                 details="Offline",
                buttons=[
                    {
                        "label": "Profile",
                        "url": profileurl
                    }
                ]
            )

        except Exception as e:
            print(f"Cannot be displayed! Error: {e}")
        time.sleep(15)
    ts = time.time()
    while("Release" or "machine" in str(cnxn.lab_status())): # Lab or Release Arena
        if "Disconnected" in str(cnxn.lab_status()):
            break
        print("Lab or Arena")
        if activebox is not None:
            try:
                rpc.update(
                    large_image=str(idbox),
                    large_text=namebox, 
                    small_image=osbox.lower(), 
                    small_text=osbox, 
                    start=ts, 
                    # end=tsend,
                    state="{}".format(cnxn.lab_status()[0]),  
                    details=details,
                    buttons=[
                        {
                            "label": "Profile",
                            "url": profileurl
                        }
                    ]
                )

            except Exception as e:
                rpc.update(
                    large_image="htb_icon", 
                    large_text="HackTheBox", 
                    start=ts, 
                    # end=tsend,
                    state="{}".format(cnxn.lab_status()[0]),  
                    details=details,
                    buttons=[
                        {
                            "label": "Profile",
                            "url": profileurl
                        }
                    ]
                )
            time.sleep(15)
        else:
            try:
                rpc.update(
                    large_image="htb_icon", 
                    large_text="HackTheBox", 
                    start=ts,  
                    # end=tsend, 
                    state="{}".format(cnxn.lab_status()[0]),
                    details="Status: Connected",
                    buttons=[
                        {
                            "label": "Profile",
                            "url": profileurl
                        }
                    ]
                )

            except Exception as e:
                print(f"Cannot be displayed! Error: {e}")
            time.sleep(15)  
