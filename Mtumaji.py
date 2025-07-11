#V 20.7
import re
import os
import Hss
import logging
import asyncio
import random
import requests
from telegram.constants import ParseMode
from telegram import Update, Chat as TGChat, Message
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from Hss import (
send_media_group,
tumia_media,
Tuma_Futa,
mbackup,
onahss,
hapohapo,
vop
)

from datetime import datetime, timedelta, timezone

#WebHook
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route


# Set timezone offset for Tanzania (UTC+3)
tz_offset = timezone(timedelta(hours=3))

URL = "https://perfect-willa-jihudumie1-ec4c16f8.koyeb.app/"
PORT = int(os.environ.get("PORT", 10000))
bot_token = "6136666252:AAGvIFrEJu9D1y93fa09y1joFdk8QHXE24Q"

# Kuanzisha logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)




#Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user.to_dict()

        tz_offset = timedelta(hours=3)  # Set the time zone offset for Tanzania (+3 hours from UTC)
        now = datetime.now() + tz_offset  # Get the current time in Tanzania

        muda = now.strftime("%I:%M:%S")  # Format the time as "%I:%M:%S" (e.g., "09:30:00")

        first_name = user['first_name']
        txt = f"Karibu, <u>{first_name}</u> Jiunge na \n1. @Mawaidha1\n2. @Jitibu\n3. @Huduma\nKwasasa ni Saa {muda} 🇹🇿"
        asyncio.create_task(context.bot.send_message(chat_id=user['id'], text=txt, parse_mode='HTML'))

    except Exception as e:
        # Handle exceptions and log or send error message
        error_msg = f"Kosa limetokea Kwenye function ya Start: {e}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))



CHANNEL_ID = -1002528346454  # Full Content
KWA = [-1002528346454, -1002227536883]


#TEXT
async def textzote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = update.channel_post or update.edited_channel_post
        chat_ID = message.chat.id

        # Orodha ya ID za Instant View
        InstantView_ID = [-1002151991495, -1001354610614, -1002151991495]

        # Dictionary ya CHAT IDs na functions
        CHATIDs = {
            -1001148345121: mbackup,
            -1001295876023: hapohapo,
            -1002012849938: hapohapo,
            -1002243599569: Hss.Copy_Tech
        }

        if chat_ID in InstantView_ID:
            if update.edited_channel_post:
                edit_time = message.edit_date
                now = datetime.now(tz_offset)  # Offset-aware datetime with UTC+3
                time_difference = now - edit_time

                if time_difference <= timedelta(hours=12):
                    asyncio.create_task(onahss(update, context))
                    return

        elif chat_ID in CHATIDs:
            asyncio.create_task(CHATIDs[chat_ID](update, context))
            return
            
        elif chat_ID == -1002528346454:  # Full Content
                if not message:
                    return
                if message.text:
                    matokeo = await Hss.xpost(update, context)
                    if matokeo:
                        for chat in KWA:
                            asyncio.create_task(context.bot.send_message(chat_id=chat, text=matokeo, parse_mode="HTML"))
                        return 

    except Exception as e:
        error_msg = f"Kosa limetokea Kwenye function ya Text tu: {e}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))


#Post kutoka channeli hizi 👇
Mawaidha_ID = {-1001744919511, -1002059308786, -1001700358064, -1001989991539, -1001458515968}

AfyaChats = {-1001939284397, -1002227098738}

Huduma_ID = {-1001673677756, -1001893767959, -1002151991495, -1002243599569}

News_Chat = {-1001656630081, -1002480315794, -1001958597227, -1002194874529, -1001332359386, -1001224159480, -1002467986859}

# Tumafuta
Tumafuta = {
    -1001442754494,  # Deep Web:
    -1002188016623,  # Maisha 💰🍷
    -1001377402220,  # Elimu Dunia 🐾
    -1001377245771,  # YouTube Upload group
    -1001852957171,  # Upload Media group
    -1001845127657,  # Quran group
    -1001632824805,  # Mawaidha1 group
    -1001218366391,  # Guiness World
    -1001080236618,  # AFYA YAKO LEO
    -1001248885302,  # Swahili News
    -1002117935045,  # Marafiki
    -1001898591688  # Bungonya
    
}


Ogpost_ID = {-1002456238597, -1001442754494}

#kwenda Channels Hizi 👇
Mawaidha1 = {-1001148345121, -1002102418633}

Huduma = -1001297333544


#MTUMAJI WA MEDIA ZOTE
banned_keywords = [
    "paripesa", "promo code", "whatsapp 0743 867 256",
    "boom shakalaka boom", "0743 867 256", "0743867256", "+255743867256",
    "1xbet", "code ::"
]
ALLOWED_USERS = {654648997}

#Mtumaji Media
async def mtumaji(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Chukua message kutoka kwenye update
        message = update.message or update.channel_post or update.edited_channel_post
        if not message:
            return

        chat_id = message.chat.id
        caption = message.caption or ""
        
        # Afya Uzima channel 
        if chat_id == -1001939284397:
            if message.document or message.audio:
                return
        

        # Hakiki kama ujumbe una media yoyote
        if any([message.video, message.photo, message.audio, message.document]):

            # Kama ujumbe umetoka kwenye channel maalum ya Full Content
            if chat_id == -1002528346454:
                matokeo = await Hss.xpost(update, context)
                if matokeo:
                    for chat in KWA:
                        asyncio.create_task(
                            context.bot.send_message(
                                chat_id=chat,
                                text=matokeo,
                                parse_mode="HTML"
                            )
                        )
                    return  # Tumemaliza kazi, tokeni

            # Kama caption ina "View original post"
            elif "View original post" in caption:
                if chat_id in Tumafuta:
                    asyncio.create_task(Tuma_Futa(update, context))
                else:
                    asyncio.create_task(vop(caption, message, chat_id, update, context))
                return

            # Kama ni media group (album ya picha n.k.)
            if message.media_group_id:
                asyncio.create_task(send_media_group(update, context))
                return

            # Kama chat iko kwenye Tumafuta
            elif chat_id in Tumafuta:
                asyncio.create_task(Tuma_Futa(update, context))
                return

            # Kwa ujumbe mwingine wowote wa media
            else:
                if chat_id == -1002194874529 and caption:
                    caption_lower = caption.lower()
                    if any(keyword in caption_lower for keyword in banned_keywords):
                        return
                asyncio.create_task(tumia_media(update, context))

    except Exception as e:
        error_msg = f"Kosa kuu limetokea Kwenye Function ya Mtumaji inayo husika na ATTACHMENT: {e}"
        asyncio.create_task(
            context.bot.send_message(chat_id=-1002158955567, text=error_msg)
        )
#Mwisho



#Usafi wa caption
async def usafishaji_cptn(update, context):
    try:
        umessage = update.message.reply_to_message
        chat_id = update.message.chat.id
        chat_id = [-1002158955567, chat_id]
        if not umessage:
            await update.message.reply_text("Amri hii inahitaji jibu (Reply Video, Audio n.k) kwa ujumbe wa Media.")
            return
        elif not umessage.caption:
            return

        elif umessage.caption:
            asyncio.create_task(Hss.safisha_caption(update, context))
        else:
            return

    except Exception as e:
        for user in chat_id:
            asyncio.create_task(context.bot.send_message(chat_id=user, text=f"Kuna tatizo limetokea wakati wa kusafisha caption kwa njia ya comaand: {e}"))



#FIXURL
async def replace_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        rmessage = update.message.reply_to_message

        # Hakikisha kuna ujumbe ulioreplyiwa
        if not rmessage:
            await update.message.reply_text(
                "Ni lazima u-reply command hii kwa URL au link ya:\n"
                "1. Twitter/X\n2. TikTok\n3. Instagram"
            )
            return
        
        if any(getattr(rmessage, media_type, None) for media_type in ["video", "audio", "photo"]):
            return

        # Hakikisha ujumbe una URL sahihi
        url_pattern = re.compile(r"https?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        if not url_pattern.match(rmessage.text):
            return

        asyncio.create_task(Hss.fix_url(update, context))

    except Exception as e:
        error_msg = f"Kuna hitilafu imejitokeza kwenye replace_link: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))



import traceback

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Pata ujumbe wa hitilafu kwa kifupi
        error_brief = "".join(traceback.format_exception_only(type(context.error), context.error)).strip()

        # Tuma hitilafu moja kwa moja kwenye Telegram
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=f"⚠️ Hitilafu: {error_brief}"))

    except Exception as e:
        # Ikiwa hata kutuma hitilafu kumesababisha tatizo, tuma ujumbe wa dharura
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=f"⚠️ Hitilafu ya dharura: {e}"))


async def main() -> None:

        app = Application.builder().token(bot_token).updater(None).build()
        
        async def telegram(request: Request) -> Response:
            """Shughulikia sasisho zinazoingia za Telegram kwa kuziweka kwenye `update_queue`"""
            await app.update_queue.put(
            Update.de_json(data=await request.json(),bot=app.bot))
            return Response()

        starlette_app = Starlette(
        routes=[
        Route("/telegram", telegram, methods=["POST"]),
        ])

        webserver = uvicorn.Server(
        config=uvicorn.Config(
        app=starlette_app,
        port=PORT,
        host="0.0.0.0",
        ))

        #Start
        app.add_handler(CommandHandler("start", start))

        #Mtumaji
        non_text_filters = filters.VIDEO | filters.PHOTO | filters.AUDIO | filters.Document.ALL & ~filters.TEXT
        text_tu = filters.TEXT & ~non_text_filters

        app.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.ATTACHMENT, mtumaji))
        
        app.add_handler(MessageHandler(filters.ChatType.SUPERGROUP & filters.ATTACHMENT, mtumaji))

        app.add_handler(MessageHandler(filters.ChatType.CHANNEL & text_tu, textzote))
      



        #Handle ya kusafisha Caption
        app.add_handler(CommandHandler(['usafi1', 'usafi2', 'usafi3'], usafishaji_cptn))


        app.add_handler(CommandHandler('fixurl', replace_link))



        app.add_error_handler(error_handler)


        # Run the bot until the user presses Ctrl-C
        await app.bot.set_webhook(url=f"{URL}/telegram")
        
        async with app:
            await app.start()
            await webserver.serve()
            await app.stop()





if __name__ == "__main__":
    asyncio.run(main())








