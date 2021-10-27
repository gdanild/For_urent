# -*- coding: utf-8 -*-
import requests, csv, time, datetime
acc_token =""
def write_data(row):
    exampleFile = open("base_users.csv", 'a', encoding='UTF-8', newline='')
    exampleWriter = csv.writer(exampleFile, delimiter=';')
    exampleWriter.writerow(row)
    exampleFile.close()

def read_data(phone):
    a = open("base_users.csv","r+",encoding="utf8")
    reader = csv.reader(a, delimiter=';')
    value = len(list(reader))
    print(value)

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


def get_zones(num):
    BASE_URL = 'https://service.urentbike.ru/customers/api/customers?filter={"text":""}&cPage='+ str(num) +'&iOnPage=1000'

    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "ADR",
        "X-Selected-Vendors": "ADR",
        "Authorization": "Bearer " + acc_token,
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
        "Content-Type": "application/x-www-form-urlencoded"
    }


    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        auth_response = get_zones(num)
    if (auth_response.status_code != 200):
        auth_response.json()
        return False
    return auth_response




def refresh_token():
    get = read_on_file()
    BASE_URL = 'https://service.urentbike.ru:10000/connect/token'
    data = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "NVU",
        "X-Selected-Vendors": "NVU",
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru:10000",
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
    global acc_token
    acc_token = auth_response.json()["access_token"]
    print(auth_response.json()["access_token"])
    write_on_file("otus.txt", str(auth_response.json()["refresh_token"]))
    return auth_response

get = refresh_token().json()
acc_token = get["access_token"]
ref_token = get["refresh_token"]
write_on_file("otus.txt", str(ref_token))
n = 7594
while True:
    print("начал скачивать")
    result = get_zones(n).json()
    print(result)
    print("скачал")
    result = result["entries"]
    for i in result:
        photo = str(i["relativePhotoUrl"])
        url_photo = "None"
        if photo != "None" and photo[0] == "C":
            url_photo = "https://service.urentbike.ru/file/" + photo
        row = [i["patronymic"],i["name"],i['surname'], i["createDateTimeUtc"],i["email"],i["phoneNumber"],i['statistics']["elapsedSeconds"],i['statistics']["distance"],i['statistics']["tripCount"],url_photo]
        write_data(row)
    print("Сделал до Н включительно: "+ str(n))
    n+=1

