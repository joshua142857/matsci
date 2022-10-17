import discord
import update as u

client = discord.Client()


@client.event
async def on_ready():
    activity = discord.Activity(name='some numbers', type=discord.ActivityType.watching)
    channel = 722248861967450162
    await client.change_presence(activity=activity)
    x = u.run(0)
    while x != -1:
        print(x)
        if x < 28867:
            x = u.run(x)
        else:
            x = -1
    if x == -1:
        await client.get_channel(channel).send("<@315226882108948500> Completed")
    if x == 0:
        await client.get_channel(channel).send("<@315226882108948500> Broken")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "xyz":
        await message.channel.send("boi")

client.run("NzIyMDYzNTE3ODQ2MzM5Njc2.GZM97l.FX3vXgO5okynzVvp9eQNrhC41tBEmGcavCh2zg")