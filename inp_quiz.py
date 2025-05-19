import discord
import discord.ext.commands
from aleatorio import shuffle
def cargar_preguntas(dificultad):
  rutaPreguntas = "inp_quiz/" + dificultad + "/preguntas.txt"
  archivoPreguntas = open(rutaPreguntas,"r", encoding='utf-8')
  lineas = archivoPreguntas.readlines()
  for element in lineas:
    element.strip()
  archivoPreguntas.close()
  return lineas

def cargar_opciones(dificultad):
  rutaOpciones = "inp_quiz/" + dificultad + "/opciones.txt"
  archivoOpciones = open(rutaOpciones,"r", encoding='utf-8')
  lineas = archivoOpciones.readlines()
  for element in lineas:
    element.strip()
  archivoOpciones.close()
  lineas.pop(0)
  return lineas


def dificultadString(dificultad):
  match dificultad:
    case "facil":
      return "fácil"
    case "medio":
      return "medio"
    case "dificil":
      return "díficil"
    case "imposible":
      return "imposible"

def leerResultados(dificultad,puntaje):
  ruta = "inp_quiz/" + dificultad + "/resultados.txt"
  archivo = open(ruta,"r", encoding='utf-8')
  lineas = archivo.readlines()
  resultado = lineas[puntaje].strip()
  return "Has obtenido un puntaje de " + str(puntaje) + "\n" + resultado

class Quiz(discord.ext.commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.ext.commands.hybrid_command(description="El quiz de Isekai No Parodi en discord!")
  async def inpquiz(self,context):
    embed = discord.Embed(
      title="INP QUIZ",
      description="Bienvenido al Isekai no Parodi Quiz!\nSelecciona la dificultad!"
    )
    id = 0
    class VistaMenu(discord.ui.View):
      async def deshabilitarMenu(self, interaction):
        if context.author == interaction.user:
          for item in self.children:
            item.disabled = True
          await interaction.response.edit_message(view=self)

      @discord.ui.select(options=[discord.SelectOption(label="Fácil", value="facil"),
                                  discord.SelectOption(label="Medio", value="medio"),
                                  discord.SelectOption(label="Díficil", value="dificil"),
                                  discord.SelectOption(label="Imposible", value="imposible")])
      async def seleccion(self, interaction, select):
        valor = select.values[-1]
        await self.deshabilitarMenu(interaction)

    msg = await context.send(embed=embed, view=VistaMenu())

    def check(interaction):
      return interaction.message == msg and interaction.user == context.author

    int = await self.bot.wait_for("interaction", check=check)
    dificultad = int.data["values"][0]
    nombreDificultad = dificultadString(dificultad)
    introduccion = discord.Embed(
      title="Has escogido la dificultad " + nombreDificultad.capitalize(),
      description="A continuación te vas a responder el quiz!\nEste consiste en 10 preguntas de opción múltiple.\nSuerte y que te diviertas!\nPresiona listo para empezar!",
    )
    ruta = "inp_quiz/" + dificultad + "/imagenes/dificultad.png"
    file = discord.File(ruta, filename="dificultad.png")
    introduccion.set_image(url="attachment://dificultad.png")

    class VistaAceptar(discord.ui.View):
      async def deshabilitarBotones(self, interaction):
        if context.author == interaction.user:
          for item in self.children:
            item.disabled = True
          await interaction.response.edit_message(view=self)

      @discord.ui.button(label="Listo", style=discord.ButtonStyle.success, custom_id="listo")
      async def buttonA(self, interaction, button):
        await self.deshabilitarBotones(interaction)

      @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger, custom_id="cancelar")
      async def buttonB(self, interaction, button):
        await self.deshabilitarBotones(interaction)

    msg = await context.send(embed=introduccion, file=file, view=VistaAceptar())
    int = await self.bot.wait_for("interaction", check=check)
    if int.data["custom_id"] == "cancelar":
      return
    else:
      preguntas = cargar_preguntas(dificultad)
      opciones = cargar_opciones(dificultad)

    class VistaBotones(discord.ui.View):
      def __init__(self):
        super().__init__(timeout=None)

      async def deshabilitarBotones(self,interaction):
        if context.author == interaction.user:
          for item in self.children:
            item.disabled = True
          await interaction.response.edit_message(view=self)

      @discord.ui.button(label="A", style=discord.ButtonStyle.primary, custom_id="0")
      async def buttonA(self, interaction, button):
        await self.deshabilitarBotones(interaction)

      @discord.ui.button(label="B", style=discord.ButtonStyle.primary, custom_id="1")
      async def buttonB(self, interaction, button):
        await self.deshabilitarBotones(interaction)

      @discord.ui.button(label="C", style=discord.ButtonStyle.primary, custom_id="2")
      async def buttonC(self, interaction, button):
        await self.deshabilitarBotones(interaction)

      @discord.ui.button(label="D", style=discord.ButtonStyle.primary, custom_id="3")
      async def buttonD(self, interaction, button):
        await self.deshabilitarBotones(interaction)

    puntaje = 0
    for num in range(10):
      pregunta = preguntas[num]
      divisionOpciones = opciones[num].split(",")
      opcionesPregunta = divisionOpciones[0:4]
      correcta = divisionOpciones[4].strip()
      shuffle(opcionesPregunta)
      indiceCorrecto = opcionesPregunta.index(correcta)
      letras = "ABCD"
      texto = f"**{pregunta}**\n"
      for op in range(4):
        texto = texto + letras[op] + ". " + opcionesPregunta[op] + "\n"
      embed = discord.Embed(
        color=discord.Colour.random(),
        description=texto,
      )
      numPregunta = str(num + 1)
      try:
        ruta = "inp_quiz/" + dificultad + "/imagenes/" + numPregunta + ".png"
        file = discord.File(ruta, filename=numPregunta + ".png")
        embed.set_image(url="attachment://" + numPregunta + ".png")
      except:
        file = None
      msg = await context.send(embed=embed, view=VistaBotones(), file=file)
      int = await self.bot.wait_for("interaction", check=check)
      if int.data["custom_id"] == str(indiceCorrecto):
        puntaje = puntaje + 1
        await msg.add_reaction("✅")
      else:
        await msg.add_reaction("❌")

    texto = leerResultados(dificultad, puntaje)
    titulo = "Felicidades, has completado el quiz de Isekai no Parodi!\n" + "DIFICULTAD " + nombreDificultad.upper()
    embed = discord.Embed(
      color=discord.Colour.light_embed(),
      description=texto,
      title=titulo
    )
    ruta = "inp_quiz/calificaciones/" + str(puntaje) + ".png"
    file = discord.File(ruta, filename=str(puntaje) + ".png")
    embed.set_image(url="attachment://" + str(puntaje) + ".png")
    await context.send(embed=embed, file=file)