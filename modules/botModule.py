from modules.module import Module
import discordSignalitics

class BotModule(Module):
    """
    A module handling bot configuration
    """

    # Set a human friendly-name for your module
    name = "BotModule"
    # Define the string used to call this module command function
    commandTrigger = "bot"
    # Define a hel text that will be showed with the help command
    help = """
    Manual for the BotModule module :

    **Description**
    This is the bot management module

    **Commands**
    - stop : stops the bot
    - status : shows the bot status
    - module start ModuleName : starts the module called ModuleName
    - module stop ModuleName : stops the module called ModuleName

    **Scrap**
    None
    """

    # Define actions that should be performed on module init
    async def init(self):
        return await super().init()

    # Define how your module is supposed tho handle commands
    async def command(self, args, originalMessage):
        # Stop the bot
        if args[0] == "stop":
            await self.discordBot.close()
        # Show status for each module
        elif args[0] == "status":
            response = "Modules status :\n\n"
            for module in self.discordBot.moduleHandler.modules:
                if module.activated:
                    status = discordSignalitics.validation
                else:
                    status = discordSignalitics.log_out
                response += "- %s %s\n" % (status, module.name)
            await originalMessage.channel.send(response)
        # Handle modules comand
        elif args[0] == "module":
            await self.moduleCommand(args[1:], originalMessage)
        return await super().command(args, originalMessage)

    # Define your module scrapping behaviour
    async def scrap(self):
        return await super().scrap()

    # Define your module behaviour when closing
    async def close(self):
        return await super().close()
    
    async def moduleCommand(self, args, originalMessage):
        """
        Handles the module part of the command treatement
        """
        # Stops a module
        if args[0] == 'stop':
            await self.changeModuleStatus(args, originalMessage, False)
        elif args[0] == "start":
            await self.changeModuleStatus(args, originalMessage, True)
        
    async def changeModuleStatus(self, args, originalMessage, newState):
        """
        Changes the state of a module

        Parameters
        ----------
        - args (list of string) : List of arguments
        - originalMessage (Discord message object) : Message which triggered the command
        - newState (bool) : The state on which you want to set the module
        """
        # Checks if a name is provided
        if len(args) < 2:
            await originalMessage.channel.send("You must provide a module name")
        else:
            # Search the corresponding module
            found = False
            for module in self.discordBot.moduleHandler.modules:
                # If it is the right name
                if module.name == args[1]:
                    found = True
                    # Check if not deactivated already
                    if module.activated == newState :
                        await originalMessage.channel.send("This module is already %s" % ("started" if newState else "stopped"))
                    else:
                        if newState:
                            # Start the module
                            await module.init()
                        else:
                            # Stop the module
                            await module.close()
                        await originalMessage.channel.send("%s module %s" % ("Started" if newState else "Stopped", module.name))
            # If no module was found
            if not found:
                await originalMessage.channel.send("Could not find a module called %s" % args[1])