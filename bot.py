import time
import random
import os 
from instagrapi import Client
from openai import OpenAI

# ---------------- CONFIGURATION ----------------
INSTAGRAM_SESSION = "77647101665%3Ae8oIRC6X31Wmzz%3A21%3AAYjpBm8kP1BWC3MgOpQoV2IOaekaxFwOw0dvFGphYw"
OPENROUTER_API_KEY = "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"
BOT_USERNAME = "thin.gailee"


# Initialize clients
cl = Client()
cl.login_by_sessionid(INSTAGRAM_SESSION)

openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

WELCOME_MESSAGES = [
    "Hey {username}! 😘 You just made this chat 10x better 🔥",
    "A wild {username} appeared! 😍 Ready to have fun? 😜",
    "Look who slid into my DMs 👀 Welcome {username}! 😉",
    "{username}, you’re here! Let's make this chat interesting 😏",
]

GOODBYE_MESSAGES = [
    "Bye {username}! 😢 Don’t stay away too long 💕",
    "Peace out {username}! 😘 DM me again soon 🔥",
]

class InstaBot:
    def __init__(self):
        self.last_messages = {}

    def generate_response(self, message, username):
        prompt = f"""
        You're an Instagram bot with a cute, flirty, funny, savage GenZ personality 😜
        You respond short, playful, and emoji-filled.
        Message from @{username}: "{message}"
        Respond naturally (under 100 characters).
        """

        try:
            response = openai_client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message},
                ],
                max_tokens=100,
                temperature=0.9,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI Error: {e}")
            return "Oops, my sass glitched 😅 Try again?"

    def process_message(self, thread, msg):
        text = msg.text or ""
        sender = msg.user.username
        thread_id = thread.id

        if sender.lower() == BOT_USERNAME.lower():
            return

        if thread.users_count == 2 or f"@{BOT_USERNAME}" in text:
            reply = self.generate_response(text, sender)
            cl.direct_send(reply, thread_ids=[thread_id])
            print(f"Replied to @{sender}: {reply}")

    def monitor(self):
        print("🚀 InstaBot Running on Render (DM + Group Mode) 💬")
        while True:
            try:
                threads = cl.direct_threads()
                for thread in threads:
                    thread_id = thread.id
                    thread_detail = cl.direct_thread(thread_id)
                    messages = thread_detail.messages

                    for msg in messages:
                        if msg.id not in self.last_messages:
                            self.last_messages[msg.id] = True
                            self.process_message(thread, msg)

                if len(self.last_messages) > 1000:
                    self.last_messages = dict(list(self.last_messages.items())[-500:])

                time.sleep(8)

            except Exception as e:
                print(f"Error: {e}")
                time.sleep(20)

if __name__ == "__main__":
    bot = InstaBot()
    bot.monitor()
