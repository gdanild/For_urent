# -*- coding: utf-8 -*-
import requests, csv, time,gspread,re



acc_token = ""

error_str = "Неправильно введены данные.\n\nФормат:\nТелефон\nСумма\nКомменатрий\n\nПример:\n9999696689\n500\nПромо"
error_str1 = "Ошибка.\nНеправильно указана сумма."
error_str2 = "Ошибка.\nНеправильно указан номер телефона."
error_str3 = "Ошибка.\nСумма не может быть нулевой или превышать 5000 рублей."

def write_data(row):
    exampleFile = open("acc_id.csv", 'a', encoding='UTF-8', newline='')
    exampleWriter = csv.writer(exampleFile, delimiter=';')
    exampleWriter.writerow(row)
    exampleFile.close()

def read_data(phone):
    with open("acc_id.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0]==phone:
                return [row[1],row[2]]
        return "no"
def in_google(row_g):
    time_now = time.strftime("%d.%m.%y %H:%M")
    row_g.append(time_now)
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key("1ITFuAVUZacSnFKIGqJqeSt5K3exNNWNir2SGIKUMj5c")
    worksheet = sh.worksheet("Worksheet")
    worksheet.resize(1000)
    worksheet.append_row(row_g)

def write_on_file(name_file, ref):
    if name_file == "users.txt":
        o_mode = "a"
    else:
        o_mode = "w"
    file = open(name_file, o_mode, encoding="utf-8")
    file.write(ref)
    file.close()
    return True


def read_on_file():
    f = open("otus.txt", encoding="utf-8")
    ref = f.readline()
    f.close()
    return ref


def end_req(num):
    BASE_URL = 'https://service.urentbike.ru/orderingscooter/api/orders/end'
    global acc_token

    headers = {
        "Authorization": acc_token,
        'Content-Type':'application/json; charset=UTF-8',
        'Accept-Language': 'ru-RU',
        'Content-Length': '173',
        'Host': 'service.urentbike.ru',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    data = '{"locationLat": 55.7101317, "locationLng": 37.597675, "scooterIdentifier": "S.'+ num +'"}'

    auth_response = requests.post(BASE_URL, headers=headers,data = data)
    if (auth_response.status_code == 401):
        refresh_token()
        return end_req(num)
    if (auth_response.status_code != 200):
        return False
    return auth_response

def get_last_orders(n):
    BASE_URL = "https://service.urentbike.ru/ordering/api/orders/my?cPage=1&iOnPage="+str(n)+"&order=StartDateTimeUtc%3Adesc"
    global acc_token

    headers = {
        "Authorization": acc_token
    }


    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        return get_last_orders(n)
    if (auth_response.status_code != 200):
        return False
    return auth_response

def end_rent(num,fio):
    actv_rents = inrents().json()
    for i in actv_rents["activities"]:
        if str(i["bikeIdentifier"][2:]) == str(num):
            actual_activ = i
    result = end_req(num)
    if result == False:
        print("error end rent")
        return False
    print(actual_activ)
    print(actual_activ["statistics"])
    min_last_ord = round(int(actual_activ["absoluteOrderingStartDateTime"]["differenceFromNowSeconds"])/60)
    print(min_last_ord)
    profit = min_last_ord*8+50
    bonus_withdrawn = int(actual_activ["bonusWithdrawn"])
    money_withdrawn_fact = round(bonus_withdrawn*0.83333333)
    in_google([fio, str(num), bonus_withdrawn, money_withdrawn_fact, min_last_ord, profit])
    return "Завершено. Взять: "+str(profit)+" рублей"







def get_zones(num,rate):
    BASE_URL = 'https://service.urentbike.ru/gatewayclient/api/v1/order/make'
    global acc_token

    headers = {
        "Authorization": acc_token,
        'Content-Type':'application/json; charset=UTF-8'
    }

    data = '{"locationLat": 54.3434675, "locationLng": 38.164853, "isQrCode": true, "rateId": "'+ rate +'","Identifier": "S.'+ num +'", "withInsurance": false }'
    print(data)

    auth_response = requests.post(BASE_URL, headers=headers,data = data)
    print(auth_response.content)
    if (auth_response.status_code == 401):
        refresh_token()
        return get_zones(num,rate)
    if (auth_response.status_code != 200):
        return auth_response.content
    return auth_response


def inrents():
    global acc_token
    BASE_URL = "https://service.urentbike.ru/ordering/api/activity"
    headers = {
        "Authorization": acc_token,
        'Content-Type':'application/json; charset=UTF-8'
    }
    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        return inrents()
    if (auth_response.status_code != 200):
        return False
    return auth_response

def refresh_token():
    get = read_on_file()
    BASE_URL = 'https://service.urentbike.ru/identity/connect/token'
    data = {

    }
    params = {
        "client_id": "mobile.client",
        "client_secret": "caRgg4LIWUsjOz9u1r8oLIpiJU8VcifabXVWLJy5bMPjqtE6ZMfTHn7ykpmJR8uz",
        "grant_type": "refresh_token",
        "scope": "bike.api%20ordering.api%20location.api%20customers.api%20payment.api%20maintenance.api%20notification.api%20log.api%20ordering.scooter.api%20driver.bike.lock.offo.api%20driver.scooter.ninebot.api%20offline_access",
        "refresh_token": get
    }
    auth_response = requests.post(BASE_URL, headers=data, data=params)
    global acc_token
    acc_token = "Bearer "+auth_response.json()["access_token"]
    write_on_file("otus.txt", str(auth_response.json()["refresh_token"]))

    return auth_response


get = refresh_token().json()
acc_token = get["access_token"]
ref_token = get["refresh_token"]
write_on_file("otus.txt", str(ref_token))



import telebot

bot = telebot.TeleBot("")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Напиши номер телефона')

@bot.message_handler(commands=['inrents'])
def start_message(message):
    status_in_rents = "В аренде:\n"
    active_rents = inrents().json()
    for i in active_rents["activities"]:
        sec_rents = round(int(i["absoluteOrderingStartDateTime"]["differenceFromNowSeconds"])/60)
        status_in_rents+="|№: "+i["bikeIdentifier"][2:]+"|Min: "+str(sec_rents)+"|₽: " + str(sec_rents*8+50)+"|\n"
    bot.reply_to(message, status_in_rents)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    print(str(message.chat.id))
    goods_users = []
    if not (int(message.from_user.id) in goods_users):
        bot.reply_to(message, "У вас нет доступа.")
        return False

    try:
        if message.text[0] == "E":
            print(message.text[1:len(message.text)])
            fio = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
            bot.reply_to(message,end_rent(message.text[1:len(message.text)], fio))
        if message.text[0] == "M": bot.reply_to(message, get_zones(message.text[1:len(message.text)], "60a13eaa1965f483d37650a2"))
        if message.text[0] == "H": bot.reply_to(message, get_zones(message.text[1:len(message.text)], "608d2c2e79002e5b28bbb6d1"))
    except Exception as ex:
        bot.reply_to(message, "Произошла ошибка\n\n" + str(ex))
        print(str(ex))
    return True



if __name__ == '__main__':
    bot.polling(none_stop=True)
#print(get_zones('031671').json())




