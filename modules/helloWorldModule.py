from modules.module import Module

class HelloWorldModule(Module):
    """
    An exemple module, showing how it works
    """

    # Set a human friendly-name without spaces for your module
    name = "HelloWorldModule"
    # Define the string used to call this module command function
    commandTrigger = "hello"
    # Define a hel text that will be showed with the help command
    help = """
    Manual for the HelloWorld module :

    **Description**
    This is a test module that just says hello

    **Commands**
    - hello : says hello

    **Scrap**
    Says hello on its attributed channel
    """

    # Define actions that should be performed on module init
    async def init(self):
        return await super().init()

    # Define how your module is supposed tho handle commands
    async def command(self, args, originalMessage):
        if args[0] == "hello":
            await originalMessage.channel.send("Hello!")
        return await super().command(args, originalMessage)

    # Define your module scrapping behaviour
    async def scrap(self):
        await self.channel.send("Hello!")
        return await super().scrap()

    # Define your module behaviour when closing
    async def close(self):
        return await super().close()