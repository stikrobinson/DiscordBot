import discord
import discord.ext.commands
import numpy as np
from aleatorio import shuffle, randint
class Quizzes(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.hybrid_command(description="Las fechas civicas aprendidas en 8vo, 9no, y 10mo. Tienes 15 segundos para responder.")
    async def fechascivicas(self, context):
        archivo = open("fechascivicas.txt", "r", encoding='utf-8')
        fechas = archivo.readlines()
        archivo.close()
        shuffle(fechas)
        fechasEscogidas = []
        acontecimientosEscogidos = []
        contador = 1
        division = fechas[0].strip().split(":")
        fechasEscogidas.append(division[0])
        acontecimientosEscogidos.append(division[1])
        while contador != 5:
            division = fechas[contador].strip().split(":")
            if division[0] not in fechasEscogidas:
                fechasEscogidas.append(division[0])
                acontecimientosEscogidos.append(division[1])
                contador = contador + 1
        letras = "ABCDE"
        numeroRandom = randint(0, 1)
        numeroOpcionCorrecta = randint(0, 4)
        if numeroRandom == 0:
            texto = f"**{fechasEscogidas[numeroOpcionCorrecta]}**\n"
            for num in range(5):
                texto = texto + letras[num] + ". " + acontecimientosEscogidos[num] + "\n"
            embed = discord.Embed(
                color=discord.Colour.random(),
                description=texto,
            )
        else:
            texto = f"**{acontecimientosEscogidos[numeroOpcionCorrecta]}**\n"
            for num in range(5):
                texto = texto + letras[num] + ". " + fechasEscogidas[num] + "\n"
            embed = discord.Embed(
                color=discord.Colour.random(),
                description=texto,
            )

        class VistaBotones(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=15)
                self.msg = None

            async def deshabilitarBotones(self, interaction):
                if context.author == interaction.user:
                    for item in self.children:
                        item.disabled = True
                    await interaction.response.edit_message(view=self)

            def deshabilitarVista(self):
                for item in self.children:
                    item.disabled = True

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

            @discord.ui.button(label="E", style=discord.ButtonStyle.primary, custom_id="4")
            async def buttonE(self, interaction, button):
                    await self.deshabilitarBotones(interaction)

        msg = await context.send(embed=embed, view=VistaBotones())

        def check(interaction):
            return interaction.message == msg and context.author == interaction.user

        try:
            interaction = await self.bot.wait_for("interaction", check=check, timeout=15)
        except:
            interaction = None

        if interaction == None or interaction.data["custom_id"] != str(numeroOpcionCorrecta):

            if interaction == None:
                nuevaVista = VistaBotones()
                nuevaVista.deshabilitarVista()
                await msg.edit(view=nuevaVista)

            await msg.add_reaction("❌")

            try:
                archivo = open(str(context.guild.id)+".csv","r",encoding='utf-8')
                lineas = archivo.readlines()
                archivo.close()
            except:
                pass

            archivo = open(str(context.guild.id) + ".csv", "w", encoding='utf-8')
            contador = 0
            for linea in lineas:
                linea = linea.strip()
                if linea.startswith(str(context.author.id)):
                    division = linea.split(",")
                    if int(division[1]) == 1:
                        lineas.pop(contador)
                    else:
                        lineas[contador] = str(context.author.id) + "," + str(int(division[1])-1) + "\n"
                    archivo.writelines(lineas)
                    archivo.close()
                    return
                contador = contador + 1
            return
        else:
            await msg.add_reaction("✅")

            try:
                archivo = open(str(context.guild.id) + ".csv", "r", encoding='utf-8')
                lineas = archivo.readlines()
                archivo.close()
            except:
                lineas = []

            archivo = open(str(context.guild.id) + ".csv", "w", encoding='utf-8')
            contador = 0
            for linea in lineas:
                linea = linea.strip()
                if linea.startswith(str(context.author.id)):
                    division = linea.split(",")
                    lineas[contador] = str(context.author.id) + "," + str(int(division[1]) + 1) + "\n"
                    archivo.writelines(lineas)
                    archivo.close()
                    return
                contador = contador + 1
            lineas.append(str(context.author.id) + ",1\n")
            archivo.writelines(lineas)
            archivo.close()
            return

    @discord.ext.commands.hybrid_command(description="Mira quien es el experto en fechas cívicas!")
    async def leaderboard(self, context):
        try:
            archivo = open(str(context.guild.id)+".csv","r",encoding='utf-8')
            lineas = archivo.readlines()
            archivo.close()
        except:
            lineas = []

        usuarios = []
        puntajes = []

        for linea in lineas:
            division = linea.strip().split(",")
            miembro = context.guild.get_member(int(division[0]))
            if miembro != None:
                usuarios.append(miembro.display_name)
                puntajes.append(int(division[1]))
        arrayPuntajes = np.array(puntajes)
        arrayUsuarios = np.array(usuarios)
        mascara = arrayPuntajes.argsort()[::-1]
        ordenUsuarios = arrayUsuarios[mascara]
        ordenPuntajes =  arrayPuntajes[mascara]

        puesto = 1
        contenido = "Aquí solo aparecen aquellos que tienen al menos un punto, recordar que puedes al responder una pregunta de forma correcta ganas un punto, y si es de forma incorrecta pierdes un punto. Es decir, puedes estar fuera del leaderboard por nunca haber respondido una pregunta o por haber llegado a los cero puntos."
        if arrayUsuarios.size > 0:
            contenido = contenido + "\n\n**Leaderboard:**\n\n"
            for indice in range(arrayUsuarios.size):
                contenido = contenido + f"{puesto}.- **{ordenUsuarios[indice]}** - {ordenPuntajes[indice]}\n"
                if indice == arrayUsuarios.size-1:
                    pass
                elif ordenPuntajes[indice] != ordenPuntajes[indice+1]:
                    puesto = puesto + 1

        embed = discord.Embed(
            title="🏆 LeaderBoard de Fechas Cívicas 🏆",
            color=discord.Colour.random(),
            description=contenido
        )
        await context.send(embed=embed)


