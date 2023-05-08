import disnake, os, datetime
from disnake.ext import commands

from dotenv import load_dotenv
load_dotenv()

bot = commands.InteractionBot(
    # server members intent
    intents=disnake.Intents.all(),
    test_guilds=[791818283867045941],
    status=disnake.Status.idle,
    activity=disnake.Game("with purpose")
)

@bot.event
async def on_ready():
    print(f"🔑 {bot.user}.")

@bot.slash_command(
    name="legacy",
    description="Add the legacy role to all members who joined before 2023.",
)
@commands.default_member_permissions(administrator=True)
async def _legacy(inter : disnake.ApplicationCommandInteraction):
    cutoff = datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc)
    legacy_role = inter.guild.get_role(1105119350052114434)
    error_audit = await bot.fetch_channel(1105089762768982036)

    members = [member for member in inter.guild.members if member.joined_at < cutoff]
    print(f"🔎 Found {len(members)} members.")

    await inter.response.send_message("I'm Mr. Meeseeks, look at me!", embed=disnake.Embed(
        title="Legacy Members",
        description=f"Adding {legacy_role.mention} to `{len(members)}` members.",
        color=disnake.Color.blurple()
    ).set_thumbnail(url=bot.user.avatar.url).set_footer(text="This may take a while..."))

    for member in members:
        try:
            await member.add_roles(legacy_role, reason="Legacy Role")
        except Exception as e:
            await error_audit.send(f"Failed to add {legacy_role.mention} to {member.mention}.\n```{e}```")

    await inter.author.send(f"Succesfully added {legacy_role.mention} to `{len(members)}` members!")
    await inter.guild.leave()




bot.run(os.getenv("TOKEN"))