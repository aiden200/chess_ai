import discord
from chess_engine.chess_game import Chess_game


def activate_bot():

    class MyClient(discord.Client):

        async def on_ready(self):
            print(f'Logged on as {self.user}!')

        async def on_message(self, message):
            print(f'Message from {message.author}: {message.content}')

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run('MTA4MzA3ODQ1MTIzNTQxMDEyMA.Gn9dew.HB4orH1xA29T3ql5AqYpqGULE2gPMEJxl-aHGI')