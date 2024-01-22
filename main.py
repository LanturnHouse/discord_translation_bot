import yaml
import os
import googletrans

import discord
from discord.ext import commands


#============  초기변수 설정  =================
main_path = os.path.abspath(__file__)
main_path = main_path.replace("\\","/")
main_path = f"{main_path}./../"

config_path = main_path + "config.yaml"
with open(config_path, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)


client = commands.Bot(command_prefix= "-", intents=discord.Intents.all())
translator = googletrans.Translator()



@client.event
async def on_ready():
    print("\n\n")
    print(f'Bot {client.user} is online.')
    with open(config_path, encoding='utf-8') as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
    await client.change_presence(status = discord.Status.online, activity = discord.Game(config_data['BOT_STATUS']))
    await client.tree.sync()

@client.event
async def on_message(message: discord.message.Message):
    if not message.author.bot:
        original_message = message.content
        original_message_lang = translator.detect(original_message).lang
        trans_messages = []

        print(f"original message: {original_message}")
        print(f"original message lang: {original_message_lang}")


        embed = discord.Embed(color = 0x87CEEB)
        embed.set_author(name= f"{message.author.name}", icon_url=message.author.avatar.url)

        if original_message_lang == "en":
            trans_messages.append(translator.translate(original_message, dest='ko').text )
            trans_messages.append(translator.translate(original_message, dest='ja').text )
            
            embed.add_field(name="Korean", value=f"{trans_messages[0]}", inline=False)
            embed.add_field(name="Japanese", value=f"{trans_messages[1]}", inline=False)
        elif original_message_lang == "ko":
            trans_messages.append(translator.translate(original_message, dest='en').text )
            trans_messages.append(translator.translate(original_message, dest='ja').text )
            
            embed.add_field(name="English", value=f"{trans_messages[0]}", inline=False)
            embed.add_field(name="Japanese", value=f"{trans_messages[1]}", inline=False)
        elif original_message_lang == "ja":
            trans_messages.append(translator.translate(original_message, dest='ko').text )
            trans_messages.append(translator.translate(original_message, dest='en').text )
            
            embed.add_field(name="Korean", value=f"{trans_messages[0]}", inline=False)
            embed.add_field(name="English", value=f"{trans_messages[1]}", inline=False)
        



        await message.reply(embed = embed, mention_author = False)

        print(trans_messages)
        


with open(config_path, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
client.run(config_data['TOKEN'])