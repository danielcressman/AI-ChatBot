import argparse
import discord
import faqbot
import random

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    def get_response_and_embed(self, message):
        result = faqbot.predict(message)
        empty_field = ['', '', '']
        if result is not None:
            responses = result['responses']
            fieldOne = result['Field-1'] if 'Field-1' in result else empty_field
            fieldTwo = result['Field-2'] if 'Field-2' in result else empty_field
            fieldThree = result['Field-3'] if 'Field-3' in result else empty_field
            fieldFour = result['Field-4'] if 'Field-4' in result else empty_field
            fieldFive = result['Field-5'] if 'Field-5' in result else empty_field
            fieldSix = result['Field-6'] if 'Field-6' in result else empty_field
            RelatedQ = result['Related-Q'] if 'Related-Q' in result else '' 
            theTag = result['tag']
            embed = None

                #### Make the embed if there is no resource field 1 ####
            if fieldOne[0] == "" and RelatedQ != "":
                embed=discord.Embed(title="Related Questions:", description=RelatedQ, color=0x6544e9)
                embed.set_footer(text="I am only useable by Admins, mods, and helpers in this channel. If you want to ask me a question, please visit #🤖basic-qa-bot. You do not need to type !bot in that channel.".format(RelatedQ))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856984019337609236/862729433265864784/Refold-Japanese.png")
                #### Make embed if there is a field 1 resource ####
            if fieldOne[0] != "":
                embed=discord.Embed(title="Additional Resources:", description="", color=0x6544e9)
                embed.set_footer(text="I am only useable by Admins, mods, and helpers in this channel. If you want to ask me a question, please visit #🤖basic-qa-bot. You do not need to type !bot in that channel.".format(RelatedQ))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856984019337609236/862729433265864784/Refold-Japanese.png")
                embed.add_field(name=fieldOne[0], value="[{}]({})".format(fieldOne[1], fieldOne[2]), inline=True)
                if fieldTwo[0] != "":
                    embed.add_field(name=fieldTwo[0], value="[{}]({})".format(fieldTwo[1], fieldTwo[2]), inline=True)
                    if fieldThree[0] != "":
                        embed.add_field(name=fieldThree[0], value="[{}]({})".format(fieldThree[1], fieldThree[2]), inline=True)
                        if fieldFour[0] != "":
                            embed.add_field(name=fieldFour[0], value="[{}]({})".format(fieldFour[1], fieldFour[2]), inline=True)
                            if fieldFive[0] != "":
                                embed.add_field(name=fieldFive[0], value="[{}]({})".format(fieldFive[1], fieldFive[2]), inline=True)
                                if fieldSix[0] != "":
                                    embed.add_field(name=fieldSix[0], value="[{}]({})".format(fieldSix[1], fieldSix[2]), inline=True)
                if RelatedQ != "": 
                    embed.add_field(name="Related Questions", value=RelatedQ, inline=False)
            return random.choice(responses), embed
        return None, None

    async def send_reply(self, response, embed, reply_to):
        await reply_to.reply(response)
        if embed is not None:
            await reply_to.channel.send(embed=embed)


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.channel.name in ['beginner-questions', 'methodology-qa', 'language-general', 'off-topic']:
            if discord.utils.get(message.author.roles, name="Admin") is not None or discord.utils.get(user.roles, name="Mod") is not None or discord.utils.get(user.roles, name="Helper") is not None:
                if message.content.startswith('!bot'):
                    inp = message.content[5:]
                    response, embed = self.get_response_and_embed(inp)
                    reference = message.reference
                    if reference is None:
                        await self.send_reply(response, embed, message)
                    else:
                        await self.send_reply(response, embed, reference.resolved)
            return

        if message.channel.name == '🤖basic-qa-bot':
            response, embed = self.get_response_and_embed(message.content)  
            if response is not None:
                await self.send_reply(response, embed, message)
            else:
                await message.channel.send("I'm sorry. I have not been taught an answer to this question yet. Please ask a different way or try again later. I will hopefully be taught this soon.\n Until then try <#778822272081330177>, <#778820943459778570>, <#778821128436318218> or the most appropriate channel. Don't forget to tag your questions with !q to make them easy for mods and helpers to find.   ")

parser = argparse.ArgumentParser(description='Discord FAQ bot for Refold Mandarin server')
parser.add_argument('auth_key', type=str, help='the key to authenticate this discord bot with discord')
args = parser.parse_args()
client = MyClient()
client.run(args.auth_key)
