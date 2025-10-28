import discord
from discord import app_commands
from discord.ext import commands

# --- SETTINGS ---
ROLE_ID = 1432681974308274327
PING_ROLE_ID = 1432681974308274327
EMOJI = "👍"  


intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)


@bot.tree.command(name="request", description="Create a roleplay request embed")
@app_commands.describe(
    title="Title for your request",
    description="What your character is doing or looking for"
)
async def request(interaction: discord.Interaction, title: str, description: str):
    guild = interaction.guild
    role_to_give = guild.get_role(ROLE_ID)
    ping_role = guild.get_role(PING_ROLE_ID)


    embed = discord.Embed(title=title, description=description, color=0x5865F2)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
    embed.set_image(url=interaction.user.display_avatar.url)

    
    class RoleButton(discord.ui.View):
        @discord.ui.button(label="Get the role!", style=discord.ButtonStyle.blurple)
        async def button_callback(self, interaction_button: discord.Interaction, button: discord.ui.Button):
            if role_to_give in interaction_button.user.roles:
                await interaction_button.user.remove_roles(role_to_give)
                await interaction_button.response.send_message(f"❌ Removed {role_to_give.name}", ephemeral=True)
            else:
                await interaction_button.user.add_roles(role_to_give)
                await interaction_button.response.send_message(f"✅ Added {role_to_give.name}", ephemeral=True)

    message = await interaction.channel.send(
        content=f"{ping_role.mention}", 
        embed=embed,
        view=RoleButton()
    )

    await message.add_reaction(EMOJI)

    await interaction.response.send_message("✅ Your request has been posted!", ephemeral=True)

import os
TOKEN = os.getenv("DISCORD_TOKEN") 
bot.run(TOKEN)
