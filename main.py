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
current_timer = TIMER

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
    context.job_queue.run_repeating(pccheck, 60*current_timer, context=chat_id, name=str(chat_id))
    return ConversationHandler.END

def change_timer(update, context: CallbackContext):

    try:
        chat_id = update.message.chat_id
        new_time = float(context.args[0])
        
        if new_time < 0:
            update.message.reply_text("Мало)")
            return
        current_timer = new_time
        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        if not current_jobs:
            pass
        for job in current_jobs:
            job.schedule_removal()

        update.message.reply_text("Інтервал змінений на: " + str(new_time))
        logger.info("Інтервал змінений на: %s", new_time)
        context.job_queue.run_once(pccheck, 1, context=chat_id, name=str(chat_id))
        context.job_queue.run_repeating(pccheck, 60*current_timer, context=chat_id, name=str(chat_id))
        
    except (IndexError, ValueError):
        update.message.reply_text("Синтаксис: /set <minutes>")
    
    return




def main():
    dispatcher = updater.dispatcher
    # application = Application.builder().token(tgtoken).build()

    # Bot start procedure
    dispatcher.add_handler(CommandHandler('start', start_polling))

    # Change time
    dispatcher.add_handler(CommandHandler('set', change_timer))
    # dispatcher.add_error_handler(error_callback)

    dispatcher.add_error_handler(error_callback)

    # updater.run_polling()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()