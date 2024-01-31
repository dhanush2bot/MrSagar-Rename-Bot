import os
from pyrogram import Client, filters
from helper.database import botdata, find_one, total_user
from helper.progress import humanbytes

token = os.environ.get('TOKEN', '')
botid = token.split(':')[0]

@Client.on_message(filters.private & filters.command(["about"]))
async def start(client, message):
    botdata(int(botid))
    data = find_one(int(botid))
    
    # Check if the key exists in the dictionary
    total_rename = data.get("total_rename", "Key not found")
    total_size = data.get("total_size", "Key not found")
    
    await message.reply_text(f"᚛› 𝐔𝐬𝐞𝐫𝐬 - {total_user()}\n᚛› 𝐑𝐞𝐧𝐚𝐦𝐞 𝐅𝐢𝐥𝐞𝐬 - {total_rename}\n᚛› 𝐑𝐞𝐧𝐚𝐦𝐞𝐝 𝐒𝐢𝐳𝐞 - {humanbytes(int(total_size))}", quote=True)
