from flask import Flask, request, jsonify
import requests
import os
import sys  # Para que Render imprima los errores en logs

app = Flask(__name__)

# 🔐 Credenciales de Twilio (reales para cuenta Trial)
TWILIO_SID = "ACd7f136c6cf64a754606ef982d884bac7"
TWILIO_AUTH_TOKEN = "5a6119ffcc8a3fbfcb3e7bd0a3fbfbfb"
TWILIO_NUMBER = "whatsapp:+14155238886"  # Número de origen asignado por Twilio

# 📱 Número de Jona (el único verificado en Twilio Trial)
NUMERO_JONA = "whatsapp:+5491124591988"

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

    # 💬 Armar mensaje para enviar a Marina
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
                "To": NUMERO_JONA,
                "Body": mensaje
            }
        )

        if response.status_code == 201:
            return jsonify({"estado": "Mensaje enviado a Jona correctamente ✅"})
        else:
            print("❌ Error Twilio:", response.text, file=sys.stderr)
            return jsonify({
                "error": "No se pudo enviar el mensaje a Jona.",
                "detalle": response.text
            }), 500

    except Exception as e:
        print("❌ Error interno:", e, file=sys.stderr)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

