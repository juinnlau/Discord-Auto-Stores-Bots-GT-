import discord
import asyncio
from pymongo import MongoClient
import dns.resolver
import json

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

# Read values from the 'config.json' file
with open('config.json') as config_file:
    config = json.load(config_file)

MONGODB_URL = config['mongodb_url']
DB_NAME = config['dbname']
COLLECTION_NAME = config['collection_name']
ALLOWED_DISCORD_IDS = config['allowed_discord_ids']
TOKEN = config['token']
COMMANDS = config['commands']
PACK_PRICES = config['pack_prices']

client = MongoClient(MONGODB_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def close_ticket(channel):
    await asyncio.sleep(20)  # Wait for 20 seconds
    await channel.delete()

def reset_database():
    collections = db.list_collection_names()
    for collection_name in collections:
        collection.delete_many({})
    print("Data in the Database has been successfully reset.")

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command_name = message.content.split()[0]

    if command_name in COMMANDS.values():
        if command_name == COMMANDS['addball']:
            if str(message.author.id) not in ALLOWED_DISCORD_IDS:
                await message.channel.send('Permission denied `.addball`.')
                return
        else:
            if not message.channel.name.startswith('ticket'):
                if command_name in [COMMANDS['set'], COMMANDS['buy']]:
                    await message.channel.send('This command can only be used in the Ticket channel.')
                    return
    else:
        if command_name not in COMMANDS.values():
            return

    if command_name == COMMANDS['set']:
        args = message.content.split()[1:]

        if len(args) == 1:
            growid = args[0].lower()
            existing_data = collection.find_one({'discord_id': str(message.author.id)})
            if existing_data:
                if existing_data['growid'] == growid:
                    await message.channel.send('GrowID is already in use.')
                else:
                    collection.update_one({'discord_id': str(message.author.id)}, {'$set': {'growid': growid}})
                    await message.channel.send(f'GrowID has been successfully changed to {growid}')
            else:
                data = {
                    'discord_id': str(message.author.id),
                    'growid': growid,
                    'balance': '0'
                }
                collection.insert_one(data)
                await message.channel.send(f'Successfully set GrowID: {growid}')
        else:
            await message.channel.send('Invalid number of arguments for .set command')

    elif command_name == COMMANDS['cleardata']:
        if str(message.author.id) in ALLOWED_DISCORD_IDS:
            reset_database()
            await message.channel.send('Data has been cleared')
        else:
            await message.channel.send('Permission denied.')

    elif command_name == COMMANDS['info']:
        existing_data = collection.find_one({'discord_id': str(message.author.id)})
        if existing_data:
            growid = existing_data['growid']
            balance = existing_data['balance']
            await message.channel.send(f'GrowID: {growid}\nBalance: {balance}')
        else:
            await message.channel.send('Data not found')

    elif command_name == COMMANDS['buy']:
        args = message.content.split()[1:]

        if len (args) == 2:
            packname = args[0].lower()
            amount = int(args[1])

            if packname not in PACK_PRICES:
                await message.channel.send(f'Packname `{packname}` is not valid.')
                return

            price = PACK_PRICES[packname]

            existing_data = collection.find_one({'discord_id': str(message.author.id)})
            if existing_data:
                balance = int(existing_data['balance'])
                if balance >= (price * amount):
                    new_balance = balance - (price * amount)
                    collection.update_one({'discord_id': str(message.author.id)}, {'$set': {'balance': str(new_balance)}})
                    await message.channel.send(f'Successfully purchased {amount} `{packname}`. Balance: {new_balance}')
                    ticket_channel = message.channel
                    await ticket_channel.send('Ticket will be closed in 20 seconds.')
                    asyncio.create_task(close_ticket(ticket_channel))
                else:
                    await message.channel.send('Sorry, your balance is insufficient.')
            else:
                await message.channel.send('Data not found')
        else:
            await message.channel.send('Invalid number of arguments for .buy command')

    elif command_name == COMMANDS['addball']:
        if len(message.content.split()) == 3:
            username = message.content.split()[1]
            amount = int(message.content.split()[2])

            mentioned_users = message.mentions
            if len(mentioned_users) > 0:
                discord_id = str(mentioned_users[0].id)
            else:
                await message.channel.send('Invalid user tag.')
                return

            existing_data = collection.find_one({'discord_id': discord_id})
            if existing_data:
                balance = int(existing_data['balance'])
                new_balance = balance + amount
                collection.update_one({'discord_id': discord_id}, {'$set': {'balance': str(new_balance)}})
                await message.channel.send(f'Successfully added {amount} balance to {username}. New balance: {new_balance}')
            else:
                await message.channel.send('Data not found')
        else:
            await message.channel.send('Invalid number of arguments for .addball command')

client.run(TOKEN)
