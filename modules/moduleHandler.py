import asyncio

class ModuleHandler:
    """
    Object handling command and scrapping calls for modules.
    """
    # A list of every modules
    modules = []

    def __init__(self, moduleList):
        """
        Inititalize a moduleHandler by setting its modules list
        """
        self.modules = moduleList

    async def init(self):
        """
        Initializes every module
        """
        for module in self.modules:
            await module.runInit()

    async def close(self):
        """
        Closes every module
        """
        for module in self.modules:
            await module.runClose()

    def scrap(self):
        """
        Initialize an async task for every module's crap function
        """
        for module in self.modules:
            asyncio.create_task(module.runScrap())

    def command(self, args, originalMessage):
        """
        Initialize an async task for every module's crap function

        Parameters
        ----------
        args (list of strings) : Command arguments
        originalMessage (Discord message object) : Message that triggered the command
        """
        for module in self.modules:
            # Find which module is should be sollicited by this command 
            if args[0] == module.commandTrigger:
                # Call the concerned module
                asyncio.create_task(module.runCommand(args[1:], originalMessage))

    def assignChannels(self,discordBot):
        """
        Replace strings in module by their Discord object representation

        Parameters
        ----------
        discordBot(Discord Client object)
        """
        for module in self.modules:
            module.channel = discordBot.get_channel_from_name(module.channel)
            module.discordBot = discordBot
