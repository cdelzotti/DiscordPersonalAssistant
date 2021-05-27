import discord
import environment
import discordSignalitics
import modules.moduleHandler

class DiscordMessageBot(discord.Client):
    # Maps channels's string name to their ID 
    channels = {}
    # Auth token
    TOKEN = ""
    # Command symbol
    CMD_SYMBOL = "%"
    # Module handler
    moduleHandler = ""

    def __init__(self, token, channelsDict):
        """
        Build the whole thing

        Parameters
        ----------
        token : A Discord auth token in string format
        channelsDict : Dict mapping channel's string names to their IDs
        """
        super().__init__()
        self.channels = channelsDict
        self.TOKEN = token
        self.moduleHandler = modules.moduleHandler.ModuleHandler(environment.ENABLED_MODULES)
        self.run()

    async def log(self, symbol, message):
        """
        Send a message preceded by a given symbol in the status channel
        """
        await self.send_message("%s %s" % (symbol, message), "status")

    async def triggerError(self, errorMessage, blockingError=False):
        """
        Send Discord error notification

        Parameters
        ----------
        errorMessage (string) : Message that will be sent to Discord
        blockingError (bool) : true if the error must stop execution, false otherwise
        """
        await self.log(discordSignalitics.error, errorMessage)
        if (blockingError):
            raise ValueError(errorMessage)

    def run(self):
        """
        Run the bot. Once this function is called, execution is blocked.
        """
        return super().run(self.TOKEN)
    
    def get_channel_from_name(self, channelName):
        """
        From a channel's string name, returns the corresponding channel object 
        """
        if self.channels.get(channelName):
            return self.get_channel(self.channels[channelName])
        else:
            self.log("%s doesn't exist in registered channels" % channelName)
            raise ValueError()

    async def send_message(self, message, channelName):
        """
        Send a message to a particular channel

        Parameters
        ----------
        message (string) : the message
        channelName (string) : channel's name
        """
        channel = self.get_channel_from_name(channelName)
        await channel.send(message)
        
    async def on_message(self, message):
        """
        Reaction when a message is sent

        Parameters
        ----------
        message : A Discord API message object
        """
        # If it's a command message
        if message.content.startswith('%'):
            command = message.content[1:].split(" ")
            if len(command) > 0:
                self.moduleHandler.command(command,message)

    async def close(self):
        """
        Run every module closing function before closing bot
        """
        await self.moduleHandler.close()
        await self.log(discordSignalitics.log_out, "Now offline")
        return await super().close()

    async def on_ready(self):
        """
        Code executed after bot initialization
        """
        # Show online status in log
        print('We have logged in as {0.user}'.format(self))
        # Show online status in server
        await self.log(discordSignalitics.validation, "Now online")
        # Setup discord presence
        await self.change_presence(activity=discord.Game(name="Scrapping for master"))
        # Assign real channels to modules
        self.moduleHandler.assignChannels(self)
        # Init modules
        await self.moduleHandler.init()
        # Apply module scrapping
        self.moduleHandler.scrap()

bot = DiscordMessageBot(environment.TOKEN, environment.CHANNELS)