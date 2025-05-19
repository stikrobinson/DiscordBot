import discord
import asyncio
from aleatorio import shuffle

listaCanales = []
listaTerminarAbruptamente = []

async def can_dm_user(miembro: discord.User):
    try:
        await miembro.send()
    except discord.Forbidden:
        valor = True
    except discord.HTTPException:
        valor = False
    return valor

async def control(listaCanales):
    while True:
        if len(listaCanales) >0:
            for canal in listaCanales:
                if len(canal.members)==0:
                    listaCanales.remove(canal)
        await asyncio.sleep(300)
class Verificador:
    def __init__(self):
        self.interactuado = False
class Bebetronic(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def votacion(self, member):
        class View(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.success, custom_id="aceptar")
            async def buttonA(self, interaction, button):
                await interaction.response.defer()

            @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger, custom_id="cancelar")
            async def buttonB(self, interaction, button):
                await interaction.response.defer()
        try:
            msg = await member.send(content="¿Seguro quieres terminar abruptamente este juego?",view=View())

            def check(int):
                return int.guild is None and int.user == member and int.message == msg

            interaction = await self.bot.wait_for("interaction", check=check, timeout=60)
            await msg.delete()
            return interaction.data["custom_id"]
        except:
            await msg.delete()
            return "cancelar"


    async def get_input(self, member, unidos, mensajeEspera, timeout, channel):
        validas = unidos.copy()
        validas.remove(member)
        seleccion = []
        opciones = []
        contador = 0
        for miembro in validas:
            opcion = discord.SelectOption(label=miembro.display_name, value=contador)
            opciones.append(opcion)
            contador = contador + 1
        descripcion = """❓ **Para escribir tu pregunta anónima:** 
**1.-** Selecciona al usuario
**2.-** Una vez seleccionado el usuario puedes escribirle tu pregunta anónima.\n
⚠️ **Advertencias:** 
**1.-** Una vez seleccionado el usuario este no se puede cambiar
**2.-** Una vez enviada la pregunta esta no se puede cambiar.
**3.-** Piensa y revisa bien antes de interactuar con el bot porque no se pueden hacer cambios.\n
**Paso actual:** """

        verificador = Verificador()

        class View(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @discord.ui.select(options=opciones)
            async def seleccion(self, interaction, select):
                await interaction.response.defer()
                index = int(select.values[-1])
                seleccion.append(validas[index].id)
                for item in self.children:
                    item.disabled = True
                verificador.interactuado = True
                embed = discord.Embed(
                    title="Escribe tu pregunta anónima!",
                    description=descripcion + "2.- Escribe tu pregunta anónima para " + select.options[index].label)
                await interaction.edit_original_response(embed=embed, view=self)

        embed = discord.Embed(title="Escribe tu pregunta anónima!",
        description= descripcion + "1.- Seleccionar al usuario")
        msg = await member.send(embed = embed,view=View())

        def check(msg):
            return (msg.guild is None and msg.author == member and verificador.interactuado) or (channel not in listaCanales)

        try:
            mensaje = await self.bot.wait_for("message", check=check, timeout=timeout)
            if channel not in listaCanales:
                newView = View()
                for item in newView.children:
                    item.disabled = True
                await msg.edit(view=newView)
                return None
            seleccion.append(mensaje.content)
            await member.send("Pregunta anónima enviada!")
            embed = discord.Embed(title="Escribe tu pregunta anónima!",
            description=descripcion + "3.- Pregunta anónima enviada!")
            await msg.edit(embed=embed)
        except:
            return None

        await mensajeEspera.editarMensaje()
        return tuple(seleccion)


    @discord.ext.commands.hybrid_command(description="Primer intento de Bebetronic")
    async def bebetronic(self, context, espera: int = None, privado: bool = True):
        miembro = context.author
        channel = miembro.voice

        class VistaAceptar(discord.ui.View):
            def __init__(self, llamada):
                super().__init__(timeout=None)
                self.llamada = llamada

            async def deshabilitarBotones(self, interaction):
                await interaction.response.defer()
                if miembro == interaction.user and miembro in self.llamada.members:
                    for item in self.children:
                        item.disabled = True
                    await interaction.edit_original_response(view=self)

            @discord.ui.button(label="Listo", style=discord.ButtonStyle.success, custom_id="listo")
            async def buttonA(self, interaction, button):
                await self.deshabilitarBotones(interaction)

            @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger, custom_id="cancelar")
            async def buttonB(self, interaction, button):
                await self.deshabilitarBotones(interaction)

        class VistaPasar(discord.ui.View):
            def __init__(self, llamada):
                super().__init__(timeout=None)
                self.llamada = llamada

            async def deshabilitarBotones(self, interaction):
                await interaction.response.defer()
                if context.author == interaction.user and miembro in self.llamada.members:
                    for item in self.children:
                        item.disabled = True
                    await interaction.edit_original_response(view=self)

            @discord.ui.button(label="Pasar", style=discord.ButtonStyle.success, custom_id="pasar")
            async def buttonA(self, interaction, button):
                if privado:
                    await interaction.response.defer()
                else:
                    await self.deshabilitarBotones(interaction)


            @discord.ui.button(label="Terminar", style=discord.ButtonStyle.danger, custom_id="cancelar")
            async def buttonB(self, interaction, button):
                if privado:
                    await interaction.response.defer()
                else:
                    await self.deshabilitarBotones(interaction)

        if channel == None:
            await context.send("No estás en llamada xd")

        elif channel.channel in listaCanales:
            await context.send("Ya se está jugando en esta llamada")

        else:
            channel = miembro.voice.channel

            unidos = channel.members.copy()
            for m in unidos:
                if m.bot or await can_dm_user(m):
                    unidos.remove(m)

            if len(unidos) == 1:
                await context.send("Solo hay uno en llamada xd")

            else:
                listaCanales.append(channel)


                embed = discord.Embed(title="Instrucciones del Juego",
                description="""A continuación encontrarás las preguntas más incómodas para hacerle a tu pareja, tu crush, tus amigos e incluso a desconocidos.

Para este juego, hay que tener en cuenta lo siguiente:
**1.-** Existen dos roles: el de admin y el de jugador. El admin es quien ha empezado la partida y es el único que puede pasar entre preguntas y terminar la partida. El resto de los que están en la llamada (excepto los bots) son jugadores, quienes envían y responden preguntas.

**2.-** Cuando se inicie la partida, todos los que están en la llamada recibirán un mensaje en privado donde podrán enviar su pregunta. Una vez que todos envíen sus preguntas, estas aparecerán aleatoriamente en pantalla. Para cada pregunta, quien sea mencionado debe responderla. Luego de que la pregunta sea respondida, el admin puede pasar a la siguiente pregunta con el botón 'Pasar' que aparece debajo de la pregunta. Al final cuando se pasen todas las preguntas enviadas, se repite todo lo antes mencionado.

**3.-** El admin puede terminar la partida presionando el botón 'Terminar' que aparece en cada mensaje. Sin embargo, de forma extraordinaria existe el comando /finalizar, que permite que por mayoría de los que están en la llamada se termine el juego. El comando /finalizar tiene un cooldown de diez minutos.

**4.-** En caso que el bot no pueda enviarte mensajes directos, serás directamente excluido del juego. Para saber si el bot puede enviarte mensajes directos usa el comando /verificar_dms, si aparece que está prohibido enviarte mensajes, cambia tus configuraciones de privacidad de discord para que el bot pueda enviarte mensajes directos.

¡Espero que se diviertan mucho!""")
                ruta = "images.jpg"
                file = discord.File(ruta, filename="images.jpg")
                embed.set_image(url="attachment://images.jpg")
                msg = await context.send(file=file,embed=embed,view=VistaAceptar(channel))

                def check(int):
                    return int.user == context.author and int.message == msg and channel in listaCanales and context.author in channel.members

                aceptacion = await self.bot.wait_for("interaction", check=check)

                if aceptacion.data["custom_id"] == "cancelar":
                    listaCanales.remove(channel)
                    return

                else:
                    while len(unidos)>1 and context.author in unidos:

                        class ViewCancelar(discord.ui.View):
                            def __init__(self, context, canal):
                                super().__init__(timeout=None)
                                self.canal = canal
                                self.context = context

                            def deshabilitar(self):
                                for item in self.children:
                                    item.disabled = True

                            @discord.ui.button(label="Terminar", style=discord.ButtonStyle.danger, custom_id="cancelar")
                            async def cancelar(self, interaction, button):
                                await interaction.response.defer()
                                if self.context.author == interaction.user and self.context.author in self.canal.members:
                                    self.deshabilitar()
                                    listaCanales.remove(self.canal)
                                    await interaction.edit_original_response(view=self)
                                    await self.context.send("Juego terminado!")


                        class MensajeEspera:
                            def __init__(self, contador, context, canal):
                                self.contador = contador
                                self.context = context
                                self.view = ViewCancelar(context, canal)

                            async def enviarMensaje(self):
                                msg = await self.context.send(
                                    "Faltan " + str(self.contador) + " personas para empezar!", view=self.view)
                                self.msg = msg

                            async def editarMensaje(self):
                                self.contador = self.contador - 1
                                if self.contador == 1:
                                    msg = await self.msg.edit(
                                        content="Falta " + str(self.contador) + " persona para empezar!")
                                elif self.contador == 0:
                                    msg = await self.msg.edit(content="Empezamos el juego!")
                                else:
                                    msg = await self.msg.edit(
                                        content="Faltan " + str(self.contador) + " personas para empezar!")
                                self.msg = msg

                            async def cerrarMensaje(self):
                                for item in self.view.children:
                                    item.disabled = True
                                await self.msg.edit(view=self.view)
                                if privado:
                                    await asyncio.sleep(2)
                                    await self.msg.delete()



                        mensajeEspera = MensajeEspera(len(unidos),context, channel)
                        await mensajeEspera.enviarMensaje()

                        async with asyncio.TaskGroup() as tg:
                            responses = [tg.create_task(self.get_input(m, unidos, mensajeEspera, espera, channel)) for m in unidos]

                        await mensajeEspera.cerrarMensaje()
                        shuffle(responses)

                        if channel not in listaCanales:
                            return

                        for response in responses:
                            respuesta = response.result()
                            if respuesta != None:
                                embed = discord.Embed(title="Pregunta Anónima",description=f"**Pregunta para:** <@{respuesta[0]}>\n```{respuesta[1]}```")
                                confesion = await context.send(embed=embed, view=VistaPasar(channel))

                                def check(int):
                                    return int.user == context.author and int.message == confesion and channel in listaCanales and context.author in channel.members

                                pasar = await self.bot.wait_for("interaction", check=check)

                                if pasar.data["custom_id"] == "cancelar":
                                    if privado:
                                        await confesion.delete()
                                    await context.send("Juego terminado!")
                                    listaCanales.remove(channel)
                                    return
                                elif pasar.data["custom_id"] == "pasar" and privado:
                                    await confesion.delete()

                        unidos = channel.members.copy()
                        for m in unidos:
                            if m.bot or await can_dm_user(m):
                                unidos.remove(m)

                    listaCanales.remove(channel)
                    await context.send("Juego terminado!")
                    return

    @discord.ext.commands.hybrid_command(description="Terminar partidas de Bebetronic")
    @discord.ext.commands.cooldown(1, 600, discord.ext.commands.BucketType.user)
    async def finalizar(self, context):
        for canal in listaCanales:
            if canal in listaTerminarAbruptamente:
                await context.send("Ya se está intentando terminar este juego")
                return
            elif context.author in canal.members:
                listaTerminarAbruptamente.append(canal)
                await context.send(content="Para finalizar abruptamente el juego la mayoría de los que están en llamada deben seleccionar el botón Aceptar que se les enviará en privado. Tienen un minuto para responder.")

                unidos = canal.members.copy()
                for m in unidos:
                    if m.bot or await can_dm_user(m):
                        unidos.remove(m)

                async with asyncio.TaskGroup() as tg:
                    responses = [tg.create_task(self.votacion(m)) for m in unidos]

                contador=0
                for response in responses:
                    respuesta = response.result()
                    if respuesta == "aceptar":
                        contador = contador + 1

                mayoria=len(unidos)//2+1

                if contador >= mayoria:
                    listaCanales.remove(canal)
                    listaTerminarAbruptamente.remove(canal)
                    await context.send(f"El resultado fue: {contador}/{len(unidos)}\nPartida terminada abruptamente")
                    return
                else:
                    listaTerminarAbruptamente.remove(canal)
                    await context.send(f"El resultado fue: {contador}/{len(unidos)}\nPartida no se terminó abruptamente")
                    return

        await context.send("No estás en una llamada en la que se esté jugando")
        return

    @finalizar.error
    async def futuro_error(self, context, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            tiempo = int(round(error.retry_after, 0))
            minutos = tiempo // 60
            segundos = tiempo % 60
            try:
                await context.interaction.response.send_message(content=f"Faltan {minutos} minutos, y {segundos} segundos para que puedas volver a finalizar una partida",ephemeral=True)
            except:
                await context.send(f"Faltan {minutos} minutos, y {segundos} segundos para que puedas volver a finalizar una partida")

    @discord.ext.commands.hybrid_command(description="Verifica si el bot puede enviarte mensaje directos")
    async def verificar_dms(self, context):
        try:
            await context.author.send(content="Test")
            valor = "Se puede enviar mensaje"
        except discord.Forbidden:
            valor = "No se puede enviar mensaje, está prohibido"
        except discord.HTTPException:
            valor = "Se puede enviar mensaje, pero hay problemas con los servidores"
        await context.send(valor)