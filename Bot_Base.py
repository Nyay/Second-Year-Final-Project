import random
import Bot_Brain
import telebot
from telebot import types

bot = telebot.TeleBot(Bot_Brain.TOKEN)
bot.remove_webhook()
data = {}
problems = []
current_word = []
maybe_line = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот для снятия омонимии в предложениях. Надеюсь, что когда-нибудь'
                                      ' я принесу много пользы науке и людям, но кто его знает. В общем, для того чтобы'
                                      'узнать как я работаю, пиши /help. Так ты унаешь как использовать команды.\n'
                                      'Удачи, нодеюсь тебе понравится! Со всеми предложениям, пиши моему создателю '
                                      '@sorry_im_neet')


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Так-так. Сейчас все расскажу.\n'
                                      'Для начала работы необходимо загрузить сообщение, кторое ты собираешься '
                                      'анализировть.\n\n'
                                      '/new_line (текст через пробел) – Добавляет предложение с которым сне потом '
                                      'предстоит работать. Обязательно не забудь пробел, наче я могу не понять тебя\n\n'
                                      'После того, как предложение добавлено, я готова с ним работать. Для это...\n\n'
                                      '/analize – Я проведу разбор предложения. Затем я составлю у себя словарь '
                                      'со всеми разборами и самим предложением. Если омонимических форм не обнаружено, '
                                      'то можно переходить сразу к загрузки в мою память.\n\n'
                                      '/commit – Загрузить разбор в фойл который хранится у меня. Возможно... '
                                      'Я распечатаю разбор, но это не точно, я еще не решила с этим\n\n'
                                      'Если омонимичные формы все же найдены, то с ними надо разобраться. Для этого '
                                      'прописываес вот эту команду:\n\n'
                                      '/select – Я покажу тебе слова у которых я не смогла определиться с разбором.'
                                      ' После того, как ты выбрал слово, тебе будут представленны мои варианты разбора'
                                      ' если нужного разбора нет, то ты можешь вбить мне разбор вручную. Чтобы узнать'
                                      ' какие обозначения использовать используй следующую команду:\n\n'
                                      '/designation – Список всех обозначений и правило их использования\n\n'
                                      'После того, как ты разобрал слова, ты можешь проверить все данные,'
                                      ' для этго используй эту команду:\n\n'
                                      '/show – Я покажу тебе какой разбор у меня есть на данный момент.\n\n'
                                      'Вроде бы все. Запонми, что каждый раз, когда ты добавляешь новое предложение или'
                                      ' записываешь данные, то предыдущий разбор удаляется у меня из памяти. '
                                      'Поэтому не забывает про /commit!\n'
                                      'Четь не забыла! Если теюе не нравится разбор,'
                                      ' тогда просто напиши мне это слово, а затем правильный разбор. Я все перепишу!\n'
                                      'По всем вопросам ты также можешь образаться к создателю @sorry_im_neet ^^')
    bot.send_sticker(message.chat.id, Bot_Brain.STICK_HELP)


@bot.message_handler(commands=['new_line'])
def new_line(message):
    data.clear()
    text = message.text
    text_for_function = text.strip('/new_line ')
    data['line'] = text_for_function
    reply = 'Окей! Я загрузила это предложения и готова к дальнейшей работе. Вся предыдущая информация стерта ^_^'
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['analize'])
def analise(message):
    try:
        problems.clear()
        analise_list = Bot_Brain.LINE_ANALISE(data['line'])
        for el in analise_list:
            if len(el) != 2:
                problems.append(el[0])
            data[el[0]] = []
            x = 1
            while x <= len(el) - 1:
               data[el[0]].append(el[x])
               x += 1
        print(data)
        print(problems)
        if len(problems) != 0:
            line_of_problems = ', '.join(problems)
            reply = 'При разборе предложения, я обнаружила омонимичные формы для слов:\n"' + line_of_problems + '".\n' \
                    'Чтобы выбрать правильные формы для данных форм напишите команду /select, затем выберете слово.'
            bot.send_message(message.chat.id, reply)
        else:
            reply = 'Омонимичных форм в вашем предложении не обнаружено, я могу загрузить это предложение? ' \
                    'Если да, то припишите /commit!'
            bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_SUCCESS))
            bot.send_message(message.chat.id, reply)
    except KeyError:
        reply = 'Хммммм не получается проанализировать... А ты мне текст вообще давал?' \
                ' Если нет, то пропиши /new_line и текст, а потом уже я проанализирую его.'
        bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_ERROR))
        bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['add'])
def add(message):
    text = message.text
    text.strip('/add ')
    items = text.split()
    if len(items) == 2 and len(data) > 2:
        for element in items:
            if element == 'A' or 'S' or 'I' or 'C' or 'N' or:
                continue
            else:
                data[str(element)].append(items.remove(element)[0])
        bot.send_message(message.chat.id, 'Окей... Раз этот разбор так важен я его записала. Можешь продолжать работу')
    else:
        bot.send_message(message.chat.id, 'Для начала надо добавить предложение и сделать разбор!'
                                          ' Только потом использовать эту функцию.')


@bot.message_handler(commands=['select'])
def analise(message):
    if len(problems) == 0:
        bot.send_message(message.chat.id, 'Мне нечего выбирать, все, вроде бы, разобрано... '
                                          'Но, если вдруг ты хочешь записать другой разбор,'
                                          ' то просто напиши это слово ,'
                                          ' а затем напиши его разбор, и я его заменю')
        bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_ERROR))
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        for word in problems:
            btn = types.KeyboardButton(str(word))
            keyboard.add(btn)
        bot.send_message(message.chat.id, 'Выберай:', reply_markup=keyboard)


@bot.message_handler(commands=['show'])
def show(message):
    print(data)
    if len(data) == 1:
        bot.send_message(message.chat.id, 'К сожалению, сейчас у меня есть только ваше предложение.'
                                          ' Чтобы я его разобрала, напиши команду /analize.')
    elif len(data) == 0:
        bot.send_message(message.chat.id, 'Мне совершенно несчем работать... даже сообзения нет! Так не пойдет!'
                                          'Добавь сообщение с помощью компнды /new_line'
                                          ' и проанализий ее с помощью команды /analize')
        bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_ERROR))
    else:
        lines = []
        for word in data:
            if word != 'line':
                for el in data[word]:
                    line = word + ' (' + el + ')'
                    lines.append(line)
        line = ';\n'.join(lines)
        print(line)
        line = 'Первоначальное предложение: ' + data['line'] + '\nРазбор для слов:\n' + line
        bot.send_message(message.chat.id, line)


@bot.message_handler(commands=['commit'])
def commit(message):
    if len(data) == 1:
        bot.send_message(message.chat.id, 'Эй! У меня есть пока только сообщение. Его нет смылса записывать,'
                                          ' проведи хотя бы необработанный ананлиз')
        bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_ERROR))
    elif data != {}:
        file = open('/Users/macbook/Desktop/Second-Year-Final-Project/result.txt', 'a', encoding='UTF-8')
        lines = []
        for word in data:
            if word != 'line':
                for el in data[word]:
                    line = word + ' (' + el + ')'
                    lines.append(line)
        line = '; '.join(lines)
        print(line)
        file.write('Первоначальное предложение: ' + data['line'] + '\nРазбор для слов: ' + str(line) + '\n\n')
        file.close()
        data.clear()
        bot.send_message(message.chat.id, 'Все! Я все загрузила в txt файл. Мой "рабочий стол очизен и'
                                          ' теперь можно добавить новое предложение для разбора"')
        sid = random.choice(Bot_Brain.STICK_PACK_SUCCESS)
        print(sid)
        bot.send_sticker(message.chat.id, sid)
    else:
        bot.send_message(message.chat.id, 'Хм, что-то нечего мне записывать.'
                                          ' Вначале надо произвести весь процесс разбора! Посмотри внимательно в /help')


@bot.message_handler(commands=['designation'])
def designation(message):
    bot.send_message(message.chat.id, 'Дававй, я тебя познакомлю с оформленем морфологического рабора.'
                                      'Бывает же такое, что я не могу разобрать все прямо так идеально,'
                                      ' тогда тебе придется заполнить разбор самостоятельно.'
                                      ' Все признаки надо писать через запятую'
                                      '\nВот сам список признаков:\n'
                                      '\nЧасти речи\n\n'
                                      'S — Существительное\n'
                                      'A — Прилагательное\n'
                                      'NUM — Числительное\n'
                                      'ANUM — Числительное-прилагательное\n'
                                      'V — Глагол\n'
                                      'ADV — Наречие\n'
                                      'SPRO — Местоимение-существительное\n'
                                      'ADVPRO — Местоименное наречие\n'
                                      'PR — Предлог\n'
                                      'CONJ — Союз\n'
                                      'PART — Частица\n'
                                      'INTJ — Междометие\n'
                                      '\nРод\n\n'
                                      'муж — Мужской род\n'
                                      'жен — Женский род\n'
                                      'сред — Средний род\n'
                                      '\nОдушевленность\n\n'
                                      'од — Одушевленноe\n'
                                      'неод — Неодушевленноe\n'
                                      '\nЧисло\n\n'
                                      'ед — Единственное число\n'
                                      'мн — Множественное число\n'
                                      '\nПадеж\n\n'
                                      'им — Именительный падеж\n'
                                      'род - Родительный падеж\n'
                                      'дат - Дательный падеж\n'
                                      'вин - Винительный падеж\n'
                                      'твор - Творительный падеж\n'
                                      'пр - Предложный падеж\n'
                                      'парт - Партитив(второй родительный) падеж\n'
                                      'местн - Местный(второй предложный) падеж\n'
                                      'зват - Звательный падеж\n'
                                      '\nВремя (глаголов)\n\n'
                                      'наст - Настоящее\n'
                                      'непрош - Непрошедшее\n'
                                      'прош - Нрошедшее\n'
                                      '\nРепрезентация и наклонение глагола\n\n'
                                      'деепр - Деепричастие\n'
                                      'инф - Инфинитив\n'
                                      'прич - Причастие\n'
                                      'изъяв - Изьявительное наклонение\n'
                                      'пов - Повелительное наклонение\n'
                                      '\nФорма прилагательных\n\n'
                                      'кр - Краткая форма\n'
                                      'полн - Полная форма\n'
                                      'притяж - Притяжательные прилагательные\n'
                                      '\nСтепень сравнения\n\n'
                                      'прев - Превосходная\n'
                                      'срав - Сравнительная\n'
                                      '\nЛицо глагола\n\n'
                                      '1-л - 1-е лицо\n'
                                      '2-л - 2-е лицо\n'
                                      '3-л - 3-е лицо\n'
                                      '\nВид\n\n'
                                      'несов - Несовершенный\n'
                                      'сов - Совершенный\n'
                                      '\nЗалог\n\n'
                                      'действ - Действительный залог\n'
                                      'страд - Страдательный залог\n'
                                      '\nПереходность\n\n'
                                      'пе - Переходный глагол\n'
                                      'нп - Непереходный глагол\n'
                                      '\nПрочие обозначения\n\n'
                                      'вводн - Вводное слово\n'
                                      'гео - Географическое название\n'
                                      'затр - Образование формы затруднено\n'
                                      'имя - Имя собственное\n'
                                      'искаж - Искаженная форма\n'
                                      'мж - Общая форма мужского и женского рода\n'
                                      'обсц - Обсценная лексика\n'
                                      'отч - Отчество\n'
                                      'прдк - Предикатив\n'
                                      'разг - Разговорная форма\n'
                                      'редк - Редко встречающееся слово\n'
                                      'сокр - Сокращение\n'
                                      'устар - Устаревшая форма\n'
                                      'фам - Фамилия\n')


@bot.message_handler(content_types=['text'])
def job(message):
    try:
        if message.text in data['line']:
            print('True')
            current_word.append(message.text)
            keyboard = types.ReplyKeyboardMarkup(row_width=3)
            lines_of_ana = data[str(message.text)]
            for word in lines_of_ana:
                btn = types.KeyboardButton(str(word))
                keyboard.add(btn)
            bot.send_message(message.chat.id, 'Выберете правильный разбор. '
                                              'Если правильного варианта нет, вы можете вписать разбор вречную.'
                                              ' Чтобы прочитать формат записи ответа, пропишите'
                                              ' /designation.\n'
                                              'Напомню ваше предложение: ' + data['line'], reply_markup=keyboard)
        elif message.text[0] == 'A' or 'S' or 'I' or 'C' or 'N':
            data[current_word[0]] = []
            data[current_word[0]].append(message.text)
            try:
                try:
                    problems.remove(current_word[0])
                except ValueError:
                    print('Блин')
                current_word.clear()
                if len(problems) == 1:
                    bot.send_message(message.chat.id, 'Так, это записала, осталось одно слово и можно отправлять!^^')
                    analise(message)
                elif len(problems) > 1:
                    bot.send_message(message.chat.id, 'Окей, я записала выбранный вами ответ.'
                                                      ' Какое слово разберем дальше?')
                    analise(message)
                elif len(problems) == 0:
                    bot.send_message(message.chat.id, 'Так... Все слова вроде разобрали, теперь можно и записывать...')
                    bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_SUCCESS))
            except IndexError:
                current_word.clear()
                bot.send_message(message.chat.id, 'Этого слово было уже разобрано,'
                                                  ' поэтому список оставшихся слов не изменился:')
                analise(message)
    except KeyError:
        print('Restarted')
        bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_ERROR))
    except IndexError:
        bot.send_message(message.chat.id, 'У меня не выбрано слово к которому мне нужно прикрепить данный разбор.'
                                          'Поэтому пропиши /select и выбери слово из списка, или пропеши его вручную.'
                                          'После этого можешь уже прописать анализ.')
        bot.send_sticker(message.chat.id, random.choice(Bot_Brain.STICK_PACK_ERROR))

if __name__ == '__main__':
    bot.polling(none_stop=True)
