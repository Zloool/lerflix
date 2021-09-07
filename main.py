import logging
from random import randrange
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          RegexHandler, ConversationHandler, Job, Filters)
from netconnector import get_tasks
from settings import tgtoken, TIMER

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
REGISTER, GETMAIL, GETPASSWORD = range(3)
pclogin = ''
pcpass = ''
listnumber = ''
# users = dict()
updater = Updater(token=tgtoken)
jobqueue = updater.job_queue


def pccheck(context):
    global listnumber
    # pc = PostCardUser(pclogin, pcpass)
    number = get_tasks(pclogin, pcpass) #pc.loginToPC()
    job = context.job
    logger.info("Tasks number: %s" % number)

    if(listnumber != number):
        context.bot.sendMessage(job.context, text='You have currently ' + number +
                        ' unsed mails!')
        listnumber = number


def start(bot, update):
    bot.message.reply_text(
        text="Hi! I am bot, made for checking your PostCrossing account! Type /register to begin")
    # TODO perepisat
    return REGISTER


def error(bot,  error):
    logger.warn('Update "%s" caused error "%s"' % (bot, error))


def register(bot, update):
    # user = update.message.from_user
    bot.message.reply_text('Lets start! Give me your PostCrossing email, please:')
    return GETMAIL


def getmail(bot, update):
    global pclogin
    # user = update.message.from_user
    pclogin = bot.message.text
    bot.message.reply_text(
        'Okay, now give me your passwod(yep, thats tottaly insecure):')

    return GETPASSWORD


def getpassword(bot, update):
    global pcpass
    global listnumber
    # user = update.message.from_user
    pcpass = bot.message.text
    bot.message.reply_text('All done! Now i will check your ackount')

    # pc = PostCardUser(pclogin, pcpass)
    number = get_tasks(pclogin, pcpass) # pc.loginToPC()
    logger.info("Tasks number: %s" % number)
    if number:
        bot.message.reply_text('You have currently ' + number + ' unsed mails!')
    else:
        bot.message.reply_text('No new tasks.')

    listnumber = number
    chat_id = bot.message.chat_id
   # second_checker = Job(pccheck, 1800.0, context=chat_id)
    #job = Job(pccheck, 360.0, context=chat_id)
    jobqueue.run_repeating(pccheck, 60*TIMER-5+randrange(10), context=chat_id)
    return ConversationHandler.END


def cancel(bot, update):
    user = bot.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.REGISTER


def main():
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTER: [CommandHandler('register', register)],
            GETMAIL: [MessageHandler(Filters.text, getmail)],
            GETPASSWORD: [MessageHandler(Filters.text, getpassword)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()