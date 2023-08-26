import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client(
    "Mtumaji",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)



@app.on_message(filters.command(["id", 'hss']))
def send_id(client, message):
    # Kupata ID ya mtumiaji
    ID = message.chat.id
    
    # Kutuma ID ya mtumiaji kama jibu
    message.reply_text(f"ID yako ni <code>{ID}</code>")
		
						
	
Hamis = chat_id=-1001744919511
Mawaidha = chat_id=-1001148345121


@app.on_message(filters.chat(Hamis))
async def mawaidha(client, message):
 
 if message.video:
  video_file = message.video.file_id
  if message.caption is not None:
    message.caption = message.caption.replace("Saved by @InstantMediaBot", "❖ @Mawaidha1")
    message.caption = message.caption.replace("Saved by @download_it_bot", "❖ @Mawaidha1")

  video_caption = message.caption if message.caption else "@Mawaidha1"
  await client.send_video(chat_id=Mawaidha, video=video_file, caption=video_caption)
  
 

print('Alhamdulillah, bot On 𓁷')

app.run()
