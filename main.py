#!/usr/bin/python3
import logging
from random import randrange
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from netconnector import get_tasks

from settings import tgtoken, TIMER, username, password

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
listnumber = -1
current_timer = TIMER




async def pccheck(context):
    global listnumber
    number = get_tasks() #pc.loginToPC()
    logger.info("Tasks number: %s" % number)
    message = 'You have currently ' + str(number) +' unsed mails!'

    if(listnumber != number):
        await context.bot.sendMessage(chat_id=context.job.chat_id, text=message)
        listnumber = number


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)



async def start_polling(update, context):
    # Getting chat id to let job know who to notify 
    chat_id = update.message.chat_id
    # setting job interval, converting interval from minutes to seconds
    interval = 60*TIMER-5+randrange(10)
    # doing a forced first check on launch
    context.job_queue.run_once(pccheck, 1, chat_id=chat_id, name=str(chat_id))
    # adding repeating job
    context.job_queue.run_repeating(pccheck, interval, chat_id=chat_id, name=str(chat_id))
    
    message = 'All done! Now i will check your ackount'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


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
    application = ApplicationBuilder().token(tgtoken).build()

    start_handler = CommandHandler('start', start_polling)
    application.add_handler(start_handler)
    application.run_polling()

if __name__ == '__main__':
    main()