import asyncio
import aiohttp
import json
import sys

class BlockGrab:
    def __init__(self, token):
        self.base_url = "https://discord.com/api/v9"
        self.token = token
        self.headers = {"Authorization": self.token, "Content-Type": "application/json"}
        self.session = None

    async def create_session(self):
        self.session = aiohttp.ClientSession()

    async def close_session(self):
        if self.session:
            await self.session.close()

    async def get_blocked_users(self):
        async with self.session.get(f"{self.base_url}/users/@me/relationships", headers=self.headers) as response:
            relationships = await response.json()
            return [r for r in relationships if r['type'] == 2]

    async def get_dm_channel(self, user_id):
        async with self.session.post(f"{self.base_url}/users/@me/channels", headers=self.headers, json={"recipient_id": user_id}) as response:
            return await response.json()

    async def get_messages(self, channel_id, limit=100):
        async with self.session.get(f"{self.base_url}/channels/{channel_id}/messages?limit={limit}", headers=self.headers) as response:
            return await response.json()

    async def process_blocked_user(self, user):
        user_id = user['id']
        username = user['user']['username']
        print(f"processing user: {username}")

        try:
            dm_channel = await self.get_dm_channel(user_id)
            channel_id = dm_channel['id']
            messages = await self.get_messages(channel_id)

            messages_filename = f"messages_{username}_{user_id}.json"
            with open(messages_filename, 'w') as f:
                json.dump(messages, f, indent=2)
            print(f"saved messages to {messages_filename}")

        except Exception as e:
            print(f"error processing user: {e}")

    async def run(self):
        await self.create_session()
        blocked_users = await self.get_blocked_users()

        if blocked_users:
            print("blocked users:")
            for i, user in enumerate(blocked_users):
                username = user['user']['username']
                print(f"{i+1}. {username}")

            print()
            while True:
                choice = input("enter the number of the blocked user to grab (leave empty for all, or 'exit' to quit): ")
                if choice.lower() == 'exit':
                    break
                if choice:
                    try:
                        index = int(choice) - 1
                        await self.process_blocked_user(blocked_users[index])
                    except (ValueError, IndexError):
                        print("invalid choice")
                else:
                    print(f"found {len(blocked_users)} blocked users")
                    await asyncio.gather(*[self.process_blocked_user(user) for user in blocked_users])
                    break
        else:
            print("no blocked users found")

        await self.close_session()

async def main():
    try:
        token = input("enter your discord token: ")
        grabber = BlockGrab(token)
        await grabber.run()
    except KeyboardInterrupt:
        print("\nexiting...")
    except Exception as e:
        print(f"error: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())