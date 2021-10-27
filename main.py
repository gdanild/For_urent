import requests, sqlite3, csv, time, datetime
acc_token = ""
table_key = "1liTT4-j78eMazzmGMrhDxj-t9LWUsKxMxubqjwWmpQA"
conn = sqlite3.connect("sv_insurance.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

headers_glob = {
    "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
    "TraceId": "JVCJ1FE9V8",
    "X-Vendor": "ADR",
    "X-Selected-Vendors": "ADR",
    "Authorization": "Bearer iuytrew",
    "Accept-Language": "ru-RU",
    "Host": "service.urentbike.ru",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.12.6",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "149"
}

sv_num = {"5f134b44b9c2c80001b2f5d9": "Екатерина Шишова МСК",
          "5f1aa7c8d0ff3300010d55ca": "Глеб Пилат МСК",
          "5ef8e2f8a1cc5900018849da": "Александр Маричук МСК",
          "5f0072e446f88800010fd1da": "Данила Грищенко МСК",
          "5f3666339b7343000197031a": "Дмитрий Попов МСК",
          "5f4d7e8b82bc110001c44ef9": "Анастасия Васильева АДР",
          "600bb570a2d2b10001351ba9": "Евгений Уваров АДР",
          "5c1e643d2f38380001e08132": "Светлана Ситкова АДР",
          "5fc3d71d1fa39900011836cb": "Евгений Железняков АДР",
          "5f4d13b682bc110001bf8104": "Игорь Смирнов Крд",
          "5f6c5f8e6251330001ed0f61": "Александр Яланджи СПБ",
          "5f24012fee900e0001ce9c1a": "Софья Дормидонтова СПБ",
          "61092e9b89097e1191d575f8": "Мария Ражева НН",
          "60768c513e5330f436a426ac": "Олег Бузмаков ГЛЖК",
          "5f1ca0a2d0ff3300011c892e": "Алиса Шама КРД",
          "608bf5de9b50923f61e942f4": "Юлия Гажиенко АНП",
          "5d74e235da19a800014a7ae0": "Андрей Колесник Стажер",
          "5baf640281502f0001213e16": "Илья Тимаховский Стажер",
          "5bc1e3e6b28c5c0001091d0e": "Андрей Азаров Стажер",
          "5c65592f01cdcb0001f23d32": "Елизаров",
          "60bf9f14e73ab24bafcbb56e": "Ибрахим Чоудори"}

def create_table(name):
    try:
        string = "(ФИО text, Понедельник text, Вторник text, Среда text, Четверг text, Пятница text, Суббота text, Воскресенье text, Сумма text)"
        cmd = "CREATE TABLE " + name + string
        cursor.execute(cmd)
        conn.commit()
    except Exception as ex:
        print(str(ex))
        return True

def get_zones(num):
    BASE_URL = 'https://customers.service.urentbike.ru/api/customers?filter={"text":"' + num + '"}&cPage=1&iOnPage=10'
    global headers_glob

    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "ADR",
        "X-Selected-Vendors": "ADR",
        "Authorization": "Bearer " + acc_token,
        "Accept-Language": "ru-RU",
        "Host": "customers.service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    headers["Authorization"] = headers_glob["Authorization"]

    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        auth_response = get_zones(num)
    elif (auth_response.status_code != 200):
        return False
    return auth_response

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

def refresh_token():
    get = read_on_file()
    BASE_URL = 'https://service.urentbike.ru/identity/connect/token'
    data = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "NVU",
        "X-Selected-Vendors": "NVU",
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content - Length": "659"
    }
    params = {
        "client_id": "mobile.technic",
        "client_secret": "McL1uMsTuL3ESeYi0iP0jwLUz6j2oOcM7zvBJZkdFdQjBynV11e0VueACQDdkCRu",
        "grant_type": "refresh_token",
        "scope": "bike.api%20maintenance.api%20location.api%20ordering.api%20ordering.scooter.api%20driver.scooter.tracker.navtelecom.api%20driver.bike.tracker.concox.api%20driver.bike.lock.offo.api%20driver.bike.lock.tomsk.api%20log.api%20payment.api%20customers.api%20driver.scooter.ninebot.api%20driver.scooter.teltonika.api%20driver.scooter.cityride.api%20driver.scooter.tracker.arusnavi.api%20driver.scooter.omni.api%20driver.scooter.voi.api%20offline_access",
        "refresh_token": get
    }
    auth_response = requests.post(BASE_URL, headers=data, data=params)
    global headers_glob
    headers_glob["Authorization"] = "Bearer " + auth_response.json()["access_token"]
    print(auth_response.json()["access_token"])
    write_on_file("otus.txt", str(auth_response.json()["refresh_token"]))
    return auth_response

def get_orders(user_id, start, end):
    BASE_URL = 'https://service.urentbike.ru/ordering/api/orders?filter={"accountId":"' + user_id + '","start":"' + start + 'T00:00:00.000Z","end":"' + end + 'T00:00:00.000Z"}&iOnPage=1000'
    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "MOCHM",
        "X-Selected-Vendors": "MOCHM,MOKRG,MOLBI,MOODV,MOU,MURB,VDNH,KGD,KGDO,ADR,SCH,ANR,GRU,KBRK,KRD,KRP,NVU",
        "Authorization": "Bearer " + acc_token,
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
    }

    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        auth_response = get_orders()
    elif (auth_response.status_code != 200):
        return False
    return auth_response

def get_to_db():
    #18 start 41end
    for i in range(18, 44):
        print("Начал делать неделю: "+str(i))
        d = "2021.W"+str(i)
        d_next = "2021.W"+str(i+1)
        r = datetime.datetime.strptime(d + '.1', "%Y.W%W.%w")
        monday = r.strftime("%Y-%m-%d")
        r = datetime.datetime.strptime(d_next + '.1', "%Y.W%W.%w")
        monday_next = r.strftime("%Y-%m-%d")
        print("Это: "+monday + "==>" + monday_next)
        name_for_table = "w"+str(i)
        create_table(name_for_table)
        print("Создал табличку с названием: " + name_for_table)
     #   sv_num = ["5f0072e446f88800010fd1da"]

        for j in sv_num:
            orders = get_orders(j, monday,monday_next).json()["entries"]
            row = [0, 0, 0, 0, 0, 0, 0]
            for k in orders:
                times = k["startDateTimeUtc"]
                try:
                    r = datetime.datetime.strptime(times, "%Y-%m-%dT%H:%M:%S.%fZ")
                except Exception as ex:
                    r = datetime.datetime.strptime(times, "%Y-%m-%dT%H:%M:%SZ")
                date_msc = (r + datetime.timedelta(minutes=180))
                week = int(date_msc.strftime("%w")) -1
                if week == -1: week = 6
                print(k)
                if k["insurance"] != None:
                    row[week]+=k["insurance"]["value"]
            sum = 0
            for i in range(len(row)):
                row[i]=round(row[i])
                sum+=round(row[i])
            row.append(sum)
            row = [sv_num[j]] + row
            conn.execute('insert into ' + name_for_table + ' values (?,?,?,?,?,?,?,?,?)', tuple(row))
            conn.commit()
        print("закончил неделю: "+str(i))
    return True

import gspread
def in_google(row_g, city):
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(table_key)
    worksheet = sh.worksheet(city)
    worksheet.resize(1000)
    worksheet.append_row(row_g)

def create_list_in_google(name):
    try:
        gc = gspread.service_account(filename="credentials.json")
        sh = gc.open_by_key(table_key)
        work = sh.add_worksheet(title=name, rows="100", cols="10")
        row = ["ФИО", "Понедельник"," Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Сумма"]
        in_google(row, name)
    except Exception as ex:
        print(ex)
        return True

def from_db_to_table():
    mat_row = []
    for i in range(21):
        mat_row.append([])
        for j in range(21):
            mat_row[i].append(0)
    for i in range(18, 44):
        print("Неделя "+str(i))
        name_for_table = "w"+str(i)
        d = "2021.W"+str(i)
        d_next = "2021.W"+str(i+1)
        r = datetime.datetime.strptime(d + '.1', "%Y.W%W.%w")
        monday = r.strftime("%y.%m.%d")
        r = datetime.datetime.strptime(d_next + '.1', "%Y.W%W.%w")
        monday_next = r.strftime("%y.%m.%d")
        name_for_google = "["+str(i)+"]"+ monday+"-"+monday_next
        def execu():
            global cursor
            cursor.execute("SELECT * FROM "+name_for_table)
            #create_list_in_google(name_for_google)
            rows = cursor.fetchall()
            for i in range(len(rows)):
                for j in range(len(rows[i])):
                    try:
                        int(rows[i][j])
                        mat_row[i][j]+=int(rows[i][j])
                    except Exception as ex:
                        print(ex)
                        mat_row[i][j]=rows[i][j]
            #update_rows(name_for_google, rows)


        try:
            execu()
        except Exception as ex:
            print(ex)
            time.sleep(5)
            execu()
    print(mat_row)
    update_rows("summa_eliz_minut", mat_row)

def update_rows(name, matr):
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(table_key)
    worksheet = sh.worksheet(name)
    for i in range(len(matr)): matr[i] = list(matr[i])
    worksheet.update('A2', matr)



get = refresh_token().json()
acc_token = get["access_token"]
ref_token = get["refresh_token"]
write_on_file("otus.txt", str(ref_token))

from_db_to_table()