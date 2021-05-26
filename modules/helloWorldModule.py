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