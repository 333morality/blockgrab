
### blockgrab

blockgrab is a simple script that retrieves direct messages (dms) from blocked users on discord. 

#### prerequisites

1. python 3.7+
2. aiohttp library

install aiohttp:
```bash
pip install aiohttp
```

#### how to get your discord token

1. open discord in your web browser
2. press f12 to open developer tools
3. go to the "network" tab
4. in discord, perform any action (like sending a message)
5. in the network tab, look for a request with "api/v9" in its name
6. click on this request and find the "authorization" header in the request headers
7. the value of this header is your token



#### usage

1. save the script as `blockgrab.py`
2. run it:
   ```bash
   python blockgrab.py
   ```
3. enter your discord token when prompted
4. choose a specific blocked user or grab all

#### examples

grabbing all blocked users' dms:
```
enter your discord token: your_token_here
blocked users:
1. blockeduser1
2. blockeduser2
3. blockeduser3

enter the number of the blocked user to grab (leave empty for all, or 'exit' to quit): 
found 3 blocked users
processing user: blockeduser1
saved messages to messages_blockeduser1_123456789.json
processing user: blockeduser2
saved messages to messages_blockeduser2_987654321.json
processing user: blockeduser3
saved messages to messages_blockeduser3_456789123.json
```

grabbing a specific blocked user's dms:
```
enter your discord token: your_token_here
blocked users:
1. blockeduser1
2. blockeduser2
3. blockeduser3

enter the number of the blocked user to grab (leave empty for all, or 'exit' to quit): 2
processing user: blockeduser2
saved messages to messages_blockeduser2_987654321.json
```



