import discord
from discord.ext import commands
import database_manager as dbm
from datetime import datetime, timezone

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Displays commands based on the user's authorization level."""
        
        # 1. Check Authorization Level
        # We fetch the auth data from your existing database_manager
        auth_data = dbm.load_json(dbm.AUTH_FILE)
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        
        # Default level is 0 (Regular User)
        # If the user is the Bot Owner (defined in your .env or app), we treat them as Level 3
        is_owner = await self.bot.is_owner(ctx.author)
        
        # Get level from JSON: auth_data[guild_id][user_id]
        # Using .get() prevents the bot from crashing if the ID isn't in the file
        user_level = 0
        if is_owner:
            user_level = 3
        else:
            guild_auth = auth_data.get(guild_id, {})
            user_level = guild_auth.get(user_id, 0)

        # 2. Construct the Embed
        embed = discord.Embed(
            title="🥋 JUDO SYSTEM DIRECTORY",
            description=f"Current Access Level: **{user_level}**",
            color=discord.Color.blue(),
            timestamp=datetime.now(timezone.utc)
        )

        # --- CATEGORY: GENERAL (Level 0+) ---
        embed.add_field(
            name="📁 GENERAL", 
            value="`ping`, `display my strikes`, `convey suggestion`, `help`", 
            inline=False
        )

        # --- CATEGORY: MODERATION & INTELLIGENCE (Level 1+) ---
        if user_level >= 1:
            embed.add_field(
                name="📁 MODERATION & INTEL", 
                value="`mute`, `unmute`, `delete`, `kick`, `ban`, `user`, `status`, `display strike of @user`", 
                inline=False
            )

        # --- CATEGORY: MANAGEMENT (Level 2+) ---
        if user_level >= 2:
            embed.add_field(
                name="📁 MANAGEMENT", 
                value="`authorize`, `unauthorize`, `auth_list`, `send`, `servers`", 
                inline=False
            )

        # --- CATEGORY: SUPREME PROTOCOLS (Level 3 / Owner Only) ---
        if user_level >= 3:
            embed.add_field(
                name="⚠️ SUPREME PROTOCOLS", 
                value="`activate_emergency_panic_control_system` \n`deactivate_panic_control_system` \n`clear_auth`, `delete_all` \n`mass authorize`", 
                inline=False
            )

        embed.set_footer(text="Judo Core • Restricted Access System")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))