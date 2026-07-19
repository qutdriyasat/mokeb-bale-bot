from flask import Flask, request
import requests

from config import BASE_URL
from database import get_db
from states import *

app = Flask(__name__)
print("BOT STARTED")

def send(chat_id, text):
    try:
        requests.post(
            BASE_URL + "/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=10
        )
    except Exception as e:
        print(e)


@app.route("/", methods=["GET"])
def home():
    return "Mokeb Bale Bot Running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if not data or "message" not in data:
        return "ok"


    msg = data["message"]

    chat_id = msg["chat"]["id"]
    text = msg.get("text", "").strip()


    if chat_id not in users:
        users[chat_id] = {
            "state": NAME
        }


    state = users[chat_id]["state"]


    if text == "/start":

        users[chat_id] = {
            "state": NAME
        }

        send(
            chat_id,
            "👋 به ثبت نام موکب خوش آمدید.\n\nنام و نام خانوادگی را وارد کنید:"
        )

        return "ok"



    if state == NAME:

        users[chat_id]["full_name"] = text
        users[chat_id]["state"] = MOBILE

        send(chat_id, "📱 شماره موبایل را وارد کنید:")



    elif state == MOBILE:

        users[chat_id]["mobile"] = text
        users[chat_id]["state"] = NATIONAL

        send(chat_id, "🆔 کد ملی را وارد کنید:")



    elif state == NATIONAL:

        users[chat_id]["national_id"] = text
        users[chat_id]["state"] = PASSPORT

        send(chat_id, "📘 شماره گذرنامه را وارد کنید:")



    elif state == PASSPORT:

        users[chat_id]["passport"] = text
        users[chat_id]["state"] = GENDER

        send(
            chat_id,
            "👤 جنسیت را وارد کنید:\nمرد\nزن"
        )



    elif state == GENDER:

        users[chat_id]["gender"] = text
        users[chat_id]["state"] = DATE

        send(
            chat_id,
            "📅 تاریخ حضور در موکب را وارد کنید:"
        )



    elif state == DATE:

        users[chat_id]["arrival_date"] = text


        data = users[chat_id]


        conn = get_db()

        conn.execute(
            """
            INSERT OR REPLACE INTO registrations
            (
                chat_id,
                full_name,
                mobile,
                national_id,
                passport,
                gender,
                arrival_date
            )
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                chat_id,
                data["full_name"],
                data["mobile"],
                data["national_id"],
                data["passport"],
                data["gender"],
                data["arrival_date"]
            )
        )


        conn.commit()
        conn.close()


        users.pop(chat_id)


        send(
            chat_id,
            "✅ ثبت نام شما با موفقیت انجام شد."
        )


    return "ok"
