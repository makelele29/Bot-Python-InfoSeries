# -*- coding: utf-8 -*-
__author__ = 'Javier Castillo'

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters,CallbackQueryHandler
import logging
import re
import requests
from bs4 import BeautifulSoup
import themoviedb
import sensacine
import mongo
import os
clave=os.environ["TOKEN"]
bot = telegram.Bot(token=clave)
updater = Updater(token=clave)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def callback(bot,update):
    d=mongo.show(update.callback_query.message.chat_id)
    if re.match("^c[1-9][0-9]?x[1-9][0-9]*",update.callback_query.data) is not None:
        serie=update.callback_query.data.replace("c","").split("x")
        data="Temporada "+serie[0]+ " Capitulo "+serie[1]
        if d['message']!=update.callback_query.message.message_id:
            mongo.update(d['id'],update.callback_query.message.message_id)
            bot.sendMessage(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id, text=data)
        else:
            bot.editMessageText(chat_id=update.callback_query.message.chat_id,message_id=(update.callback_query.message.message_id+1), text=data)
    elif re.match("^t[1-9][0-9]?",update.callback_query.data) is not None:
        temporada=themoviedb.seriesdb()
        temporada.season(d['enlace'],update.callback_query.data.replace("t",""))
        botones=[]
        botones.append([telegram.InlineKeyboardButton("atras", callback_data="temporadas")])
        fil=[]

        for i in range (1,(temporada.season(d['enlace'],update.callback_query.data.replace("t",""))+1)):
            fil.append(telegram.InlineKeyboardButton(str(i), callback_data="c"+update.callback_query.data.replace("t","")+"x"+str(i)))
            if i%8==0:
                botones.append(fil)
                fil=[]
        if fil:
            botones.append(fil)
        reply_markup = telegram.InlineKeyboardMarkup(botones)
        bot.editMessageText(chat_id = update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,
        text = "Que episodio quieres?", reply_markup=reply_markup)

    elif update.callback_query.data=="0":
        reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("Sinopsis", callback_data='overview'),
         telegram.InlineKeyboardButton("Estado", callback_data="status"),
         telegram.InlineKeyboardButton("Duración", callback_data="duracion")],
         [telegram.InlineKeyboardButton("Temporadas", callback_data="temporadas")]])

        bot.editMessageText(chat_id = update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,
        text = "Que quieres saber?", reply_markup=reply_markup)
    elif update.callback_query.data!="temporadas":
        data=d[update.callback_query.data]
        if d['message']!=update.callback_query.message.message_id:
            mongo.update(d['id'],update.callback_query.message.message_id)
            bot.sendMessage(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id, text=data)
        else:
            bot.editMessageText(chat_id=update.callback_query.message.chat_id,message_id=(update.callback_query.message.message_id+1), text=data)

    else:
        botones=[]
        botones.append([telegram.InlineKeyboardButton("atras", callback_data="0")])
        fil=[]

        for i in range (1,(d[update.callback_query.data]+1)):
            fil.append(telegram.InlineKeyboardButton("Temporada "+str(i), callback_data="t"+str(i)))
            if i%3==0:
                botones.append(fil)
                fil=[]
        if fil:
            botones.append(fil)
        reply_markup = telegram.InlineKeyboardMarkup(botones)
        bot.editMessageText(chat_id = update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,
        text = "Que temporada eligiras?", reply_markup=reply_markup)
def serie(bot, update,args):
    if len(args)==1:

        mongo.insertar(update.message,args[0])
        serie=themoviedb.seriesdb(args[0])
        bot.sendPhoto(chat_id=update.message.chat_id,photo=serie.image())
        reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("Sinopsis", callback_data='overview'),
         telegram.InlineKeyboardButton("Estado", callback_data="status"),
         telegram.InlineKeyboardButton("Duración", callback_data="duracion")],
         [telegram.InlineKeyboardButton("Temporadas", callback_data="temporadas")]])

        bot.sendMessage(chat_id = update.message.chat_id,
        text = "Que quieres saber?", reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="El formato es /serie nombre_serie")

echo_handler = MessageHandler(Filters.text, echo)
serie_handler = CommandHandler('serie', serie,pass_args=True)
dispatcher.add_handler(serie_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CallbackQueryHandler(callback))


updater.start_polling()
updater.idle()
