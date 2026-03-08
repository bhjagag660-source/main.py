# -*- coding: utf-8 -*-
import telebot
from telebot import types
import json
import os
from datetime import datetime
import time

TOKEN = "8694381551:AAH6APfePsmisywAYMRk9CnukF6WCNoask0"
bot = telebot.TeleBot(TOKEN)

# === SABITLER ===
BOT_USERNAME = "AhmetMarketBot"
YENI_ADMIN_USERNAME = "Hakikiyetsiz"
ADMINLER = ["8434939976", "8451593028"]
ZORUNLU_GRUP_ID = -1003525217103
ZORUNLU_GRUP_LINK = "https://t.me/+2YhZmp5RKD8xZjg8"

ZORUNLU_KANALLAR = [
    {"link": "https://t.me/+2YhZmp5RKD8xZjg8", "id": -1003525217103},
    {"link": "https://t.me/+ge4oDY3JKhc0Y2Yy", "id": -1003590768175}
]

URUNLER = {
    "pubg_hesap": {"ad": "Pubg Hesap", "fiyat": 10, "aciklama": "PUBG hesap teslim edilir."},
    "tiktok_hit": {"ad": "Tiktok Hit", "fiyat": 5, "aciklama": "Tiktok videonuz icin etkilesim."},
    "wp_no": {"ad": "Wp No", "fiyat": 12, "aciklama": "WhatsApp onayli numara."},
    "tg_no": {"ad": "Tg No", "fiyat": 20, "aciklama": "Telegram onayli numara."},
    "cpm_kesin": {"ad": "Cpm Kesin", "fiyat": 5, "aciklama": "CPM garantili hizmet."},
    "insta_eski": {"ad": "Insta Eski Kurulum", "fiyat": 7, "aciklama": "Eski kurulum Instagram hesabi."},
    "tiktok_yuksek_hit": {"ad": "Tiktok 2-10k Hit", "fiyat": 15, "aciklama": "Tiktok icin yuksek hit."},
    "wp_cekme_bot": {"ad": "Sinirsiz Wp Cekme Bot", "fiyat": 17, "aciklama": "Sinirsiz WP numara cekme botu."},
    "100_emoji": {"ad": "100 Emoji", "fiyat": 10, "aciklama": "100 adet emoji etkilesimi."},
    "pubg_buzdiyari": {"ad": "Pubg Buzdiyari Random", "fiyat": 15, "aciklama": "Buzdiyari garantili random hesap."},
    "blutv_giris": {"ad": "Blutv Kesin Giris", "fiyat": 8, "aciklama": "Kesin giris garantili BluTV hesabi."},
    "exxen_giris": {"ad": "Exxen Kesin Giris", "fiyat": 5, "aciklama": "Kesin giris garantili Exxen hesabi."},
    "netflix": {"ad": "Netflix", "fiyat": 6, "aciklama": "Netflix izleme profili/hesabi."},
    "valorant": {"ad": "Valorant", "fiyat": 10, "aciklama": "Valorant random hesap teslimi."},
    "live_civciv": {"ad": "Live Civciv", "fiyat": 10, "aciklama": "Canli civciv hizmeti."},
    "idefix_hit": {"ad": "Idefix Hit", "fiyat": 5, "aciklama": "Idefix icin hit gonderimi."},
    "disney_plus": {"ad": "Disney+", "fiyat": 5, "aciklama": "Disney+ hesap/profil erisimi."},
    "pubg_uc": {"ad": "Pubg UC", "fiyat": 8, "aciklama": "PUBG UC teslim edilir."}
}

if not os.path.exists("kullanicilar.json"):
    with open("kullanicilar.json", "w") as f:
        json.dump({}, f)

def load_users():
    try:
        with open("kullanicilar.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("kullanicilar.json", "w") as f:
        json.dump(data, f, indent=4)

def kanallarda_mi(user_id):
    for kanal in ZORUNLU_KANALLAR:
        try:
            member = bot.get_chat_member(kanal["id"], user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print("Kanal hata: " + str(e))
            return False
    return True

def grupta_mi(user_id):
    try:
        member = bot.get_chat_member(ZORUNLU_GRUP_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def ensure_user(uid, username=None, first_name=None):
    data = load_users()
    if uid not in data:
        data[uid] = {
            "puan": 0,
            "referans_veren": None,
            "referans_getirdigi": [],
            "referans_sayisi": 0,
            "username": username or "",
            "isim": first_name or "",
            "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "son_aktif": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "grup_kontrol": False,
            "satin_aldiklari": []
        }
        save_users(data)
    else:
        data[uid]["son_aktif"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if username:
            data[uid]["username"] = username
        if first_name:
            data[uid]["isim"] = first_name
        save_users(data)
    return data[uid]

def ana_menu(chat_id, yeni_kullanici=False):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for urun_id, urun in URUNLER.items():
        markup.add(types.InlineKeyboardButton(
            urun["ad"] + " - " + str(urun["fiyat"]) + " Puan",
            callback_data="urun_" + urun_id
        ))
    markup.add(
        types.InlineKeyboardButton("Puan Durumu", callback_data="puan_durumu"),
        types.InlineKeyboardButton("Referans Linkim", callback_data="ref_link")
    )
    markup.add(
        types.InlineKeyboardButton("Gruba Katil", url=ZORUNLU_GRUP_LINK),
        types.InlineKeyboardButton("Admin @" + YENI_ADMIN_USERNAME, url="https://t.me/" + YENI_ADMIN_USERNAME)
    )
    if yeni_kullanici:
        bot.send_message(
            chat_id,
            "*Hos Geldin!*\n\nUrunlerden satin alabilirsin:\n10 Tepki = 1 Puan\n50 Uye = 5 Puan\n\nButonlari kullanarak islem yapabilirsin:",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.send_message(chat_id, "*Ana Menu*\n\nIslem sec:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=["start"])
def start(message):
    uid = str(message.from_user.id)
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""
    args = message.text.split()
    referans_id = None
    if len(args) > 1:
        referans_id = args[1]
        if referans_id == uid:
            referans_id = None
    ensure_user(uid, username, first_name)
    data = load_users()
    if not grupta_mi(uid):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Gruba Katil", url=ZORUNLU_GRUP_LINK))
        markup.add(types.InlineKeyboardButton("Katildim Kontrol Et", callback_data="grup_kontrol"))
        bot.send_message(
            uid,
            "*ZORUNLU GRUP*\n\nBu botu kullanmak icin once gruba katilmalisin:\n\n" + ZORUNLU_GRUP_LINK,
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return
    if referans_id and data.get(uid) and data[uid].get("referans_veren") is None:
        ref_id = str(referans_id)
        if ref_id in data:
            data[ref_id]["puan"] = data[ref_id].get("puan", 0) + 1
            data[ref_id]["referans_sayisi"] = data[ref_id].get("referans_sayisi", 0) + 1
            if "referans_getirdigi" not in data[ref_id]:
                data[ref_id]["referans_getirdigi"] = []
            data[ref_id]["referans_getirdigi"].append(uid)
            data[uid]["referans_veren"] = ref_id
            try:
                bot.send_message(ref_id,
                    "*Yeni Referans Kazandin!*\n\n" + first_name + " senin referansinla katildi!\n+1 Puan kazandin!",
                    parse_mode="Markdown")
            except Exception as e:
                print("Bildirim hatasi: " + str(e))
        data[uid]["puan"] = data[uid].get("puan", 0) + 1
        data[uid]["referans_veren"] = referans_id
        save_users(data)
        ana_menu(uid, yeni_kullanici=True)
    else:
        ana_menu(uid)

@bot.callback_query_handler(func=lambda call: call.data == "grup_kontrol")
def grup_kontrol_callback(call):
    uid = str(call.from_user.id)
    if grupta_mi(uid):
        bot.answer_callback_query(call.id, "Gruba katilmissin! Devam edebilirsin.")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        ana_menu(uid)
    else:
        bot.answer_callback_query(call.id, "Hala gruba katilmadin!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("urun_"))
def urun_sec(call):
    uid = str(call.from_user.id)
    urun_id = call.data.replace("urun_", "")
    if urun_id not in URUNLER:
        bot.answer_callback_query(call.id, "Urun bulunamadi!")
        return
    urun = URUNLER[urun_id]
    data = load_users()
    user_data = data.get(uid, {"puan": 0})
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Onayla", callback_data="onayla_" + urun_id),
        types.InlineKeyboardButton("Iptal", callback_data="ana_menu_don")
    )
    bot.edit_message_text(
        "*" + urun["ad"] + "*\n\n" + urun["aciklama"] + "\n\nFiyat: " + str(urun["fiyat"]) + " Puan\nMevcut Puanin: " + str(user_data.get("puan", 0)) + "\n\nSatin almayi onayliyor musun?",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("onayla_"))
def urun_onayla(call):
    uid = str(call.from_user.id)
    urun_id = call.data.replace("onayla_", "")
    if urun_id not in URUNLER:
        bot.answer_callback_query(call.id, "Urun bulunamadi!")
        return
    urun = URUNLER[urun_id]
    data = load_users()
    if uid not in data:
        bot.answer_callback_query(call.id, "Kullanici bulunamadi!")
        return
    if data[uid]["puan"] < urun["fiyat"]:
        bot.answer_callback_query(call.id, "Yetersiz puan! Gerekli: " + str(urun["fiyat"]), show_alert=True)
        return
    data[uid]["puan"] -= urun["fiyat"]
    data[uid]["satin_aldiklari"] = data[uid].get("satin_aldiklari", []) + [{
        "urun": urun["ad"],
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fiyat": urun["fiyat"]
    }]
    save_users(data)
    for admin in ADMINLER:
        try:
            admin_markup = types.InlineKeyboardMarkup()
            admin_markup.add(types.InlineKeyboardButton(
                "@" + data[uid].get("username", "Kullanici"),
                url="tg://user?id=" + uid
            ))
            bot.send_message(
                admin,
                "*YENI SATIN ALMA*\n\nKullanici: " + data[uid].get("isim", "") + " (@" + data[uid].get("username", "yok") + ")\nID: `" + uid + "`\nUrun: " + urun["ad"] + "\nFiyat: " + str(urun["fiyat"]) + " Puan\nTarih: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                reply_markup=admin_markup,
                parse_mode="Markdown"
            )
        except:
            pass
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Urun Teslim", url="https://t.me/" + YENI_ADMIN_USERNAME))
    markup.add(types.InlineKeyboardButton("Ana Menu", callback_data="ana_menu_don"))
    bot.edit_message_text(
        "*Satin Alma Basarili!*\n\nUrun: " + urun["ad"] + "\nOdenen: " + str(urun["fiyat"]) + " Puan\nKalan Puan: " + str(data[uid]["puan"]) + "\n\nUrun teslimi icin @" + YENI_ADMIN_USERNAME + " ile iletisime gec!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id, "Satin alindi!")

@bot.callback_query_handler(func=lambda call: call.data == "puan_durumu")
def puan_durumu(call):
    uid = str(call.from_user.id)
    data = load_users()
    user_data = data.get(uid, {"puan": 0, "referans_sayisi": 0, "kayit_tarihi": "bilinmiyor"})
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Ana Menu", callback_data="ana_menu_don"))
    bot.edit_message_text(
        "*Puan Durumun*\n\nPuan: `" + str(user_data.get("puan", 0)) + "`\nReferans Sayisi: `" + str(user_data.get("referans_sayisi", 0)) + "`\nID: `" + uid + "`\nKayit: " + str(user_data.get("kayit_tarihi", "bilinmiyor")) + "\n\nSatin Aldiklarin: " + str(len(user_data.get("satin_aldiklari", []))) + " urun",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "ref_link")
def ref_link_callback(call):
    uid = str(call.from_user.id)
    link = "https://t.me/" + BOT_USERNAME + "?start=" + uid
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Paylas", url="https://t.me/share/url?url=" + link),
        types.InlineKeyboardButton("Ana Menu", callback_data="ana_menu_don")
    )
    bot.edit_message_text(
        "*Senin Referans Linkin:*\n\n`" + link + "`\n\nBu linki paylas, her katilan icin +1 puan kazan!\nNot: Katilanlar gruba katilmazsa puan gelmez.",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "ana_menu_don")
def ana_menu_don(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    ana_menu(call.message.chat.id)
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=["adminpaneli"])
def admin_panel(message):
    uid = str(message.from_user.id)
    if uid not in ADMINLER:
        bot.reply_to(message, "Bu komutu kullanma yetkin yok!")
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Tum Kullanicilar", callback_data="admin_kullanicilar"),
        types.InlineKeyboardButton("Puan Siralaması", callback_data="admin_siralama"),
        types.InlineKeyboardButton("Duyuru Gonder", callback_data="admin_duyuru"),
        types.InlineKeyboardButton("Son Satin Almalar", callback_data="admin_satinalmalar")
    )
    data = load_users()
    toplam_kullanici = len(data)
    toplam_puan = sum([k.get("puan", 0) for k in data.values()])
    bot.send_message(
        uid,
        "*Admin Paneli*\n\nToplam Kullanici: " + str(toplam_kullanici) + "\nToplam Puan: " + str(toplam_puan) + "\nAdmin: @" + YENI_ADMIN_USERNAME + "\n\nIslem sec:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_kullanicilar")
def admin_kullanicilar(call):
    uid = str(call.from_user.id)
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "Yetkin yok!")
        return
    data = load_users()
    mesaj = "*Son Kayit Olan Kullanicilar:*\n\n"
    kullanicilar = sorted(data.items(), key=lambda x: x[1].get("kayit_tarihi", ""), reverse=True)[:10]
    for k, v in kullanicilar:
        mesaj += "@" + v.get("username", "yok") + " | " + v.get("isim", "") + "\n"
        mesaj += "ID: `" + k + "` | " + str(v.get("puan", 0)) + " puan\n"
        mesaj += v.get("kayit_tarihi", "") + "\n--------------------\n"
    mesaj += "\nToplam: " + str(len(data)) + " kullanici"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Geri", callback_data="admin_geri"))
    bot.edit_message_text(mesaj, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_siralama")
def admin_siralama(call):
    uid = str(call.from_user.id)
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "Yetkin yok!")
        return
    data = load_users()
    kullanicilar = sorted(data.items(), key=lambda x: x[1].get("puan", 0), reverse=True)[:10]
    mesaj = "*En Zengin 10 Kullanici:*\n\n"
    for i, (k, v) in enumerate(kullanicilar, 1):
        mesaj += str(i) + ". @" + v.get("username", "yok") + " | " + str(v.get("puan", 0)) + " puan\n"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Geri", callback_data="admin_geri"))
    bot.edit_message_text(mesaj, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_satinalmalar")
def admin_satinalmalar(call):
    uid = str(call.from_user.id)
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "Yetkin yok!")
        return
    data = load_users()
    mesaj = "*Son Satin Almalar:*\n\n"
    sayac = 0
    for k, v in data.items():
        for urun in v.get("satin_aldiklari", [])[-3:]:
            if sayac >= 10:
                break
            mesaj += "@" + v.get("username", "yok") + "\n" + urun["urun"] + " | " + str(urun["fiyat"]) + " puan\n" + urun["tarih"] + "\n--------------------\n"
            sayac += 1
        if sayac >= 10:
            break
    if sayac == 0:
        mesaj += "Henuz satin alma yok."
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Geri", callback_data="admin_geri"))
    bot.edit_message_text(mesaj, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_duyuru")
def admin_duyuru(call):
    uid = str(call.from_user.id)
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "Yetkin yok!")
        return
    bot.edit_message_text(
        "*Duyuru Gonderme*\n\nGondermek istedigin metni yaz:\n(Iptal icin /iptal yaz)",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown"
    )
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, duyuru_gonder)
    bot.answer_callback_query(call.id)

def duyuru_gonder(message):
    uid = str(message.from_user.id)
    if uid not in ADMINLER:
        bot.reply_to(message, "Yetkin yok!")
        return
    if message.text == "/iptal":
        bot.reply_to(message, "Duyuru iptal edildi.")
        return
    duyuru_metni = message.text
    data = load_users()
    basarili, basarisiz = 0, 0
    for user_id in data:
        try:
            bot.send_message(user_id, duyuru_metni)
            basarili += 1
        except:
            basarisiz += 1
    bot.send_message(message.chat.id, "Duyuru Gonderildi!\nBasarili: " + str(basarili) + "\nBasarisiz: " + str(basarisiz))

@bot.callback_query_handler(func=lambda call: call.data == "admin_geri")
def admin_geri(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    admin_panel(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "admin_puan_ver")
def admin_puan_ver(call):
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "Puan gonderilecek kullanicinin ID numarasini yazin:")
    bot.register_next_step_handler(msg, puan_id_al)

def puan_id_al(message):
    target_id = message.text
    msg = bot.send_message(message.chat.id, "Gonderilecek puan miktarini rakamla yazin:")
    bot.register_next_step_handler(msg, lambda m: puan_yukle(m, target_id))

def puan_yukle(message, target_id):
    try:
        miktar = int(message.text)
        data = load_users()
        if target_id in data:
            data[target_id]["puan"] = data[target_id].get("puan", 0) + miktar
            save_users(data)
            bot.send_message(message.chat.id, target_id + " ID kullaniciya " + str(miktar) + " puan eklendi!")
            bot.send_message(target_id, "Admin tarafindan hesabiniza " + str(miktar) + " puan eklendi!")
        else:
            bot.send_message(message.chat.id, "Kullanici bulunamadi!")
    except ValueError:
        bot.send_message(message.chat.id, "Hata: Sadece sayi girin!")

from flask import Flask
from threading import Thread
app = Flask("")

@app.route("/")
def home():
    return "Bot 7/24 Aktif!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("Bot aktif basladi...")
    bot.infinity_polling()
            
