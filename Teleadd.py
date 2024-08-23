from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, UserPrivacyRestrictedError, PeerFloodError, UserAlreadyParticipantError
from telethon.tl.functions.channels import InviteToChannelRequest

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'
group_id = input('Group ID or Username >> ')
users_to_add = input('Enter usernames or IDs Without @ (comma-separated) >> ').split(',')

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone_number)
    
    # Handle 2FA if enabled
    if not await client.is_user_authorized():
        try:
            await client.sign_in(phone_number)
        except SessionPasswordNeededError:
            password = input('Enter your 2FA password: ')
            await client.sign_in(password=password)
    
    try:
        group = await client.get_entity(group_id)

        for user in users_to_add:
            try:
                user_entity = await client.get_entity(user.strip())
                await client(InviteToChannelRequest(group, [user_entity]))
                print(f"Added {user_entity.username or user_entity.id} to the group")
            except UserAlreadyParticipantError:
                print(f"{user} is already in the group")
            except UserPrivacyRestrictedError:
                print(f"Cannot add {user} due to privacy settings")
            except PeerFloodError:
                print("Flood error! Too many requests. Try again later.")
                break
            except Exception as e:
                print(f"Failed to add {user}: {e}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

with client:
    client.loop.run_until_complete(main())
