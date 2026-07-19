from flask import Flask, request
import requests

from config import BASE_URL
from database import get_db
from states import *

app = Flask(__name__)


def send(chat_id, text):

    requests.post(
        BASE_URL + "/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )


@app.route("/", methods=["POST"])
def webhook():

    data = request.json

    if not data or "message" not in data:
        return "ok"

    msg = data["message"]

    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")


    if chat_id not in users:
        users[chat_id] = {"state": NAME}


    state = users[chat_id]["state"]


    if text == "/start":

        users[chat_id] = {
            "state": NAME
        }

        send(chat_id, "نام و نام خانوادگی را وارد کنید")
        return "ok"


    if state == NAME:

        users[chat_id]["full_name"] = text
        users[chat_id]["state"] = MOBILE

        send(chat_id, "شماره موبایل را وارد کنید")


    elif state == MOBILE:

        users[chat_id]["mobile"] = text
        users[chat_id]["state"] = NATIONAL

        send(chat_id, "کد ملی را وارد کنید")


    elif state == NATIONAL:

        users[chat_id]["national_id"] = text
        users[chat_id]["state"] = PASSPORT

        send(chat_id, "شماره گذرنامه را وارد کنید")


    elif state == PASSPORT:

        users[chat_id]["passport"] = text
        users[chat_id]["state"] = GENDER

        send(chat_id, "جنسیت را وارد کنید (مرد/زن)")


    elif state == GENDER:

        users[chat_id]["gender"] = text
        users[chat_id]["state"] = DATE

        send(chat_id, "تاریخ حضور در موکب را وارد کنید")


    elif state == DATE:

        users[chat_id]["arrival_date"] = text


        d = users[chat_id]

        conn = get_db()

        conn.execute("""
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
        d["full_name"],
        d["mobile"],
        d["national_id"],
        d["passport"],
        d["gender"],
        d["arrival_date"]
        ))

        conn.commit()
        conn.close()


        users.pop(chat_id)

        send(chat_id,"✅ ثبت نام انجام شد")


    return "ok"


@app.route("/", methods=["GET"])
def home():
    return "Mokeb Bale Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
