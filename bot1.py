import random
import telebot

token = '123456789'

bot = telebot.TeleBot(token)

HELP = """
/help - напечатать справку по программе.
/add - добавить задачу в список (название задачи запрашиваем у пользователя).
/show - напечатать все добавленные задачи.
/random - выбрать рандомно задачу на сегодня.
/exit - покинуть программу. """


tasks = {}

def add_task(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
      tasks[date] = []
      tasks[date].append(task)



@bot.message_handler(commands = ['help','exit'])
def help_exit(message):
    command = message.text.split(maxsplit=2)[0]
    if command.lower() == 'exit':
        text = "Спасибо за использование! До свидания!"
    else:
        text = HELP
    bot.send_message(message.chat.id, text = text)


@bot.message_handler(commands=['show'])
def show(message):
    date = message.text.split(maxsplit=2)[1]
    if date in tasks:
        msg = f'На дату {date.upper()} назначены задачи: \n'
        for value in tasks[date]:
            msg += '\n' + value
    else:
        msg = "Задач на данную дату не выявлено!"
    bot.send_message(message.chat.id, text=msg)

@bot.message_handler(commands = ['add', 'random'])
def add(message):
    try:
        command = message.text.split(maxsplit=2)[0]
        if command == '/random':
            task = random.choice(list(tasks.values()))
            date = "Сегодня"
            msg = f'На дату {date} добавлена задача {task}'
        else:
            parts = message.text.split(maxsplit=2)
            if len(parts) < 3:
                msg = ("Ошибка: введены некорректные данные! \n"
                       "Формат запроса: /add дата задача")
            else:
                task = parts[2]
                date = parts[1]
                if len(task) <= 3:
                    msg = ("Ошибка: введены некорректные данные! \n"
                           "Задача меньше трёх символов!")

                else:
                    add_task(date, task)
                    msg = f'На дату {date} добавлена задача {task}'

    except ValueError:
        print("Ошибка: введены некорректные данные!")
        msg = "Ошибка: введены некорректные данные!"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda msg:True)
def handle_all_messages(message):
    bot.reply_to(message, "Напиши /help для справки")

bot.polling(non_stop=True)
