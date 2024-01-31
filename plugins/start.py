import os
import time
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.progress import humanbytes
from helper.database import find_one, total_rename, total_size, daily as daily_, used_limit, usertype, updatetotal
from pyrogram.file_id import FileId
from helper.date import add_date, check_expi

CHANNEL = os.environ.get('CHANNEL', "")
STRING = os.environ.get("STRING", "")
log_channel = int(os.environ.get("LOG_CHANNEL", ""))
token = os.environ.get('TOKEN', '')
botid = token.split(':')[0]

# Part of Day --------------------
currentTime = datetime.datetime.now()

if currentTime.hour < 12:
    wish = "Good morning."
elif 12 <= currentTime.hour < 18:
    wish = 'Good afternoon.'
else:
    wish = 'Good evening.'

# -------------------------------

app = Client("my_account")


@app.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    old = insert(int(message.chat.id))
    try:
        id = message.text.split(' ')[1]
    except:
        await message.reply_text(text=f"""{wish} {message.from_user.mention}\n\nThis is an advanced and yet powerful rename bot.\n\nUsing this bot you can rename and change thumbnail of your files.\n\nYou can also convert video to file and file to video.\n\nThis bot also supports custom thumbnail and custom caption.\n\nBot is made by @MrSagarBots""", reply_to_message_id=message.id,
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton('⚚     BOT CHANNEL    ⚚', url='https://t.me/MrSagarBots')],
                                      [InlineKeyboardButton('👨‍💻 OWNER', url='https://t.me/MrSagar0'),
                                       InlineKeyboardButton('⚡️ PREMIUM PLANS ⚡️', callback_data="upgrade")]]))
        return
    if id:
        if old == True:
            try:
                await client.send_message(id, "Your friend already using me")
                await message.reply_text(text=f"""{wish} {message.from_user.mention}\n\nThis is an advanced and yet powerful rename bot.\n\nUsing this bot you can rename and change thumbnail of your files.\n\nYou can also convert video to file and file to video.\n\nThis bot also supports custom thumbnail and custom caption.\n\nBot is made by @MrSagarBots""",
                                         reply_to_message_id=message.id,
                                         reply_markup=InlineKeyboardMarkup(
                                             [[InlineKeyboardButton('⚚      BOT CHANNEL     ⚚',
                                                                    url='https://t.me/MrSagarBots')],
                                              [InlineKeyboardButton('👨‍💻 OWNER', url='https://t.me/MrSagar0'),
                                               InlineKeyboardButton('⚡️ PREMIUM PLANS ⚡️',
                                                                    callback_data="upgrade")]]))
            except:
                return
        else:
            await client.send_message(id, "You won 100 MB extra upload limit 😊")
            _user_ = find_one(int(id))
            limit = _user_["uploadlimit"]
            new_limit = limit + 104857600
            uploadlimit(int(id), new_limit)
            await message.reply_text(
                text=f"""{wish} {message.from_user.mention}\n\nThis is an advanced and yet powerful rename bot.\n\nUsing this bot you can rename and change thumbnail of your files.\n\nYou can also convert video to file and file to video.\n\nThis bot also supports custom thumbnail and custom caption.\n\nBot is made by @MrSagarBots""",
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton('⚚      BOT CHANNEL     ⚚', url='https://t.me/MrSagarBots')],
                     [InlineKeyboardButton('👨‍💻 OWNER', url='https://t.me/MrSagar0'),
                      InlineKeyboardButton('⚡️ PREMIUM PLANS ⚡️', callback_data="upgrade")]]))


@app.on_message((filters.private & (filters.document | filters.audio | filters.video)) | filters.channel & (
        filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = CHANNEL
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            await message.reply_text(
                f"""**{message.from_user.mention}**,\nDue to overload, only channel members can use me.""",
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔥  JOIN  UPDATE  CHANNEL  🔥", url=f"https://telegram.me/{update_channel}")]]))
            return
    try:
        bot_data = find_one(int(botid))
        prrename = bot_data['total_rename']
        prsize = bot_data['total_size']
        user_deta = find_one(user_id)
    except:
        await message.reply_text("Use About cmd first /about")
    try:
        used_date = user_deta["date"]
        buy_date = user_deta["prexdate"]
        daily = user_deta["daily"]
        user_type = user_deta["usertype"]
    except:
        await message.reply_text("database has been Cleared click on /start")
        return

    c_time = time.time()

    if user_type == "Free":
        LIMIT = 600
    else:
        LIMIT = 50
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
        await message.reply_text(f"**Sorry Dude I am not only for YOU \n Flood control is active so please wait for {ltime}**",
                                 reply_to_message_id=message.id)
    else:
        # Forward a single message
        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_["used_limit"]
        limit = used_["uploadlimit"]
        expi = daily - int(time.time())
        if expi > 0:
            await message.reply_text(
                f"""**You Have Used Your Daily Limit So Please Wait {expi} Seconds**""",
                reply_to_message_id=message.message_id)
            return
        elif used >= limit:
            await message.reply_text(
                f"""**You have Exceed Your Limit Of {humanbytes(limit)} So Please Upgrade Your Plan**""",
                reply_to_message_id=message.message_id)
            return
        else:
            await message.forward(chat_id=update_channel)
            uset = used + value
            used_limit(int(message.from_user.id), uset)
            add_date(int(message.from_user.id), int(time.time()))
            await message.reply_text(
                text=f"""**File Name :** `{filename}`\n**Size :** {humanbytes(file.file_size)}\n**Uploaded To :** {update_channel}\n**Your File Will Be Renamed And Forwarded Shortly**""",
                reply_to_message_id=message.message_id)


@app.on_message(filters.private & filters.command(["about"]))
async def about(client, message):
    await message.reply_text(
        text=f"""{wish} {message.from_user.mention}\n\nThis is an advanced and yet powerful rename bot.\n\nUsing this bot you can rename and change thumbnail of your files.\n\nYou can also convert video to file and file to video.\n\nThis bot also supports custom thumbnail and custom caption.\n\nBot is made by @MrSagarBots""",
        reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('⚚     BOT CHANNEL    ⚚', url='https://t.me/MrSagarBots')],
             [InlineKeyboardButton('👨‍💻 OWNER', url='https://t.me/MrSagar0'),
              InlineKeyboardButton('⚡️ PREMIUM PLANS ⚡️', callback_data="upgrade")]]))


@app.on_message(filters.private & filters.command(["update"]))
async def update(client, message):
    try:
        bot_data = find_one(int(botid))
        prrename = bot_data.get('total_rename', 0)
        prsize = bot_data.get('total_size', 0)
    except KeyError as e:
        print(f"KeyError: {e} - One or more keys are missing in bot_data")
        # Handle the missing keys gracefully or return an error message
        return

    # Assume new_rename and new_size are the updated values
    new_rename = 10  # Example new value for total_rename
    new_size = 1024  # Example new value for total_size

    # Update the total_rename and total_size in the database
    updatetotal(int(botid), new_rename, new_size)

    # Send a confirmation message
    await message.reply_text(f"Total Rename Updated: {new_rename}, Total Size Updated: {new_size}")


app.run()
