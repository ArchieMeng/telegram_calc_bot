from multiprocessing import Process, Manager, Value
import telegram
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
from telegram import InlineQueryResultArticle, InputTextMessageContent

from calc import calc


COMMAND_HANDLERS = []


def set_command_handler(
        command,
        filters=None,
        allow_edited=False,
        pass_args=False,
        pass_update_queue=False,
        pass_job_queue=False,
        pass_user_data=False,
        pass_chat_data=False
):
    def decorate(func):
        COMMAND_HANDLERS.append(
            CommandHandler(
                command=command,
                callback=func,
                filters=filters,
                allow_edited=allow_edited,
                pass_args=pass_args,
                pass_update_queue=pass_update_queue,
                pass_job_queue=pass_job_queue,
                pass_user_data=pass_user_data,
                pass_chat_data=pass_chat_data
            )
        )
        return func

    return decorate


def calculate_impl(formula, result: Value, error: Value):
    try:
        result.value = str(calc(formula))
    except Exception as e:
        result.value = e.args[0]
        error.value = True


def get_result(formula):
    with Manager() as manager:
        result = manager.Value('s', " ")
        error = manager.Value('b', False)
        process = Process(target=calculate_impl, args=(formula, result, error))
        process.start()
        process.join(0.5)
        if process.is_alive():
            process.terminate()
            result = "Time limit exceeded"
            title = result
        else:
            title = "result"
            if error.value:
                result = result.value
            else:
                result = formula + '=' + result.value
    return result, title


@set_command_handler('calc', pass_args=True, allow_edited=True)
@run_async
def calculate(bot: telegram.Bot, update: telegram.Update, args):
    def send_message(text):
        message = update.message or update.edited_message
        chat_id = message.chat_id
        message_id = message.message_id
        if update.message:
            bot.send_message(
                chat_id=chat_id,
                reply_to_message_id=message_id,
                text=text
            )
        else:
            # on edited received
            message.reply_text(text)

    if args:
        formula = ''.join(args)
        send_message(get_result(formula)[0])
    else:
        send_message("Usage: /calc <formula>. Currently, +-*/()^ operator is supported")


@run_async
def inline_calc(bot, update):
    query = update.inline_query.query
    if not query:
        return

    results = list()
    formula = query.replace(' ', '')
    result, title = get_result(formula)

    results.append(
        InlineQueryResultArticle(
            id=formula,
            title=title,
            input_message_content=InputTextMessageContent(result)
        )
    )

    bot.answer_inline_query(update.inline_query.id, results)
