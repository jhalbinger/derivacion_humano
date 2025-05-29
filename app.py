from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔐 Datos de autenticación de Twilio
TWILIO_SID = "ACd7f136c6cf64a754606ef982d884bac7"
TWILIO_AUTH_TOKEN = "79f8320640a3cbb915bcc79c358336a8"
TWILIO_NUMBER = "whatsapp:+14155238886"  # Número de WhatsApp de Twilio

# 📱 Número de Marina (destino de la alerta)
NUMERO_MARINA = "whatsapp:+5491140991878"

@app.route("/")
def index():
    return "✅ Microservicio operativo."

@app.route("/derivar-humano", methods=["POST"])
def derivar_humano():
    datos = request.get_json()
    numero_cliente = datos.get("numero", "").strip()
    motivo = datos.get("motivo", "").strip()

    if not numero_cliente or not motivo:
        return jsonify({"error": "Falta el número o el motivo"}), 400

    mensaje = (
        f"📩 Usuario {numero_cliente} pidió hablar con un humano.\n"
        f"📝 Motivo: {motivo}"
    )

    try:
        response = requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
            auth=(TWILIO_SID, TWILIO_AUTH_TOKEN),
            data={
                "From": TWILIO_NUMBER,
                "To": NUMERO_MARINA,
                "Body": mensaje
            }
        )

        if response.status_code == 201:
            return jsonify({"estado": "Mensaje enviado a Marina correctamente ✅"})
        else:
            return jsonify({
                "error": "No se pudo enviar el mensaje a Marina.",
                "detalle": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
