import discord
import discord.app_commands
import discord.ext.commands

nivel1 = discord.Embed(title="Nivel 1", description="""
• El Trío Clásico (Sadhu, Johann, Steve).
• El grupo empezó con solo tres personas.
• A lo largo de la historia del grupo han habido tres trios principales: Sadhu, Johann, Steve (el clásico); Sadhu, Samir, Johann; y Johann, Sadhu, Jordy.
• Existen dos mensajes principales del grupo, el grupo de Whatsapp 'Amigardos' y el Discord 'Ronaldinho LOL', cada uno tiene su propia historia.
• Antes, el grupo se conocía como 'Super Mega', que se cambiaria a partir de un suceso histórico.
• El roll que ha estado presente en el Discord y el Whatsapp (mucho más en Whatsapp), los cuales contienen variados arcos que marcaron un antes y un después.
• El muro de frases icónicas.
• La expansión del grupo, cuando dejo de ser solo un trio, y empezaron a llegar más integrantes.
• Las historietas icónicas: 'Sparcky: El Perro Volador' y 'Amistad, Amigos no Enemigos'.
• Los crranos y costeños.
• Modas de prestigio y competencia: Los niveles, la economía del servidor y actualmente las waifus.
• Los miembros temporales (que fueron de corto plazo o estuvieron solo un año), por ejemplo, Thomas, Leandro, Jose Andrés.
• El boom de los juegos en la pandemia y discord, por ejemplo, Among us, Bebetronic, Minecraft, Gartic Phone, Chaton, Roblox.
• Llamadas internacionales.""")

nivel2 = discord.Embed(title="Nivel 2", description="""
• Las obsesiones del grupo (ejemplo: Jojo's, Beyblade, Pokémon, Sonic y Mario, Fútbol).
• La foto grupal supuestamente cada año.
• La decadencia, y tiempos excesivos de inactividad.
• 7-1 Jordy vs Dioggo Free Fire.        
• Las elecciones del admin.
• Canciones de Emilio.
• Los arcos del roll (ejemplo: dictaduras, elecciones, golpes de estado, arcos con villanos).
• Guerra entre UwU, OwO, 7w7, y el :v.
• Make It Memes.
• Isekai no Parodi.
• Los trolleos (ejemplo: trolleos en Instagram, trolleos en Amino).
• Ronaldinho League (un torneo de fútbol en PVP, Axel salió campeón).
• Las páginas de Instagram de Super Mega: @team_super_mega y @super_mega_momazos.
• El manga de décimo hecho en clases de pintura.
• El Hola Grupo de Dioggo.
• La Batalla de Billetees en 5to (los Sadhu vs Sergio dólares más Juanse).
• El estornudo de Steve.
• Enfrentamiento: Emilio vs Miss Maria Isabel.
• Apodos como: Sadhu el Pirro, Dhusa, Sadhu Mafu, Emciclocks, Furro, Stik Tok, Esteban Dido, Agotado Stock.
• Los servidores de Ronaldinho LOL en Minecraft.
• La frase: ¿Por qué eres tan feo?.
• Hangouts y Messenger.
• Este iceberg que estás leyendo es una segunda versión, la primera es lost media y nunca se completó.
• Las actuaciones de Speaking, Beyblade, y cuando Sadhu se tiró a la pared.
• Intento fallido de cambio de nombre de Super Mega a Disoulx.""")

nivel3 = discord.Embed(title="Nivel 3", description="""
• Cuando Samir y Sadhu tuvieron novias de internet al mismo tiempo.
• La pelea por una chica entre Dioggo, Sadhu, Samir.
• El cague de Sadhu con Samantha y Johann.
• Chat de Axel con Abdala Bucaram.        
• Intento de trolleo de Jordy y Sahid al server.
• Conspiración de fraude electoral de Dioggo.
• La pica entre Axel y Dioggo.
• Incidente del cumpleaños de Daniel 30/01/2021.
• La polémica entre Jordy y Johann por una chica.
• El incidente de Clarence.
• Intento de fraude electoral de Jordy.
• Mudae Tóxico.
• Discusiones con Allesia.
• #JohannVuelveACasa.
• Make it Memes (incidente de los memes ofensivos).
• El caballo de Bebetronic.
• Spam de culos.
• La vez que Daniel se voló con Axel.
• La ola de bromas hacia la relación de Johann.
• Los chistes racistas de Sadhu.
• Worlds.com.
• **Jordy (2018)**.""")

nivel4 = discord.Embed(title="Nivel 4", description="""
• Issac.
• Videos Nazis de Issac.
• El incidente de Axxxel cruceta con Daniel.
• Spam de caballos.""")

nivel5 = discord.Embed(title="Nivel 5", description="""
• Videos gore.
• Invasión de Axel (alias Pinchevsky) al grupo de Whatsapp.""")

nivel6 = discord.Embed(title="Nivel 6", description="""
• Funa a Giordano.""")

nivel7 = discord.Embed(title="Nivel 7", description="""
• **El incidente de DAISY'S DESTRUCTION.**""")

def determinarNivel(num):
    if num==1:
        return nivel1
    elif num==2:
        return nivel2
    elif num==3:
        return nivel3
    elif num==4:
        return nivel4
    elif num==5:
        return nivel5
    elif num==6:
        return nivel6
    elif num==7:
        return nivel7

class Vista(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.nivel = 1

    @discord.ui.button(label="←", disabled = True, custom_id="izq")
    async def buttonIzq(self, interaction, button):
        await self.actualizar(interaction)

    @discord.ui.button(label="→", custom_id="der")
    async def buttonDer(self, interaction, button):
        await self.actualizar(interaction)
    async def actualizar(self, interaction):
        if interaction.data["custom_id"] == "izq":
            if self.nivel != 1:
                self.nivel = self.nivel - 1
            if self.nivel != 1:
                for item in self.children:
                    item.disabled = False
            elif self.nivel == 1:
                for item in self.children:
                    if item.custom_id == "izq":
                        item.disabled = True
            await interaction.response.edit_message(embed=determinarNivel(self.nivel), view=self)
        elif interaction.data["custom_id"] == "der":
            if self.nivel !=7:
                self.nivel = self.nivel + 1
            if self.nivel != 7:
                for item in self.children:
                    item.disabled = False
            elif self.nivel == 7:
                for item in self.children:
                    if item.custom_id == "der":
                        item.disabled = True
            await interaction.response.edit_message(embed=determinarNivel(self.nivel),view=self)

class ComandosSimples(discord.ext.commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @discord.ext.commands.hybrid_command(description="Mira el iceberg del grupo!")
    async def iceberg(self, context):
        if context.interaction != None:
            await context.interaction.response.defer()
        await context.send(file=discord.File("ICEBERG_DE_AMIGARDOS_2.0.png"), embed=nivel1, view=Vista())
