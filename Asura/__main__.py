from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Asura import *

@Client.on_message(filters.command("banall") & filters.private)
async def banall_command_handler(client, message):
    # Send a confirmation message with an inline button
    chat_id = message.chat.id
    confirm_text = "Are you sure you want to ban all members from this chat?"
    confirm_button = InlineKeyboardButton("Yes, ban all", callback_data="confirm_banall")
    cancel_button = InlineKeyboardButton("Cancel", callback_data="cancel_banall")
    keyboard = InlineKeyboardMarkup([[confirm_button, cancel_button]])
    await client.send_message(chat_id, confirm_text, reply_markup=keyboard)

@Client.on_callback_query()
async def banall_callback_handler(client, query):
    chat_id = query.message.chat.id
    if query.data == "confirm_banall":
        await banall(chat_id)
        await query.answer("All members have been banned from this chat.")
    elif query.data == "cancel_banall":
        await query.answer("Ban all cancelled.")

async def banall(chat_id):
    members = []
    async for member in app.iter_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user.id)
            if len(members) == 100:
                try:
                    await app.ban_chat_members(chat_id, members)
                except Exception as e:
                    print(f"Failed to ban members: {str(e)}")
                members = []
    if members:
        try:
            await app.ban_chat_members(chat_id, members)
        except Exception as e:
            print(f"Failed to ban members: {str(e)}")

with app:
    app.run()
