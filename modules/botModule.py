from modules.module import Module

class BotModule(Module):
    """
    A module handling bot configuration
    """

    # Set a human friendly-name for your module
    name = "Bot Module"
    # Define the string used to call this module command function
    commandTrigger = "bot"

    # Define actions that should be performed on module init
    async def init(self):
        return await super().init()

    # Define how your module is supposed tho handle commands
    async def command(self, args, channel):
        if args[0] == "stop":
            await self.discordBot.close()
        return await super().command(args, channel)

    # Define your module scrapping behaviour
    async def scrap(self):
        return await super().scrap()

    # Define your module behaviour when closing
    async def close(self):
        return await super().close()