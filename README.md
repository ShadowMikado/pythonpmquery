# pythonpmquery

A Python script which allows you to query servers for a selection of information

## Basic Usage
This script is litteraly a python translatation of [libpmquery](https://github.com/jasonw4331/libpmquery/) by [@jasonw4331](https://github.com/jasonw4331) and was made for developers to query Pocketmine-MP servers with ease. Here is some basic functionality:

### Required imports
The following imports are necessary to use the virion library:
```python
from PMQuery import PMQuery, PMQueryException
```

### API
The querying API is a single function which grabs the data from whatever server you input. Usage is as follows:
```php
query = PMQuery.query("my.server.net", 19132)
```
The values returned will follow these values/types:
```python
query.get("GameName")         # Returns the server software being used
query.get("HostName")         # Returns the server host name
query.get("Protocol")         # Returns the protocol version allowed to connect
query.get("Version")          # Returns the client version allowed to connect
query.get("Players")          # Returns the number of players on the server currently
query.get("MaxPlayers")       # Returns the maximum player count of the server
query.get("ServerId")         # Returns the RakNet server ID
query.get("Map")              # Returns the default world name
query.get("GameMode")         # Returns the default game mode
query.get("NintendoLimited")  # Returns the status of Nintendo's limitation to join
query.get("IPv4Port")         # Returns the IPv4 port number
query.get("IPv6Port")         # Returns the IPv6 port number
query.get("Extra")            # I still don't know what this info is
```

### Offline Queries
Queries sent to offline servers always throw a `PmQueryException`. Exceptions can be caught in a try/except statement to log their offline status.
```python
try:
    query = PMQuery.query("my.server.net", 19133)
    players = query.get('Players')
    print(f"There are {players} on the queried server right now!")
except PMQueryException as e:
    # You can choose to log this if you want
    print("The queried server is offline right now!")

```

Thanks again to [@jasonw4331](https://github.com/jasonw4331)
