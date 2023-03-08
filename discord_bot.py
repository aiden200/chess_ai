import discord
from discord_token import *
from chess_engine.chess_game import Chess_game


def activate_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    # intents = discord.Intents.all()

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        channel = client.get_channel
        print(channel, message)
        # if message.author == client.user:
        #     return

        # if message.content.startswith('$hello'):
        #     await message.channel.send('Hello!')
    

    client.run(token)


activate_bot()