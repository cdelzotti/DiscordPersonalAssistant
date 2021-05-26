# Discord Personal Assistant

A quick base for a Discord personal assistant using Discord Python API.

## How it works

This Discord bot is build in a modular approach. It uses modules to allow you to define precisely what you want to do with your Discord Personal Assistant.

### What is a module ?

A module is a part of your Discord Personal Assistant where you can define what it does. A module is built around two main concepts :

1. **Scrapping** : A function called at a certain interval performing a specific action (Checking the news, parsing tweets, checking if your train is late, etc).
2. **Command** : A function called by the user using a specific keyword, allowing you to handle interaction with users.


## How to use

In order to run your discord assistant, you'll need to specify values in `environment.py`:

See

- [How to get your bot token](https://discordpy.readthedocs.io/en/latest/discord.html)
- [How to find your channel IDs](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

```python
from modules import *

# Bot token
TOKEN = "your-bot-token"
# Mapping between channel's name and their IDs
# MUST contains a 'status' channel
CHANNELS = {
    "status" : 123456789123456789,
    "helloWorld" : 123456789213456789,
    "news" : 123456789123457689
}
# Every modules used by the bot
# Each module takes 2 parameters in its contructor :
# 1. A channel name (must match one of the channels set above) defining where the module is going to send its updates
# 2. A triggering interval defining de time (in seconds) between 2 scrapping actions  
ENABLED_MODULES = [
    # Exemple
    HelloWorldModule("news", 10)
]
```

You'll find every module in the `modules` folder.

## How can I make my own modules ?

The whole idea of this project is to give you an easy way to build your own modules. To do so, you just have to define a new module in the modules directory following this structure :

```python
from modules.module import Module

class HelloWorldModule(Module):
    """
    An exemple module, showing how it works
    """

    # Set a human friendly-name for your module
    name = "Hello world Module"
    # Define the string used to call this module command function
    commandTrigger = "hello"

    # Define how your module is supposed tho handle commands
    async def command(self, args, channel):
        if args[0] == "hello":
            await channel.send("Hello!")
        return await super().command(args, channel)

    # Define your module scrapping behaviour
    async def scrap(self):
        await self.channel.send("Hello!")
        return await super().scrap()
```

Once your module is defined, you simply have to add it in the ENABLE_MODULES of your environment :

```python
# Every modules used by the bot
# For each module takes 2 parameters in its contructor :
# 1. A channel name (must match one of the channels set above) defining where the module is going to send its updates
# 2. A triggering interval defining de time (in seconds) between 2 scrapping actions  
ENABLED_MODULES = [
    # Exemple
    HelloWorldModule("news", 10)
]
```