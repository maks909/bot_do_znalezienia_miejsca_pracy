import telebot
import os 
f = open(os.path.join(os.path.dirname(__file__), "TOKEN.ini"), "r", encoding="UTF-8")
bot = telebot.TeleBot(f.read())
f.close()
from random import*

obrazki_moje = []
for x in range(1,3):
    obraz = open(os.path.join(os.path.dirname(__file__), f"ja{x}.jpg"), "rb")
    obrazki_moje.append(obraz.read())
    obraz.close()

@bot.message_handler(commands=["start"])
def start(m, res=False):
    button_phone = telebot.types.KeyboardButton(text="Wysłać kontakt", request_contact=True)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_phone, "Wysłać dokument", "Otrzymać kontakt", "Otrzymać obraz", "Otrzymać CV")
    bot.send_message(m.chat.id, "Dzień dobry", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def contact(message):

    if message.contact is not None:
        p = open(os.path.join(os.path.dirname(__file__), "kontakty.txt"), "r")
        zapisywać = True
        text = p.read()
        for x in text:
            if message.contact.phone_number in x:
                zapisywać = False
        p.close()
        p = open(os.path.join(os.path.dirname(__file__), "kontakty.txt"), "a")
        if zapisywać == True:
            p.write("\n\n numer telefonu: %s \n imię: %s \n nazwisko: %s " % (message.contact.phone_number, message.contact.first_name, message.contact.last_name))
        p.close()
        print(zapisywać)

@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)
        print(type(message.contact))
        print('Name: ' + str(message.contact.first_name))
        text = 'Пользователь: ' + message.contact.first_name + ': телефон: ' + message.contact.phone_number
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types="text")
def text(m):
    if m.text == "Otrzymać kontakt":
        bot.send_contact(m.chat.id, '+375 44 794 7317', 'Максим', 'Кужальков') #(m.chat.id, "Wysyłam coś podobnego na to")    
    if m.text == "Otrzymać obraz":
        bot.send_photo(m.chat.id, choice(obrazki_moje))
    if m.text == "Otrzymać CV":
        plik = os.path.join(os.path.dirname(__file__), "CV.pdf")
        with open(plik, "rb") as CV:
            bot.send_document(m.chat.id, CV.read(), "plik CV")
    if m.text == "Wysłać dokument":
        bot.send_message(m.chat.id, "Proszę przeciągnąć plik z pomocą myszy do 'telegram' lub użyj załącznika")

@bot.message_handler(content_types="document")
def dokument(m):
    informacja_pliku = bot.get_file(m.document.file_id)
    zapisany_plik = bot.download_file(informacja_pliku.file_path)

    miejsce_zapisu = "Coś/telegram_bot/bot_do_znazezienia_miejsca_pobytu/pliki_od_ludzi/" + m.document.file_name
    with open(miejsce_zapisu, "wb") as nowy_plik:
        nowy_plik.write(zapisany_plik)
    bot.reply_to(m, "Dziękuję, ja zapisałem ten dokument do siebie")

bot.polling(none_stop=True, interval=0)