# HTBRichPresence
Unofficial Discord Rich Presence for HackTheBox platform
The project is under lazy development.

## How to run
Install requirements: // I'm gonna add this
```
pip3 install -r requirements.txt
```
Enter your api_key in main.py script (1 on screenshot) and your id (2 on screenshot)

![idandapi](https://raw.githubusercontent.com/nulledrin/HTBRichPresence/main/boxicons/enterapikeyandid.png)

And run the main script:
```
python3 path/to/main.py [active_machine], [--help]
```
## Info about
Attention: `active_machine` is for showing what box you re doing now and it's case sensitive! U're using this arg makes RP look like that:

![RPwithactive_machine](https://raw.githubusercontent.com/nulledrin/HTBRichPresence/main/boxicons/active_machine_screen.png)

But now that works only for non-retired boxes. Also, `active_machine` may be used as fortress name

`active_machine` is NOT necessary argument, you can run the script without one

If you run Release Arena you have to enter `active_machine` anyway // Check features

You should be connected to HTB or script show this RP:

![RPwithDisconnected](https://raw.githubusercontent.com/nulledrin/HTBRichPresence/main/boxicons/offline_screen.png)

Any questions? My discord is nulledrin#0001

## Features gonna be realized later
- Show battlegrounds
- Show Release Arena box without entering `active_machine`
- Challenges and starting point info
- Rank and progress info
- VIP users wont hafta enter active_machine
