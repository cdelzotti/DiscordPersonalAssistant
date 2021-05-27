import asyncio

class ModuleHandler:
    """
    Object handling command and scrapping calls for modules.
    """
    # A list of every modules
    modules = []
    # The char used to trigger a command
    CMD_SYM = ""


    def __init__(self, moduleList, CMD_SYMBOL):
        """
        Inititalize a moduleHandler by setting its modules list
        """
        self.modules = moduleList
        self.CMD_SYM = CMD_SYMBOL

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

    def command(self, args, originalMessage):
        """
        Initialize an async task for every module's crap function

        Parameters
        ----------
        args (list of strings) : Command arguments
        originalMessage (Discord message object) : Message that triggered the command
        """
        if args[0] == "help":
            helpText = "Each module provides its how help menu :\n\n"
            for module in self.modules:
                helpText += "- **%s** : %s%s help\n" % (module.name, self.CMD_SYM, module.commandTrigger)
            asyncio.create_task(originalMessage.channel.send(helpText))
        else:
            for module in self.modules:
                # Find which module is should be sollicited by this command 
                if args[0] == module.commandTrigger:
                    # Call the concerned module
                    module.commandTask = asyncio.create_task(module.runCommand(args[1:], originalMessage))

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
