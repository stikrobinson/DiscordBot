from dotenv import load_dotenv
import os
import discord
import discord.ext.commands

import bebetronic
import inp_quiz as inp
from quizzes import Quizzes
from bebetronic import Bebetronic
import comandos_simples
import aleatorio
import chatbots

def main():
  # Cargamos el token del bot (debe ser privado)
  load_dotenv()
  token = os.getenv("DISCORD_TOKEN")

  # Se crea variable intents que contiene todos los intents del bot
  # Los intents son como una funcionalidad a la que se le asocia el bot, dentro del cual encontramos los eventos relacionados a esa funcionalidad
  # discord.intents.default() habilita todos los intents estandares.
  intents = discord.Intents.default()
  # Se habilitan los intents que no son estandar, o tambien llamados de privilegios como Presences, Server Members, y Message Content.
  # Deben tambien ser habilitados en las configuraciones del bot dentro Discord Developer
  intents.message_content = True
  intents.members = True

  # Constructor de la clase cliente o una clase hija
  # La clase cliente es nuestra conección con discord
  # Dentro de ella incluimos los intents
  bot = discord.ext.commands.Bot(command_prefix='=' ,intents=intents)

  # Función para saber si el bot está activo
  # @client.event permite que la función creada se establezca como un evento para el cliente (discord)
  # Todos los eventos deben ser una corutina. Si no lo son, podrías obtener errores inesperados. Para convertir una función en una corutina, deben ser funciones definidas con async def.
  # on_ready()
  @bot.event
  async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.add_cog(inp.Quiz(bot))
    await bot.add_cog(Quizzes(bot))
    await bot.add_cog(Bebetronic(bot))
    await bot.add_cog(comandos_simples.ComandosSimples(bot))
    await bot.add_cog(aleatorio.Random(bot))
    await bot.add_cog(chatbots.ChatBots(bot))
    await bot.tree.sync()
    await bebetronic.control(bebetronic.listaCanales)

  bot.run(token)

if __name__ == "__main__":
  main()
