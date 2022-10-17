import discord
import update4 as u

client = discord.Client()


@client.event
async def on_ready():
    activity = discord.Activity(name='some numbers', type=discord.ActivityType.watching)
    channel = 722248861967450162
    await client.change_presence(activity=activity)
    x = u.run(4692)
    while x != -1 or x != 0:
        print(x)
        x = u.run(x)
    if x == -1:
        await client.get_channel(channel).send("<@315226882108948500> Completed")
    if x == 0:
        await client.get_channel(channel).send("<@315226882108948500> Broken")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message == "xyz":
        await message.channel.send("boi")

client.run("OTI0NzgxOTExMTk1Mzg5OTYz.G0_hSh.jvAjBcK7Xk6JMPMshTvsWkofEx9PjwYvEUJFns")