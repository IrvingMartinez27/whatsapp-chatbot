from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

@app.route("/saludar", methods=["GET"])
def saludar():
    return "Servidor funcionando Hi"

@app.route("/whatsapp", methods=["GET"])
def VerifyToken():
    try:
        access_token = "asdasd"
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == access_token:
            return challenge
        else:
            return "error", 400
    except:
        return "error", 400

def whatsappService(body):
    try:
        token = "EAAMtlIjZBjLwBRrYkQahTJLlcPahG7WM9aeXqjZBKCCqp8wEZBkohXrJU5j69wEuqE8ntN4URSj7BXWZCphI1i0ZBJu3DdA6Y8GNV3P0xu3MHrjYpXGsZB7sLNAL6keeOuXjFCxZBj9aZAVEKSQgNkKAxGLJP82IsChN4iN5OoBZCLF5qhgyekiXqwJT93hTTZBK1NBQZDZD"
        api_url = "https://graph.facebook.com/v22.0/1098506706683416/messages"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(api_url, data=json.dumps(body), headers=headers)
        if response.status_code == 200:
            print("Mensaje enviado correctamente")
            return True
        else:
            print("Error al enviar el mensaje:", response.text)
            return False
    except Exception as e:
        print("Ocurrió un error con la API:", str(e))
        return False

def enviarmensaje(text, numero):
    body = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {
            "body": "Esta es la respuesta a la pregunta: " + text
        }
    }
    return body

@app.route("/whatsapp", methods=["POST"])
def RecibirMensaje():
    try:
        body = request.get_json()
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value["messages"][0]
        text = messages["text"]
        question_user = text["body"]
        number = messages["from"]
        print("Mensaje recibido de:", question_user)
        body_answer = enviarmensaje(question_user, number)
        send_message = whatsappService(body_answer)
        if send_message:
            print("Mensaje enviado correctamente")
        else:
            print("Error al enviar el mensaje")
        return "EVENT_RECEIVED"
    except Exception as e:
        print("Ocurrió un error al procesar el mensaje:", str(e))
        return "EVENT_RECEIVED"
    print("Número destinatario:", number)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8502))
    app.run(host="0.0.0.0", port=port, debug=True)