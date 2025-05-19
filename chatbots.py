import asyncio
import discord.ext.commands
from characterai import aiocai
import datetime

class ChatBots(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat = None
        self.time = datetime.datetime.now()

    @discord.ext.commands.hybrid_command(description="Habla con JohannBot")
    async def johann(self, context, *, mensaje):
        token = "702892816223e79bd2020285c4a4885455c516d5"
        char = "UygPlmZsnOGvoM76BM5WJOTQ-NKe7DFhIt0Mfn9AVI0"

        if context.interaction != None:
            await context.interaction.response.defer()

        client = aiocai.Client(token)
        me = await client.get_me()

        masUnDia = (datetime.datetime.now() - self.time) >= datetime.timedelta(days=1)

        if self.chat is None or masUnDia:
            if masUnDia:
                self.time = datetime.datetime.now()
            await self.create_chat(client, char, me)

        async with await client.connect() as chatConnection:
            message = await chatConnection.send_message(char, self.chat.chat_id, mensaje)

        respuesta = f"**{context.author.display_name}:** {mensaje}\n**JohannBot:** {message.text}"

        await client.close()
        await context.send(respuesta)

    async def create_chat(self, client, char, me):
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(char, me.id)

        self.chat = new
