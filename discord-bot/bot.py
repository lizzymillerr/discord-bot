import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from aiohttp import web


ROLE_ID = 1432681974308274327  # Role given when clicking the button (ping role)
EMOJI = "👍"  
GUILD_ID = 1430175314583224450


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(
    name="request",
    description="Create a roleplay request embed"
)
@app_commands.describe(
    title="Title for your request",
    description="Description for your request"
)
async def request(interaction: discord.Interaction, title: str, description: str):
    guild = interaction.guild
    role_to_give = guild.get_role(ROLE_ID)

    embed = discord.Embed(title=title, description=description, color=0x5865F2)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)

    class RoleButton(discord.ui.View):
        @discord.ui.button(label="Ping Me!", style=discord.ButtonStyle.blurple)
        async def button_callback(self, interaction_button: discord.Interaction, button: discord.ui.Button):
            # Toggle role
            if role_to_give in interaction_button.user.roles:
                await interaction_button.user.remove_roles(role_to_give)
                await interaction_button.response.send_message(f"❌ Removed {role_to_give.name}", ephemeral=True)
            else:
                await interaction_button.user.add_roles(role_to_give)
                await interaction_button.response.send_message(f"✅ Added {role_to_give.name}", ephemeral=True)

    
    message = await interaction.channel.send(
        content=f"{role_to_give.mention}",  # ping role in message
        embed=embed,
        view=RoleButton(),
        allowed_mentions=discord.AllowedMentions(roles=True)  # ⚡ important for ping to work
    )
    await message.add_reaction(EMOJI)

    # Confirmation to user
    await interaction.response.send_message("✅ Your request has been posted!", ephemeral=True)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Synced {len(synced)} slash commands to the guild.")
    except Exception as e:
        print(e)


async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"✅ Dummy web server running on port {port}")


async def main():
    await start_web_server()  # Start dummy web server
    await bot.start(os.environ["DISCORD_TOKEN"])  # Start Discord bot

asyncio.run(main())







