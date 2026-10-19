from flask import Flask, request
import requests

app = Flask(__name__)

# توكن الصفحة الحقيقي الخاص بك
PAGE_ACCESS_TOKEN = "EAA78DMfASO0BS6PPyyYOgiZC4aoebbWZBA6hXN3ZBYFoXZAjeIuuFTd81zWRVSqSzrS4AWRSjVy7nLTlMqstxZAg3d4nMrp1j16XZA1XemWljgZBNzUfUFJXY8MIUzjHPI0lElalKm9oVZBQQm7JDgbDJxCDnBa0fct7000ZAbBYZArZBsg1YgpbqKTYqtqFJt1dejCDNOy5ASpYQZDZD"


# دالة زخرفة الأسماء التلقائية
def decorate_name(text):
  if not text:
    return "✦ اسم فارغ ✦"
  return f"𝑩𝑶𝑻 ✦ {text} ✦ 𝑩𝑶𝑻"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  if request.method == "GET":
    # التحقق من الـ Webhook مع فيسبوك
    MODE = request.args.get("hub.mode")
    TOKEN = request.args.get("hub.verify_token")
    CHALLENGE = request.args.get("hub.challenge")

    if MODE and TOKEN:
      if MODE == "subscribe" and TOKEN == "my_secure_token":
        return CHALLENGE, 200
      else:
        return "Verification failed", 403
    return "Bot Server is Running!", 200

  elif request.method == "POST":
    data = request.json
    if data.get("object") == "page":
      for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
          if messaging_event.get("message"):
            sender_id = messaging_event["sender"]["id"]
            message_text = messaging_event["message"].get("text")

            if message_text:
              # زخرفة النص المرسل من المستخدم
              decorated_text = decorate_name(message_text)

              # إرسال النتيجة المزخرفة للمستخدم عبر الماسنجر
              send_message(
                  sender_id, f"إليك اسمك المزخرف:\n\n{decorated_text}"
              )

    return "ok", 200


def send_message(recipient_id, message_text):
  url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
  payload = {
      "recipient": {"id": recipient_id},
      "message": {"text": message_text},
  }
  headers = {"Content-Type": "application/json"}
  requests.post(url, json=payload, headers=headers)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
      
