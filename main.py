#!/usr/bin/python3
import logging
from random import randrange
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          RegexHandler, ConversationHandler, Job, 
                          Filters, CallbackContext)
from netconnector import get_tasks
from settings import tgtoken, TIMER, username, password

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
listnumber = -1

updater = Updater(token=tgtoken, use_context=True)


def pccheck(context: CallbackContext):
    global listnumber
    # pc = PostCardUser(pclogin, pcpass)
    number = get_tasks() #pc.loginToPC()
    job = context.job
    logger.info("Tasks number: %s" % number)

    if(listnumber != number):
        context.bot.sendMessage(job.context, text='You have currently ' + str(number) +
                        ' unsed mails!')
        listnumber = number


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def start_polling(update, context: CallbackContext):
    update.message.reply_text('All done! Now i will check your ackount')

    chat_id = update.message.chat_id
    context.job_queue.run_once(pccheck, 1, context=chat_id, name=str(chat_id))
    context.job_queue.run_repeating(pccheck, 60*TIMER-5+randrange(10), context=chat_id, name=str(chat_id))
    return ConversationHandler.END



def main():
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_polling))
    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()