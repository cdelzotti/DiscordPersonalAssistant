import asyncio

import discord

class Module:
    # Channel in which this module should post its updates
    channel = ""
    # Discord client object, represents the running bot
    discordBot = ""
    # The string used to trigger a command instruction
    commandTrigger = ""
    # Module human-friendly name
    name = ""
    # Interval between scrapping actions
    triggerInterval = 0
    # Scrapping asyncio task
    scrapTask = ""
    # Command asyncio task
    commandTask = ""
    # Help text
    help = ""
    # Active status
    activated = False

    def __init__(self, channel, triggerInterval):
        self.channel = channel
        self.triggerInterval = triggerInterval

    async def init(self):
        """
        Function called on module initialization
        """
        self.activated = True
        self.scrapTask = asyncio.create_task(self.runScrap())

    async def close(self):
        """
        Function called on module shutdown
        """
        self.activated = False
        self.scrapTask.cancel()
        if self.commandTask != "":
            self.commandTask.cancel()

    async def runInit(self):
        """
        Run init function in a trycatch
        """
        try:
            await self.init()
        except Exception as e:
            self.discordBot.triggerError("I encountered an error while initializing %s : %s" % (self.name, e))

    async def runClose(self):
        """
        Run close function in a trycatch
        """
        try:
            await self.close()
        except Exception as e:
            self.discordBot.triggerError("I encountered an error while closing %s : %s" % (self.name, e))

    async def scrap(self):
        """
        Periodic action executed every `triggerInterval` seconds
        """
        pass

    async def runScrap(self):
        """
        Run the scrap action in a try catch in order to log errors in the Discord Server
        """
        while True:
            try:
                await self.scrap()
            except Exception as e:
                await self.discordBot.triggerError("I encountered an error while scrapping in %s : %s" % (self.name, e))
            await asyncio.sleep(self.triggerInterval)
    
    async def runCommand(self, args, originalMessage):
        """
        Run the comand action in a try catch in order to log errors in the Discord Server
        """
        try:
            await self.command(args, originalMessage)
        except Exception as e:
            await originalMessage.channel.send("I encountered an error while treating command in %s : %s" % (self.name, e))


    async def command(self, args, originalMessage):
        """
        Execute a given command

        Parameters
        ----------
        - args (list of string) : Command arguments
        - originalMessage (Discord message object) : The message that triggered the command
        """
        if args[0] == "setTriggerInterval":
            self.triggerInterval = int(args[1])
            await originalMessage.channel.send("Successfully set triggering interval to %s" % args[1])
        elif args[0] == "help":
            await originalMessage.channel.send(self.help)
