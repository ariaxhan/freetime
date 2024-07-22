from telegram import Bot, ChatPermissions, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Bot token from BotFather
BOT_TOKEN = "7429609114:AAF6PeZpDx171F48b3bbaGcD515qtDPetxY"

# Bot's own user ID
BOT_USER_ID = 'FreeTime_scheduler_bot'  # Replace this with your bot's actual user ID

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /create_group <group_name> to create a group.')

def create_group(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != int(BOT_USER_ID):
        update.message.reply_text("You are not authorized to create a group.")
        return

    if context.args:
        group_name = ' '.join(context.args)
        bot: Bot = context.bot
        
        # Create a new group chat with the bot as an admin
        new_chat = bot.create_chat(group_name, context.bot.id)
        chat_id = new_chat.id
        
        # List of user IDs to add to the group
        user_ids = ['user_id1', 'user_id2']  # Replace with actual user IDs
        
        for user_id in user_ids:
            bot.add_chat_members(chat_id, [user_id])
        
        update.message.reply_text(f'Group "{group_name}" created and users added.')
    else:
        update.message.reply_text('Please provide a group name.')

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create_group", create_group))
    
    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()