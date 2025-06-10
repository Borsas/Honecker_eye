from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext
from src.utils.env import  CHANNEL_ID, GROUP_ID


async def register(update: Update, context: CallbackContext) -> None:
    chat = await context.bot.get_chat(chat_id=update.message.chat_id)
    # Only care about private chats
    if chat.type != "private":
        return

    try:
        is_used_in_group = await context.bot.get_chat_member(chat_id=GROUP_ID, user_id=update.message.chat.id)
        if is_used_in_group.status in ["left", "kicked", "restricted"]:
            await context.bot.sendMessage(chat_id=update.message.chat_id, text="Was zum Teufel machst du da, du Spion?!")
            print("User {id} not in group".format(id=update.message.chat.id))
            return
    except Exception as e:
        print("User {id} not in group".format(id=update.message.chat.id))
        await context.bot.sendMessage(chat_id=update.message.chat_id, text="Was zum Teufel machst du da, du Spion?!")
        return

    try:    
        is_user_invited = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=update.message.chat.id)
        if is_user_invited.status == "member" or is_user_invited.status == "creator":
            await context.bot.sendMessage(chat_id=update.message.chat_id, text="Hölmö sä oot jo ryhmässä...")
            return
    except:
        # If error is thrown, user is not a member of the channel, so we ignore it and proceed
        pass

    expire_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
    invite = await context.bot.create_chat_invite_link(chat_id=CHANNEL_ID, expire_date=expire_date, member_limit=1, name="{id} kutsu".format(id=update.message.chat.id))
    await context.bot.sendMessage(chat_id=update.message.chat_id, text="Kutsu on voimassa 5 minuuttia. {invite}".format(invite=invite.invite_link))
