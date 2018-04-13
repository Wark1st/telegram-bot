import random
import requests
import sys
import os
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from PersonClass import Man
from question1 import Questions

peopl = dict()


def get_goord(a):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(a)

    # Выполняем запрос.
    response = None
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Печатаем извлеченные из ответа поля:
        return (','.join(toponym_coodrinates.split()))


def start(bot, update):
    # print('Начало')
    update.message.reply_text(
        "Я могу помочь тебе выбрать место для отдыха и рассказать о нем.\n"
        "Начнем?\n"
        "p.s. Прервать диалог можно командой /stop"
    )
    # print('Новый пользователь')


    return 1


def map1(bot, update, town):
    print(town)
    update.message.reply_text('Город {} на карте'.format(town))
    api1 = "http://static-maps.yandex.ru/1.x/?ll=99.505405,61.698653&spn=35.0,35.0&l=map&pt={},pm2rdm".format(
        get_goord(town))
    bot.sendPhoto(
        update.message.chat.id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API по сути является ссылкой на картинку.
        api1)

    static_api_request = "http://static-maps.yandex.ru/1.x/?ll={}&spn=0.1,0.1&l=map".format(get_goord(town))

    bot.sendPhoto(
        update.message.chat.id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API по сути является ссылкой на картинку.
        static_api_request)


def chek(a):
    response = None

    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(a)

    # Выполняем запрос.
    response = None
    try:
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Печатаем извлеченные из ответа поля:
            print(toponym_address, "имеет координаты:", toponym_coodrinates)
            return True
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")


def end(bot, update, user_data):
    # print('+3')

    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return 11
    # print('+3.1')
    if update.message.text.lower() in Questions.positive_response:
        mass = []
        mass = [i for i in peopl[str(update._effective_message.chat.id)].keys()]
        a = ', '.join(mass)

        if len(mass) == 1:
            update.message.reply_text('Вам подошел город {}'.format(a))
            print('+1')
            map1(bot, update, a)
        else:
            update.message.reply_text('Вам подошли города {}. Вот они на карте'.format(a))
            for i in mass:
                map1(bot, update, i)

    else:
        update.message.reply_text("Жаль. А было бы интерсно пообщаться. Всего доброго!")
        del peopl[str(update._effective_message.chat.id)]
        return ConversationHandler.END


def perv(bot, update, user_data):
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, ответьте да или нет')
        return 1
    if update.message.text.lower() in Questions.positive_response:
        if update._effective_message.chat.first_name == None:
            ind = update._effective_message.chat.last_name
        else:
            ind = update._effective_message.chat.first_name
        update.message.reply_text('Привет, {}! \n '.format(ind))
        update.message.reply_text(random.choice(Questions.question['город']))
        return 2
    else:
        update.message.reply_text(
            "Жаль. А было бы интерсно пообщаться. Всего доброго!")
        del peopl[str(update._effective_message.chat.id)]
        return ConversationHandler.END


def vtoroy(bot, update, user_data):
    a = update.message.text.split()[-1]
    a = a[0].upper() + a[1:].lower()
    print('+1')
    if chek(a):
        print('+2')
    else:
        update.message.reply_text(
            'Я не нашел города {} на карте. Проверьте пожалуйста правильность написания'.format(a))
        return 2
    peopl[str(update._effective_message.chat.id)] = Man(a)

    update.message.reply_text(random.choice(Questions.question['море']))
    return 3


def tretiy(bot, update, user_data):
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return 3
    if update.message.text.lower() in Questions.positive_response:

        update.message.reply_text('Я тоже люблю море!')
        peopl[str(update._effective_message.chat.id)].SORT(0, '+')


    elif update.message.text.lower() in Questions.negative_answer:
        update.message.reply_text('И правда, кому оно нужно')
        peopl[str(update._effective_message.chat.id)].SORT(0, '-')

    update.message.reply_text(random.choice(Questions.question['время']))
    return 4


def chetvert(bot, update, user_data):
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return 4

    if update.message.text.lower() in Questions.positive_response:

        peopl[str(update._effective_message.chat.id)].SORT(2, '+')
        update.message.reply_text('Тепло - это замечательно!')

    elif update.message.text.lower() in Questions.negative_answer:

        update.message.reply_text('От жары только хуже')
        peopl[str(update._effective_message.chat.id)].SORT(2, '-')

    update.message.reply_text(random.choice(Questions.question['достопримечательности']))

    return 5


def pyat(bot, update, user_data):
    cop = peopl[str(update._effective_message.chat.id)].cities.copy()
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return 5
    if update.message.text.lower() in Questions.positive_response:
        peopl[str(update._effective_message.chat.id)].SORT(1, '+')
        update.message.reply_text('Нет ничего лучше культурного просвещения')

    elif update.message.text.lower() in Questions.negative_answer:
        update.message.reply_text('Ходить по музеям? Скукота!')
        peopl[str(update._effective_message.chat.id)].SORT(1, '-')

    d = dict()
    if peopl[str(update._effective_message.chat.id)].cities == d:
        peopl[str(update._effective_message.chat.id)] = cop
        update.message.reply_text(
            'Наша база данных достаточно мала и в данный момент не может угодить всем критериям, но по преждему есть города которые могут вам подойти. Желаете посмотреть?')
        return 11

    update.message.reply_text(random.choice(Questions.question['аэропорт']))

    return 6


def shest(bot, update, user_data):
    cop = peopl[str(update._effective_message.chat.id)].cities.copy()
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return 6

    if update.message.text.lower() in Questions.positive_response:
        peopl[str(update._effective_message.chat.id)].SORT(5, '+')
        update.message.reply_text('Я тоже считаю что самолет изобрели не просто так')

    elif update.message.text.lower() in Questions.negative_answer:
        update.message.reply_text('У каждого свои предпочтения. Продолжим')
        peopl[str(update._effective_message.chat.id)].SORT(5, '-')

    d = dict()
    if peopl[str(update._effective_message.chat.id)].cities == d:
        peopl[str(update._effective_message.chat.id)] = cop
        update.message.reply_text(
            'Наша база данных достаточно мала и в данный момент не может угодить всем критериям, но по преждему есть города которые могут вам подойти. Желаете посмотреть?')
        return 11

    update.message.reply_text(random.choice(Questions.question['актотд']))

    return 8


def sem(bot, update, user_data):
    summ = update.message.text
    cop = peopl[str(update._effective_message.chat.id)].cities.copy()
    try:
        summ = int(summ)
    except:
        update.message.reply_text('Пожалуйста введите сумму которую вы готовы тратить в день числом')
        return 7

    update.message.reply_text('Ваши предпочтения учтены. Тест закончен. Вывести pезультат?')
    peopl[str(update._effective_message.chat.id)].SORT(4, summ)

    d = dict()
    if peopl[str(update._effective_message.chat.id)].cities == d:
        peopl[str(update._effective_message.chat.id)] = cop
        update.message.reply_text(
            'Наша база данных достаточно мала и в данный момент не может угодить всем критериям, но по преждему есть города которые могут вам подойти. Желаете посмотреть?')
        return 11

    peopl[str(update._effective_message.chat.id)] = peopl[str(update._effective_message.chat.id)].cities

    return 11


def vosem(bot, update, user_data):
    cop = peopl[str(update._effective_message.chat.id)].cities.copy()
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return 8
    if update.message.text in Questions.positive_response:
        peopl[str(update._effective_message.chat.id)].SORT(7, '+')
        update.message.reply_text('Сидеть на месте это не для нас. Верно?')

    elif update.message.text in Questions.negative_answer:
        update.message.reply_text('ну да, на отдыхе нужно отдыхать')
        peopl[str(update._effective_message.chat.id)].SORT(7, '-')

    d = dict()
    if peopl[str(update._effective_message.chat.id)].cities == d:
        peopl[str(update._effective_message.chat.id)] = cop
        update.message.reply_text(
            'Наша база данных достаточно мала и в данный момент не может угодить всем критериям, но по преждему есть города которые могут вам подойти. Желаете посмотреть?')
        return 11

    update.message.reply_text(random.choice(Questions.question['кухня']))
    return 9


def dev(bot, update, user_data):
    cop = peopl[str(update._effective_message.chat.id)].cities.copy()
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return 9

    if update.message.text.lower() in Questions.positive_response:
        peopl[str(update._effective_message.chat.id)].SORT(3, '+')
        update.message.reply_text('Еда это хорошо')

    elif update.message.text.lower() in Questions.negative_answer:
        update.message.reply_text('Согласен, поесть и дома можно')
        peopl[str(update._effective_message.chat.id)].SORT(3, '-')
    r = dict()
    if peopl[str(update._effective_message.chat.id)].cities != r:
        mass = []
        mass = [peopl[str(update._effective_message.chat.id)].cities[i][5] for i in
                peopl[str(update._effective_message.chat.id)].cities.keys()]
        if mass[0] == '+':
            update.message.reply_text(random.choice(Questions.question['деньги']))
            return 7
        else:
            update.message.reply_text(random.choice(Questions.question['жд']))
            return 10
    else:

        peopl[str(update._effective_message.chat.id)] = cop
        update.message.reply_text(
            'Наша база данных достаточно мала и в данный момент не может угодить всем критериям, но по преждему есть города которые могут вам подойти. Желаете посмотреть?')
        return 11


def des(bot, update, user_data):
    cop = peopl[str(update._effective_message.chat.id)].cities.copy()
    if update.message.text.lower() not in Questions.positive_response and update.message.text.lower() not in Questions.negative_answer:
        update.message.reply_text('К сожалению я не могу понять что вы ответили :-(, напишите пожалуйста проще')
        return
    if update.message.text.lower() in Questions.positive_response:
        peopl[str(update._effective_message.chat.id)].SORT(6, '+')
        update.message.reply_text('Стук колес очень успокаивает')

    elif update.message.text.lower() in Questions.negative_answer:
        update.message.reply_text('А вдруг еще и дембеля попадуться?')
        peopl[str(update._effective_message.chat.id)].SORT(6, '-')

    d = dict()
    if peopl[str(update._effective_message.chat.id)].cities == d:
        peopl[str(update._effective_message.chat.id)] = cop
        update.message.reply_text(
            'Наша база данных достаточно мала и в данный момент не может угодить всем критериям, но по преждему есть города которые могут вам подойти. Желаете посмотреть?')
        return 11

    update.message.reply_text(random.choice(Questions.question['деньги']))
    return 7


def skip(bot, update, user_data):
    user_data['locality'] = None
    update.message.reply_text("Какая погода у вас за окном?")
    return 2


def stop(bot, update):
    update.message.reply_text(
        "Жаль. А было бы интерсно пообщаться. Всего доброго!")
    del peopl[str(update._effective_message.chat.id)]
    return ConversationHandler.END  # Константа, означающая конец диалога.


def answer(bot, update):
    text = update.message.text
    update.message.reply_text('Otvet')


def main():
    print('()')
    updater = Updater("498181759:AAHiU8ILClhAfTog3ZQ_gFaeQPlV4tvJNnw")
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('start', start)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text, perv, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            # ...и для его использования.
            2: [MessageHandler(Filters.text, vtoroy, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            3: [MessageHandler(Filters.text, tretiy, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            4: [MessageHandler(Filters.text, chetvert, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            5: [MessageHandler(Filters.text, pyat, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            6: [MessageHandler(Filters.text, shest, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            7: [MessageHandler(Filters.text, sem, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            8: [MessageHandler(Filters.text, vosem, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            9: [MessageHandler(Filters.text, dev, pass_user_data=True), CommandHandler('start', start),
                CommandHandler('stop', stop)],
            10: [MessageHandler(Filters.text, des, pass_user_data=True), CommandHandler('start', start),
                 CommandHandler('stop', stop)],
            11: [MessageHandler(Filters.text, end, pass_user_data=True), CommandHandler('start', start),
                 CommandHandler('stop', stop)]

        },
        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
