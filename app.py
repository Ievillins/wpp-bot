from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from boletos import buscar_boleto

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body", "").strip().lower()
    resp = MessagingResponse()

    if msg in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]:
        resp.message("Olá! Como posso te ajudar?\n1 - Segunda via de boleto\n2 - Falar com um atendente")
    elif msg == "1":
        resp.message("Por favor, envie seu CNPJ ou número do pedido.")
    elif msg == "2":
        resp.message("Certo! Encaminhando para um atendente. Aguarde um momento.")
    else:
        link = buscar_boleto(msg)
        if link:
            resp.message(f"Aqui está sua segunda via do boleto:\n{link}")
        else:
            resp.message("Desculpe, não encontrei nenhum boleto com esse dado.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
