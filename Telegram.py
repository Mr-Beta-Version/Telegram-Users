from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'
group_id = input('Group ID Like -100424.. >> ')

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone_number)
    if await client.is_user_authorized() == False:
        try:
            await client.sign_in(phone_number)
        except SessionPasswordNeededError:
            password = input('Enter your 2FA password: ')
            await client.sign_in(password=password)
    
    try:
        group = await client.get_entity(int(group_id))

        
        async for member in client.iter_participants(group):
            username = member.username if member.username else 'No username'
            print(username)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

with client:
    client.loop.run_until_complete(main())
