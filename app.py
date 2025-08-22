import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone, timedelta
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Reconstruction du dict de config Firebase depuis les variables d'environnement
firebase_config = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID").replace('\\n', '\n'),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
}

# Initialisation de Firebase Admin SDK avec dict au lieu du fichier JSON
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configuration Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Aucune question fournie"}), 400

    # Lecture du contexte (RAG)
    try:
        with open("prompt_context.txt", "r", encoding="utf-8") as f:
            context = f.read()
    except FileNotFoundError:
        return jsonify({"error": "Fichier prompt_context.txt introuvable."}), 500
    except Exception as e:
        return jsonify({"error": f"Erreur en lisant le fichier : {str(e)}"}), 500

    final_prompt = final_prompt = (
        "Tu es un assistant étudiant bienveillant et compétent. "
        "Tu aides à comprendre les cours, à résoudre des exercices, à écrire des algorithmes, et à utiliser des outils comme Algobox ou Pascal.\n\n"
        f"Voici un extrait de cours :\n{context}\n\n"
        f"Question de l'utilisateur : {question}\n\n"
        "Ta réponse doit :\n"
        "- Être **basée uniquement sur les informations contenues dans le texte** ci-dessus.\n"
        "- Être claire, concise et compréhensible pour un étudiant débutant.\n"
        "- Ne pas inventer d'informations hors contexte.\n"
        "- Si la réponse ne peut pas être donnée à partir du document, **n'invente rien** : explique gentiment que la réponse ne figure pas dans l'extrait et invite l'utilisateur à préciser.\n\n"
        "Commence toujours par une salutation brève si la question est ouverte. Sinon, donne directement la réponse attendue."
    )

    try:
        response = model.generate_content(final_prompt)
        answer = response.text.strip()

        # Détection améliorée des réponses vagues ou génériques
        vague_phrases = [
            "ce document", "ce texte", "cet extrait", "ce contenu", "ce passage", "ce cours",
            "il s'agit", "le document", "dans ce cours", "cet article"
        ]

        if any(phrase in answer.lower() for phrase in vague_phrases) and not context.lower().strip() in answer.lower():
            answer = (
                "Bonjour ! Je suis un assistant étudiant. Pose-moi une question précise sur un extrait de cours ou une notion. "
                "Je te répondrai en me basant uniquement sur le contenu fourni."
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Générer le timestamp local à chaque requête
    utc_plus_2 = timezone(timedelta(hours=2))
    timestamp = datetime.now(utc_plus_2).isoformat()

    # Sauvegarde dans Firestore
    db.collection("interactions").add({
        "question": question,
        "reponse": answer,
        "timestamp": timestamp
    })

    return jsonify({"answer": answer})

@app.route('/interactions', methods=['GET'])
def get_interactions():
    docs = db.collection("interactions").order_by(
        "timestamp", direction=firestore.Query.DESCENDING  # du plus récent au plus ancien
    ).limit(20).stream()

    interactions = [doc.to_dict() for doc in docs]
    return jsonify(interactions)

@app.route("/clear", methods=["DELETE"])
def clear_history():
    for doc in db.collection("interactions").stream():
        doc.reference.delete()
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
