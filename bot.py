# Imports
import discord
import json
import time

# Insert your token, if not the bot will not work
token='token'

# Insert your channel id, where users are gonna countup ;)
channel=955099338374271026

# Insert youer bot id
botid=954500672349425734

# Makes a function named "getCurrent"
def getCurrent():
    # Opens a file, and loads in json.
    f = open("countup.json")
    d = json.load(f)
    # Returns the "d" variable
    return d


class MyClient(discord.Client):
    # Runs this event every bot start
    async def on_ready(self):
        # Defines the channel
        mesChannel = client.get_channel(channel)

        # Gets current status
        current = getCurrent()
        currentNum = current['countup']

        # Sends update message
        m = await mesChannel.send(f'Bot is up and running!\nWe do not moderate messages sent in our downtime\nThe current number is: **{currentNum}**')

        # Looks after last update message
        if current['lastupdatemessage'] != 0:
            msg = await mesChannel.fetch_message(int(current['lastupdatemessage']))
            await msg.delete()

        # Updates json file
        dictionary ={"countup": currentNum, "lastupdatemessage": m.id}

        json_object = json.dumps(dictionary,indent = 2)

        # Writes the new message's id inside our json file
        with open('countup.json',"w") as outfile:
            outfile.write(json_object)

        # Makes a update loop
        while True:
            # Gets current status every second
            current = getCurrent()
            currentNum = current['countup']

            # Edit's the current update text to the new status
            await m.edit(content=f'Bot is up and running!\nWe do not moderate messages sent in our downtime\nThe current number is: **{currentNum}**')

            # Makes loop, sleep for 1 second
            time.sleep(1)

    # Runs this event every time a person sends a message
    async def on_message(self, message):
        # Checks if message is inside the correct channet
        if message.channel.id == channel:

            # Defines a shortcut
            content = message.content

            # Checks if message is numeric
            if content.isnumeric():
                # Loades our json file
                f = open("countup.json")
                d = json.load(f)

                # Checks to make sure that our int version of the players message is not None
                if int(content) != None:
                    # Checks if the int version of the message, is the current number +1
                    if int(content) == int(d["countup"])+1:

                        # Being ready to update json file
                        dictionary ={"countup": int(d["countup"])+1, "lastupdatemessage": d["lastupdatemessage"]}

                        json_object = json.dumps(dictionary,indent = 2)

                        # Removes all text from the json file
                        f.seek(0)

                        # Defines a currentnum
                        currentNum = int(d["countup"])+1

                        # Updates lines in our json file
                        with open('countup.json',"w") as outfile:

                            # Writes the text
                            outfile.write(json_object)

                        # Sends a message to the user, so the person is sure that the bot is running
                        await message.reply("Updated - (" + str(currentNum) + ")", delete_after=0.5)

                    else:
                        # Deletes text if its not correct
                        await message.reply(f'({content}) by {message.author.name} was deleted', delete_after=3)
                        await message.delete()

                        # Closes json file
                        f.close()

            else:
                # Checks if the message is not from the bot
                if message.author.id != botid:
                    # If not, deletes message
                    await message.delete()

# Sets client to our class "MyClient"
client = MyClient()

# Runs the bot, under our token
client.run(token)
