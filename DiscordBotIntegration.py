import discord
from discord.ext import commands
import UseCNN

description = '''A bot allowing concept artists to use a CNN neural network to find what genre and decade of movie 
posters an image is similar to.

?CNNHelp for commands.'''

# Create Bot With Token
token = 'MTA0OTc0MjYwNjMwNjkyMjUxNw.GTc7RX.XoY7aM_XTKGe0NyJ_Dok9R06kSMNqSpWKOkz5U'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Help Command
@bot.command()
async def CNNHelp(ctx):
    await ctx.send("Commands:")
    await ctx.send("?Genre(url): Request the CNN to predict the genre of a movie based of a poster url.")
    await ctx.send("?Decade(url): Request the CNN to predict the decade of a movie based of a poster url.")

# Request Genre Prediction
@bot.command()
async def Genre(ctx, url:str):
    await ctx.send("Command recognised! Let me figure out what genre I think that image that is!")
    output = UseCNN.Genre(url)
    await ctx.send(output[0])

    try:
        output[1].savefig("foo.png")
        file = discord.File("foo.png", filename='foo.png')
        embed = discord.Embed(color=0xff0000)
        embed = embed.set_image(url="attachment://foo.png")
        await ctx.send(file=file, embed=embed)

    except Exception as e:
        await ctx.send(f"An error occured: {e}")

# Request Decade Prediction
@bot.command()
async def Decade(ctx, url:str):
    await ctx.send("Command recognised! Let me figure out what decade I think that image that is!")
    output = UseCNN.Decade(url)
    await ctx.send(output[0])

    try:
        output[1].savefig("foo.png")
        file = discord.File("foo.png", filename='foo.png')
        embed = discord.Embed(color=0xff0000)
        embed = embed.set_image(url="attachment://foo.png")
        await ctx.send(file=file, embed=embed)

    except Exception as e:
        await ctx.send(f"An error occured: {e}")

# Run Bot
bot.run(token)