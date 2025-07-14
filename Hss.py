import re
import os
import asyncio
import random
import datetime
import requests
from telegraph import Telegraph
from telegram import Update, Chat as TGChat, Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
from telegram.constants import ParseMode
from telegram.ext import ContextTypes



Mawaidha1 = [-1001148345121, -1002102418633]

url_pattern = r'https?://\S+|www\.\S+'
mda = "<a href='https://t.me/Mawaidha1'>⏯︎ Mawaidha</a>"

Kata = re.compile(r"Subscribe|https|www|http")


# Tumafuta
Tumafuta = {
    -1001442754494,
    -1002188016623,
    -1001218366391,
    -1001377402220,
    -1001080236618,
    -1001248885302,
    -1001377245771,
    -1002617626917 # Dw
}  # Afya, Afya 02

# Mawaidha_ID
Mawaidha_ID = {
    -1001744919511,
    -1002059308786,
    -1001700358064,
    -1001989991539,
    -1001458515968
}

# AfyaChats (Kutoka channels kwenda Afya)
AfyaChats = {
    -1001939284397,
    -1002227098738
}

# Huduma_ID
Huduma_ID = {
    -1001673677756,
    -1001893767959,
    -1002151991495,
    -1002243599569
}

# News_Chat
News_Chat = {
    -1001656630081,
    -1002480315794,
    -1001958597227,
    -1002194874529,
    -1001332359386,
    -1001224159480,
    -1002467986859,
    -1002617626917 # Dw
}

# Mawaidha1
Mawaidha1 = {
    -1001148345121,
    -1002102418633
}

# Huduma
Huduma = {-1001297333544}




CHANNELS = {
    # Mawaidha_ID to Mawaidha1
    -1001744919511: [-1001148345121, -1002102418633],
    -1002059308786: [-1001148345121, -1002102418633],
    -1001700358064: [-1001148345121, -1002102418633],
    -1001989991539: [-1001148345121, -1002102418633],
    -1001458515968: [-1001148345121, -1002102418633],
    -1001860054816: [-1001148345121, -1002102418633],

    # AfyaChats to Afya channel
    -1001939284397: -1001080236618,
    -1002227098738: -1001080236618,

    # Huduma_ID to Huduma
    -1001673677756: -1001297333544,
    -1001893767959: -1001297333544,
    -1002151991495: -1001297333544,
    -1002243599569: -1001297333544,

    # News_Chat to HabariTz
    -1001656630081: -1001248885302,
    -1002480315794: -1001248885302,
    -1001958597227: -1001248885302,
    -1002194874529: -1001248885302,
    -1001332359386: -1001248885302,
    -1001224159480: -1001248885302,
    -1002467986859: -1001248885302
}

# Tuma media
async def tumia_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.channel_post or update.edited_channel_post
    if not message:
        return

    chat_id = message.chat.id
    target_channels = CHANNELS.get(chat_id, [])

    if not target_channels:
        return

    if not isinstance(target_channels, list):
        target_channels = [target_channels]

    caption = (await safisha(update, context) or "")[:1024]

    media_mapping = {
        "video": context.bot.send_video,
        "photo": context.bot.send_photo,
        "audio": context.bot.send_audio,
        "document": context.bot.send_document,
        "voice": context.bot.send_voice,
    }

    for channel in target_channels:
        for media_type, send_func in media_mapping.items():
            media = getattr(message, media_type, None)
            if media:
                file_id = media[-1].file_id if media_type == "photo" else media.file_id
                kwargs = {
                    "chat_id": channel,
                    media_type: file_id,
                    "caption": caption,
                    "parse_mode": "HTML"
                }
                asyncio.create_task(send_func(**kwargs))
                break


async def mbackup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = update.channel_post
        asyncio.create_task(context.bot.copy_message(chat_id=-1002102418633, from_chat_id=-1001148345121, message_id=message.id))
        return
    except Exception as e:
        error_msg = f"Kuna hitilafu imejitokeza kwenye mawaidha: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))


#send_media_group
async def send_media_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = update.message or update.channel_post
        if not message or not message.media_group_id:
            return
        chat_id = message.chat.id
        caption = (await safisha(update, context) or "")[:1024]

        # Hakikisha kuna channel za kutuma kutoka kwa CHANNELS
        target_channels = CHANNELS.get(chat_id)
        if not target_channels:
            return

        # Kama si list, ibadilishe kuwa list
        if not isinstance(target_channels, list):
            target_channels = [target_channels]

        # Hifadhi media group temporarily
        media_group = context.bot_data.setdefault(message.media_group_id, [])

        if message.photo:
            media_group.append(InputMediaPhoto(
                media=message.photo[-1].file_id,
                caption=caption if not media_group else None
            ))

        elif message.video:
            media_group.append(InputMediaVideo(
                media=message.video.file_id,
                caption=caption if not media_group else None
            ))

        # Hakikisha kuna zaidi ya 1 kabla ya kutuma
        if len(media_group) > 1:
            for channel in target_channels:
                asyncio.create_task(context.bot.send_media_group(chat_id=channel, media=media_group, parse_mode='HTML'))


            # Ondoa media_group baada ya kutuma
            del context.bot_data[message.media_group_id]

    except Exception as e:
        error_msg = f"Kuna hitilafu kwenye send_media_group: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))


'''Tech InstantView
Hii inashugulikia post zinazo tengenezwa na bot hii @CorsaBot'''
TCH_ID = [-1002151991495, -1002151991495]
async def onahss(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = update.edited_channel_post
        chat_ID = message.chat.id
        if message:
            text = message.text

            text = re.sub(r'from.*', '', text).strip()
            entities = message.entities
            url = entities[0]['url']
            if url:
                # Ongeza footer
                footer = "<blockquote>📨 @Huduma 👈</blockquote>"
                #kutoka kenda Afya
                if chat_ID == -1001354610614:
                    asyncio.create_task(context.bot.send_message(
                    chat_id=-1001080236618,
                    text=f"<a href='{url}'>{text}</a>",
                    parse_mode='HTML'
                ))
                elif chat_ID in TCH_ID:
                    asyncio.create_task(context.bot.send_message(
                    chat_id=-1001297333544,
                    text=f"<a href='{url}'>{text}</a>{footer}",
                    parse_mode='HTML'
                ))

    except Exception as e:
        error_msg = f"Kuna hitilafu imejitokeza kwenye function ya onahss: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))



# FIX url
async def fix_url(update, context):
    try:
        text = update.message.reply_to_message.text

        # Mapu ya links zinazohitaji kubadilishwa
        url_mappings = {
            r"https://x\.com": random.choice(["https://fxtwitter.com", "https://twittpr.com", "https://fixupx.com"]),
            r"https://twitter\.com": random.choice(["https://fxtwitter.com", "https://twittpr.com", "https://fixupx.com"]),
            r"instagram\.com": "ddinstagram.com",
            r"tiktok\.com": "vxtiktok.com",
        }

        # Angalia kama kuna URL yoyote inayohitajika kubadilishwa
        modified_text = text
        for pattern, replacement in url_mappings.items():
            modified_text = re.sub(pattern, replacement, modified_text)

        # Kama hakuna kilichobadilika, toa ujumbe wa hakuna link inayofaa
        if modified_text == text:
            await update.message.reply_text(text="No supported links found in the message.")
            return

        # Tuma meseji moja tu badala ya nyingi
        asyncio.create_task(context.bot.send_message(chat_id=update.effective_chat.id, text=modified_text))

    except Exception as e:
        error_msg = f"Kuna hitilafu imejitokeza kwenye function ya fix_url: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))


# safisha 1, 2, 3 inayoshughulikia amri tatu
async def safisha_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Pata user_id na jina la mtumiaji
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name

        message = update.message.reply_to_message
        command = update.message.text.split()[0]
        caption = message.caption or ""
        
        kata_list = re.compile(r'With ♡ @NRBOTS &')
        caption = kata_list.split(caption, maxsplit=1)[0]

        caption = REMOVE_NR_TAG.sub('', caption)
        caption = REMOVE_SAVED_BY.sub('', caption)
        caption = REMOVE_BOT_AND_EMOJIS.sub('', caption)
        caption = str(caption).lstrip("0123456789").strip()

        # Safisha caption kulingana na amri
        if command in ("/usafi1", "/usafi2"):
            caption = REMOVE_HASHTAGS.sub('', caption)
            caption = REMOVE_MENTIONS.sub('', caption)
            caption = REMOVE_LINKS.sub('', caption)
            caption = str(caption).lstrip("0123456789").strip()
            if command == "/usafi1":
                caption = replace_emoji(caption, replace="")

        elif command == "/usafi3":
            caption = caption.lstrip("0123456789").strip()


        # Tuma ujumbe uliosafishwa
        if message.video:
            asyncio.create_task(context.bot.send_video(chat_id=update.effective_chat.id, video=message.video.file_id, caption=caption[:1024]))
            return
        elif message.document:
            asyncio.create_task(context.bot.send_document(chat_id=update.effective_chat.id, document=message.document.file_id, caption=caption[:1024]))
            return
        elif message.audio:
            asyncio.create_task(context.bot.send_audio(chat_id=update.effective_chat.id, audio=message.audio.file_id, caption=caption[:1024]))
            return

    except Exception as e:
        # Tuma ujumbe wa hitilafu kwa mtumiaji
        error_msg = f"🧑‍💻 {user_name}, hitilafu imetokea wakati wa kusafisha caption yako. Hitilafu hiyo ni: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))




async def Copy_Tech(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = update.channel_post
        if not message.text:
            return  # Ruka kama si text

        if any(keyword in message.text for keyword in ["@NjiwaFLow", "@Njiwa_Store"]):
            return  # Ruka kama lina mojawapo ya maneno haya

        await context.bot.copy_message(
            chat_id=-1001297333544,
            from_chat_id=-1002243599569,
            message_id=message.message_id
        )

    except Exception as e:
        error_msg = f"Kuna hitilafu imejitokeza kwenye mawaidha: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))




'''View original post
hii inashugulikia post kotoka channels zoote'''
async def vop(caption, message, chat_id, update, context):
    try:
        entities = message.caption_entities
        url = entities[-1]['url']
        target_channels = CHANNELS.get(chat_id)
        if not target_channels:
            return

        # Hakikisha target_channels ni list
        if not isinstance(target_channels, list):
            target_channels = [target_channels]

        if "https://www.tiktok.com" in url or "https://www.instagram.com" in url:
            for channel in target_channels:
                await context.bot.copy_message(
                    chat_id=channel,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )

        elif "https://x.com" in url or "https://twitter.com" in url:
            matokeo = await ogpost(update, context)
            if matokeo:
                # Tunga ujumbe kulingana na chat_id
                if chat_id in AfyaChats:
                    ujumbe = f"{matokeo}\n\n👨‍🏫 @Jitibu 🤝"
                elif chat_id in Huduma_ID:
                    ujumbe = f"{matokeo}\n\n📨 @Huduma 🤝"
                elif chat_id in News_Chat:
                    ujumbe = f"{matokeo}\n\n️️➟ @HabariTz ✰✰✰"
                else:
                    ujumbe = matokeo


                for channel in target_channels:
                    asyncio.create_task(context.bot.send_message(
                        chat_id=channel,
                        text=ujumbe,
                        parse_mode="HTML"
                    ))
                    return


    except Exception as e:
        error_msg = f"Kuna hitilafu imejitokeza kwenye function ya vop 🧑‍💻: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))



#TUMA FUTA
async def Tuma_Futa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = update.message or update.channel_post
        if not message:
            return

        chat_id = message.chat.id
        caption = message.caption or ""

        # Kuzuia duplicate message deletion
        delete_message = False

        if any(keyword in caption for keyword in ["Saved by @", "Via @", "@Bot", "With ♡"]):
            caption = REMOVE_SAVED_BY.sub('', caption)
            caption = REMOVE_BOT_AND_EMOJIS.sub('', caption)
            kata_list = re.compile(r'With ♡ @NRBOTS &')
            caption = kata_list.split(caption, maxsplit=1)[0]
            
            if chat_id == -1001218366391:
                caption = caption.split("-----", 1)[0].strip()
            if message.video:
                asyncio.create_task(context.bot.send_video(chat_id=chat_id, video=message.video.file_id, caption=caption))

            if message.audio:
                asyncio.create_task(context.bot.send_audio(chat_id=chat_id, audio=message.audio.file_id, caption=caption))
                
            if message.photo:
                largest_photo = message.photo[-1]
                asyncio.create_task(context.bot.send_photo(
                    chat_id=chat_id,
                    photo=largest_photo.file_id,
                    caption=caption))

            delete_message = True

        elif "View original post" in caption and message.caption_entities:
            url = message.caption_entities[-1].url
            if "https://x.com" in url or "https://twitter.com" in url:
                matokeo = await ogpost(update, context)
                if matokeo:
                    channels = {
                        -1001080236618: f"🏥 {matokeo}\n\n👨‍🏫 @Jitibu 🤝",
                        -1001248885302: f"{matokeo}\n\n️️➟ @HabariTz ✰✰✰"
                    }
                    text = channels.get(chat_id, f"{matokeo}")
                    asyncio.create_task(context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML"))
                    delete_message = True

        if delete_message:
            asyncio.create_task(context.bot.delete_message(chat_id=chat_id, message_id=message.message_id))

    except Exception as e:
        error_msg = f"Kuna hitilafu kwenye Tuma_Futa: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))


ACCESS_TOKEN = "db68aebf906a685df785a07b31982ada92f7da8fd427e5b6140730c0edc9"
telegraph = Telegraph()
telegraph = Telegraph(access_token=ACCESS_TOKEN)

# Hifadhi content ya muda mfupi
cache = {}
async def hapohapo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        content = update.channel_post.text if update.channel_post else update.message.text
        if not content:
            return

        # Gawanya title na content
        title, content = (content.split("\n\n", 1) + [""])[:2]
        if not title or not content:
            return

        chat_id = update.effective_chat.id
        has_url = bool(re.search(r'http[s]?://\S+', content))

        if has_url:
            # Ikiwa kuna URL, angalia kama kuna content iliyohifadhiwa kwenye cache
            if chat_id in cache:
                cached_title, cached_content, _ = cache.pop(chat_id)
                content = f"{cached_content}\n\n{content}"  # Unganisha content zote
                title = cached_title  # Tumia title ya awali

            # Badilisha '\n' kuwa '<br>' kabla ya kutuma kwa Telegraph
            clean_content = content.replace('\n', '<br>')

            # Tengeneza ukurasa mpya wa Telegraph
            response = telegraph.create_page(
                title[:15], html_content=clean_content,
                author_name="Khamis", author_url="https://t.me/Mawaidha1"
            )
            page_path = response['path']

            # Hariri ukurasa mpya kwa content kamili
            response = telegraph.edit_page(
                path=page_path, title=title,
                html_content=clean_content,
                author_name="Khamis", author_url="https://t.me/Mawaidha1"
            )

            # Tuma ujumbe kwenye channels
            ujumbe1 = f"📚 {title}\nhttps://telegra.ph/{page_path}"
            for channel in Mawaidha1:
                asyncio.create_task(context.bot.send_message(chat_id=channel, text=ujumbe1))

        else:
            # Ikiwa haina URL, hifadhi content kwenye cache jinsi ilivyo
            cache[chat_id] = (title, content, None)

    except Exception as e:
        error_msg = f"Kuna hitilafu kwenye function ya hapohapo: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))





#OgPost
async def ogpost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.channel_post or update.edited_channel_post
        if not message:
            return

        content = message.caption or message.text or ""
        if not content:
            return

        entities = getattr(message, "caption_entities", message.entities) or []
        url = entities[-1].url if entities else ""

        if "https://x.com" in url or "https://twitter.com" in url:
            url_options = ["https://fxtwitter.com", "https://twittpr.com", "https://fixupx.com"]
            replaced_text = url.replace("https://x.com", random.choice(url_options)).replace(
                "https://twitter.com", random.choice(url_options)
            )

            first_line, *remaining = content.split("\n\n", 1) if "\n\n" in content else (content, "")
            cleaned_message = remaining[0].strip() if len(first_line.split()) <= 25 else content

            if cleaned_message:
                title = cleaned_message.split("\n")[0][:100]
                return f"<a href='{replaced_text}'>{title}</a>"

    except Exception as e:
        error_msg = f"Kuna hitilafu imejitokeza kwenye function ya ogpost: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))


x_urls = ["https://x.com", "https://twitter.com"]



# Sheria za kusafisha kwa kila chat ID
CHAT_CLEANING_RULES = {
    **{mawaidha: "mawaidha1" for mawaidha in Mawaidha_ID},
    -1001860054816: "private_mawaidha",  # Badilisha na ID halisi
    **{afya: "afya" for afya in AfyaChats},
    **{huduma: "huduma" for huduma in Huduma_ID},
    **{news: "news" for news in News_Chat},
}

# Kazi za kusafisha kwa kila aina ya chat
async def safisha_mawaidha1(caption, message):
    futa_Mlist = re.compile(r'Tube|_|--|FACEBOOK|Channel hii inahusika|Visit the post for more|https|WEBSITE')
    caption = futa_Mlist.split(caption, maxsplit=1)[0]
    return f"❖ @Mawaidha1\n\n{caption}" if message.media_group_id else f"<blockquote>❖ @Mawaidha1</blockquote>\n\n{caption}"

async def safisha_private_mawaidha(caption):
    caption = REMOVE_HASHTAGS.sub('', caption)
    caption = REMOVE_MENTIONS.sub('', caption)
    caption = REMOVE_LINKS.sub('', caption)
    caption = replace_emoji(caption, replace="")
    caption = caption.split("Tube", 1)[0]
    return f"❖ @Mawaidha1\n{caption}"

async def safisha_afya(caption):
    caption = REMOVE_HASHTAGS.sub('', caption)
    caption = re.split(r'Bonyeza', caption, maxsplit=1)[0]
    return f"👨‍🏫  @Jitibu\n\n{caption}"

async def safisha_huduma(caption, message):
    caption = re.split(r"Mind Warehouse|telegram", caption, 1)[0]
    huduma = "<a href='https://t.me/Huduma'>  〽︎ Teknolojia </a>"
    return f"@Huduma\n\n{caption[:500]}" if message.media_group_id else f"{huduma}\n\n{caption[:500]}"

async def safisha_news(caption, chat_id, update, context):
    if chat_id in {-1001332359386, -1001224159480}:  # BBC & DW
        asyncio.create_task(Tuma_Futa(update, context))
    caption = re.split(r'#dwkiswahili|Tembelea|If you find any|Step into the world|Check more here|Bonyeza link|Tufuate kwenye Ukurasa wetu', caption, 1)[0]
    return f"️️➟ @HabariTz ✰✰✰\n\n{caption}"

# Orodha ya kazi za kusafisha
CLEANING_FUNCTIONS = {
    "mawaidha1": safisha_mawaidha1,
    "private_mawaidha": safisha_private_mawaidha,
    "afya": safisha_afya,
    "huduma": safisha_huduma,
    "news": safisha_news,
}




# Compile patterns mara moja
REMOVE_NR_TAG = re.compile(r'With ♡ @NRBOTS &')
REMOVE_SAVED_BY = re.compile(r'(Saved by @|Via @)\w+', re.IGNORECASE)
REMOVE_BOT_AND_EMOJIS = re.compile(r'@BotYouTubeMusicBot\s*🎧')
REMOVE_HASHTAGS = re.compile(r'#\w+')
REMOVE_MENTIONS = re.compile(r'@\w+')
REMOVE_LINKS = re.compile(r'http\S+|www.\S+')


# Kazi kuu ya kusafisha
async def safisha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message or update.channel_post or update.edited_channel_post
        if message is None:
            return ""  # Hakuna message

        caption = message.caption or ""
        chat_id = message.chat.id

        # Kusafisha caption ya awali
        caption = REMOVE_NR_TAG.sub('', caption)
        caption = REMOVE_SAVED_BY.sub('', caption)
        caption = REMOVE_BOT_AND_EMOJIS.sub('', caption)
        caption = str(caption).lstrip("0123456789").strip()
        caption = Kata.split(caption, 1)[0]

        # Ondoa hashtags kama ni nyingi
        if caption.count("#") > 2:
            caption = REMOVE_HASHTAGS.sub('', caption)

        # Ondoa mistari mingi sana
        if chat_id in [-1001939284397, -1002467986859]:
            if len(re.findall(r'\n', caption)) > 10:
                caption = caption.split("\n\n", 1)[0]

        # Tafuta function inayohusika
        if chat_id in CHAT_CLEANING_RULES:
            function_key = CHAT_CLEANING_RULES[chat_id]
            clean_function = CLEANING_FUNCTIONS[function_key]

            # Weka hoja zinazohitajika kwa kila function
            function_args = {
                    "mawaidha1": (caption, message),
                    "huduma": (caption, message),
                    "news": (caption, chat_id, update, context),
                    }

            return await clean_function(*function_args.get(function_key, (caption,)))

        return caption  # Kama hakuna rule, rudisha caption asili

    except Exception as e:
        error_msg = f"Kuna hitilafu kwenye function ya safisha caption: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg)
        )
        return ""  # Rudisha string tupu kama kuna hitilafu




def replace_emoji(text, replace=""):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # Transport & map symbols
        u"\U0001F700-\U0001F77F"  # Alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric shapes
        u"\U0001F800-\U0001F8FF"  # Supplemental arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and pictographs extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed characters
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(replace, text)



async def xpost(update, context):
    try:
        message = update.channel_post
        if not message:
            return None

        chat_id = message.chat.id
        content = message.caption or message.text or ""
        if not content:
            return None

        entities = message.caption_entities if message.caption else message.entities or []
        url = entities[-1].url if entities else ""
        if not url or "status" not in url:
            await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
            return None

        if "https://x.com" in url or "https://twitter.com" in url:
            url_options = ["https://fxtwitter.com", "https://twittpr.com", "https://fixupx.com"]
            new_url = random.choice(url_options)
            replaced_text = url.replace("https://x.com", new_url).replace("https://twitter.com", new_url)

            parts = content.split("\n\n", 1)
            first_line = parts[0]
            remaining = parts[1] if len(parts) > 1 else ""
            cleaned_message = remaining.strip() if len(first_line.split()) <= 25 else content

            if cleaned_message:
                title = cleaned_message.split("\n")[0][:100]
                return f"<a href='{replaced_text}'>{title}</a>"

        return None

    except Exception as e:
        error_msg = f"Kuna hitilafu kwenye ogpost: {str(e)}"
        asyncio.create_task(context.bot.send_message(chat_id=-1002158955567, text=error_msg))  # Tumie background task
        return None


