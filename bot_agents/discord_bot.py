import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import asyncio
import threading
import logging, os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('discord_bot_flask')

# Your Discord bot token (from the Developer Portal)
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
# Define the intents
# Define the intents
intents = discord.Intents.default()
intents.members = True

# Create a bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Create a Flask web server instance
app = Flask(__name__)

# Create a shared dictionary to store guild information
shared_guilds = {}

@app.route('/')
def index():
    return "Flask server is running!"

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')
    logger.info('Connected guilds:')
    shared_guilds.clear()
    for guild in bot.guilds:
        logger.info(f'- {guild.name} (ID: {guild.id})')
        shared_guilds[guild.id] = guild.name

@bot.command()
async def list_guilds(ctx):
    guilds_info = "\n".join([f'{guild.name} (ID: {guild.id})' for guild in bot.guilds])
    await ctx.send(f"Connected guilds:\n{guilds_info}")

# ... (keep your other bot commands)

@app.route('/create_group_chat', methods=['POST'])
def handle_create_group_chat():
    logger.debug('Received request at /create_group_chat')
    data = request.json
    logger.debug(f'Request data: {data}')
    
    guild_id = data.get('guild_id')
    channel_name = data.get('channel_name')
    usernames = data.get('usernames')
    message = data.get('message')

    if not all([guild_id, channel_name, usernames, message]):
        logger.error('Missing required fields in request')
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Find the guild by ID
        guild_id = int(guild_id)
        logger.debug(f'Searching for guild with ID: {guild_id}')
        logger.debug(f'Available guilds: {shared_guilds}')
        
        guild_name = shared_guilds.get(guild_id)

        if not guild_name:
            logger.error(f'Guild not found with ID: {guild_id}')
            return jsonify({'error': 'Guild not found'}), 404

        logger.info(f'Found guild: {guild_name} (ID: {guild_id})')

        # Schedule the create_channel_and_invite_users task
        asyncio.run_coroutine_threadsafe(
            create_channel_and_invite_users(guild_id, channel_name, usernames, message),
            bot.loop
        )

        return jsonify({'status': 'success', 'message': f'Creating channel {channel_name} in guild {guild_name}'}), 200
    except ValueError as e:
        logger.error(f'Invalid guild ID: {e}')
        return jsonify({'error': 'Invalid guild ID'}), 400
    except Exception as e:
        logger.error(f'Error in handle_create_group_chat: {e}')
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

async def create_channel_and_invite_users(guild_id, channel_name, usernames, message):
    try:
        guild = bot.get_guild(guild_id)
        if not guild:
            logger.error(f'Guild not found with ID: {guild_id}')
            return

        # Create a new private text channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        logger.info(f'Private channel {channel_name} created.')

        # Collect user objects and set permissions
        invited_users = []
        for username in usernames:
            user = discord.utils.get(guild.members, name=username)
            if user:
                await channel.set_permissions(user, read_messages=True, send_messages=True)
                invited_users.append(user)
                logger.info(f'Set permissions for user {username}.')
            else:
                logger.error(f'User {username} not found in guild {guild.name}')

        # Create mention string for each user
        mentions = ' '.join([user.mention for user in invited_users])

        # Send a welcome message to the channel, mentioning all invited users
        welcome_message = f"{mentions}\n{message}"
        await channel.send(welcome_message)
        logger.info(f'Sent welcome message to {channel_name}.')

        # Optionally, you can send an additional message to explain the purpose of the channel
        await channel.send(f"Welcome to {channel_name}! This is a private channel for: {', '.join(usernames)}.")

    except discord.Forbidden as e:
        logger.error(f'Forbidden error in create_channel_and_invite_users: {e}')
    except discord.HTTPException as e:
        logger.error(f'HTTP exception in create_channel_and_invite_users: {e}')
    except Exception as e:
        logger.error(f'Error in create_channel_and_invite_users: {e}')

def run_bot():
    bot.run(DISCORD_BOT_TOKEN)

def run_flask():
    app.run(port=5000)

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Run the Flask app in the main thread
    run_flask()