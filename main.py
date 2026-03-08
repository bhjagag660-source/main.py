import telebot
from telebot.types import *
import json
import os
import time

TOKEN = "8694381551:AAGDXVrMM6cWRDJUpnIFyB0iWxkUkaBv9LE"

bot = telebot.TeleBot(TOKEN)

ADMINS = [8451593028, 8434939976]

KANAL1_ID = -1003525217103
KANAL1_LINK = "https://t.me/+2YhZmp5RKD8xZjg8"

KANAL2_ID = -1003590768175
KANAL2_LINK = "https://t.me/+ge4oDY3JKhc0Y2Yy"

LOG_CHANNEL = -1003706600695

DB_FILE = "db.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({
            "users": {},
            "banned": [],
            "stats": {
                "joins": 0,
                "purchases": 0
            }
        }, f)

def load_db():
    with open(DB_FILE) as f:
        data = json.load(f)

    if "users" not in data:
        data["users"] = {}

    if "banned" not in data:
        data["banned"] = []

    if "stats" not in data:
        data["stats"] = {"joins":0,"purchases":0}

    return data

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(uid):

    db = load_db()

    uid = str(uid)

    if uid not in db["users"]:

        db["users"][uid] = {
            "ref": 0,
            "invited": None,
            "join_time": int(time.time()),
            "purchases": 0
        }

        db["stats"]["joins"] += 1

        save_db(db)

    return db["users"][uid]

def update_user(uid, datau):

    db = load_db()

    db["users"][str(uid)] = datau

    save_db(db)

def is_banned(uid):

    db = load_db()

    return uid in db["banned"]

def ban_user(uid):

    db = load_db()

    if uid not in db["banned"]:

        db["banned"].append(uid)

        save_db(db)

def unban_user(uid):

    db = load_db()

    if uid in db["banned"]:

        db["banned"].remove(uid)

        save_db(db)

def check_join(uid):

    try:

        s1 = bot.get_chat_member(KANAL1_ID, uid).status
        s2 = bot.get_chat_member(KANAL2_ID, uid).status

        if s1 in ["member","administrator","creator"] and s2 in ["member","administrator","creator"]:

            return True

    except:
        pass

    return False

def join_keyboard():

    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton("KANAL 1", url=KANAL1_LINK))

    kb.add(InlineKeyboardButton("KANAL 2", url=KANAL2_LINK))

    kb.add(InlineKeyboardButton("Kontrol", callback_data="join_check"))

    return kb

def main_menu():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.row("🛒 Market")

    kb.row("👤 Profil","👥 Referans")

    kb.row("👑 Liderlik")

    kb.row("⚙️ Admin")

    return kb

PRODUCTS = {
"urun1":10,
"urun2":5,
"urun3":10,
"urun4":20,
"urun5":5,
"urun6":7,
"urun7":13,
"urun8":17,
"urun9":10,
"urun10":15,
"urun11":8,
"urun12":5,
"urun13":6,
"urun14":10,
"urun15":10,
"urun16":5,
"urun17":15,
"urun18":25,
"urun19":7,
"urun20":20,
"urun21":5,
"urun22":25
}

PRODUCT_NAMES = {
"urun1":"Pubg hesap",
"urun2":"Tiktok hit",
"urun3":"WhatsApp numara",
"urun4":"Telegram numara",
"urun5":"Car parking",
"urun6":"Instagram hit",
"urun7":"Tiktok takipçi",
"urun8":"WhatsApp bot",
"urun9":"100 emoji",
"urun10":"Pubg random",
"urun11":"BluTV",
"urun12":"Exxen",
"urun13":"Netflix",
"urun14":"Valorant",
"urun15":"Live civciv",
"urun16":"İdefix",
"urun17":"40k civciv",
"urun18":"Telegram OTP",
"urun19":"Pubg UC",
"urun20":"Pubg 8100 UC",
"urun21":"Steam",
"urun22":"200₺ Play Kod"
}

def market_keyboard():

    kb = InlineKeyboardMarkup()

    for key in PRODUCTS:

        price = PRODUCTS[key]

        name = PRODUCT_NAMES[key]

        kb.add(InlineKeyboardButton(f"{name} - {price} ref", callback_data=key))

    return kb

@bot.message_handler(commands=['start'])
def start(message):

    uid = message.from_user.id

    if is_banned(uid):
        return

    if not check_join(uid):

        bot.send_message(uid,"Kanallara katıl",reply_markup=join_keyboard())

        return

    args = message.text.split()

    user = get_user(uid)

    if len(args) > 1:

        ref = args[1]

        db = load_db()

        if ref != str(uid) and user["invited"] is None:

            if ref in db["users"]:

                db["users"][ref]["ref"] += 1

                user["invited"] = ref

                db["users"][str(uid)] = user

                save_db(db)

    bot.send_message(uid,"Hoşgeldin",reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 Market")
def open_market(m):

    bot.send_message(m.chat.id,"Market",reply_markup=market_keyboard())

@bot.message_handler(func=lambda m: m.text == "👤 Profil")
def profile(m):

    user = get_user(m.from_user.id)

    text = f"""
ID: {m.from_user.id}
Ref: {user['ref']}
Satın alma: {user['purchases']}
"""

    bot.send_message(m.chat.id,text)

@bot.message_handler(func=lambda m: m.text == "👥 Referans")
def ref_link(m):

    uid = m.from_user.id

    link = f"https://t.me/{bot.get_me().username}?start={uid}"

    bot.send_message(uid,link)

@bot.message_handler(func=lambda m: m.text == "👑 Liderlik")
def leaderboard(m):

    db = load_db()

    users = db["users"]

    ranking = sorted(users.items(),key=lambda x:x[1]["ref"],reverse=True)[:20]

    text = "🏆 TOP 20\n"

    i = 1

    for u in ranking:

        text += f"{i}. {u[0]} - {u[1]['ref']} ref\n"

        i += 1

    bot.send_message(m.chat.id,text)

@bot.message_handler(func=lambda m: m.text == "⚙️ Admin")
def admin_panel(m):

    if m.from_user.id not in ADMINS:
        return

    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton("📊 İstatistik",callback_data="admin_stats"))

    kb.add(InlineKeyboardButton("🚫 Ban",callback_data="admin_ban"))

    kb.add(InlineKeyboardButton("♻️ Unban",callback_data="admin_unban"))

    kb.add(InlineKeyboardButton("📢 Duyuru",callback_data="admin_broadcast"))

    bot.send_message(m.chat.id,"Admin Panel",reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):

    uid = call.from_user.id

    if call.data == "join_check":

        if check_join(uid):

            bot.send_message(uid,"Doğrulandı",reply_markup=main_menu())

        else:

            bot.answer_callback_query(call.id,"Kanallara katıl")

    if call.data in PRODUCTS:

        user = get_user(uid)

        price = PRODUCTS[call.data]

        name = PRODUCT_NAMES[call.data]

        if user["ref"] < price:

            bot.answer_callback_query(call.id,"Yetersiz ref")

            return

        user["ref"] -= price

        user["purchases"] += 1

        update_user(uid,user)

        db = load_db()

        db["stats"]["purchases"] += 1

        save_db(db)

        bot.send_message(uid,f"Satın aldınız: {name}")

        for admin in ADMINS:

            bot.send_message(admin,f"Yeni satın alma\nUser:{uid}\nÜrün:{name}")

        try:

            bot.send_message(LOG_CHANNEL,f"SATIN ALMA {uid} {name}")

        except:
            pass

    if call.data == "admin_stats":

        if uid not in ADMINS:
            return

        db = load_db()

        users = len(db["users"])

        joins = db["stats"]["joins"]

        purchases = db["stats"]["purchases"]

        text = f"""
Kullanıcı: {users}
Toplam giriş: {joins}
Satın alma: {purchases}
"""

        bot.send_message(uid,text)

print("BOT ÇALIŞIYOR")

bot.infinity_polling()
