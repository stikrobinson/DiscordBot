import discord
import discord.app_commands
import discord.ext.commands
import datetime
from random import shuffle, randint

dias_por_mes = {
    1: 31,  # Enero
    2: 28,  # Febrero (considerando años no bisiestos)
    3: 31,  # Marzo
    4: 30,  # Abril
    5: 31,  # Mayo
    6: 30,  # Junio
    7: 31,  # Julio
    8: 31,  # Agosto
    9: 30,  # Septiembre
    10: 31,  # Octubre
    11: 30,  # Noviembre
    12: 31  # Diciembre
}

def fechaAleatoria(fechaCreacion,fechaHoy):
    year = randint(fechaCreacion.year, fechaHoy.year)
    if year == fechaCreacion.year:
        mes = randint(fechaCreacion.month, 12)
        if mes == fechaCreacion.month:
            dia = randint(fechaCreacion.day, dias_por_mes[mes])
        else:
            dia = randint(1, dias_por_mes[mes])
    elif year == fechaHoy.year:
        mes = randint(1, fechaHoy.month)
        if mes == fechaHoy.month:
            dia = randint(1, fechaHoy.day)
        else:
            dia = randint(1, dias_por_mes[mes])
    else:
        mes = randint(1, 12)
        dia = randint(1, dias_por_mes[mes])

    return datetime.datetime(year, mes, dia)

class Random(discord.ext.commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @discord.ext.commands.hybrid_command(description="Mira una frase aleatoria de la historia")
    async def inp_random(self, context):
        archivo = open("Isekai_No_Parodi.txt", "r", encoding='utf-8')
        lineas = archivo.readlines()
        shuffle(lineas)
        archivo.close()
        await context.send(content=lineas[0])

    @discord.ext.commands.hybrid_command(description="Frase sin contexto de un usuario")
    async def frase_random(self, context, usuario: discord.User, canal: discord.channel.TextChannel):
        if context.interaction is not None:
            await context.interaction.response.defer()

        fechaCreacion = canal.created_at
        fechaHoy = datetime.date.today()

        messages = []
        while messages == []:
            fecha = fechaAleatoria(fechaCreacion,fechaHoy)
            async for message in canal.history(limit=101, around=fecha):
                if message.author == usuario and message.content != "":
                    messages.append(message.content)

        shuffle(messages)
        await context.send(content=messages[0])

