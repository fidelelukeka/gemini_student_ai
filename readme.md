# Assistant IA Étudiant (Flask + Gemini + Firebase)

Ce projet est une application web intelligente permettant aux étudiants de poser des questions pédagogiques et de recevoir des réponses contextualisées grâce à l'IA de Google (Gemini), hébergée avec Google Cloud Run.

---

## 🚀 Fonctionnalités principales

- 🔍 Interaction Question / Réponse avec Gemini API
- 🧠 Intégration de contexte pédagogique via fichier `prompt_context.txt`
- 💬 Interface web simple avec HTML + CSS responsive (mobile-friendly)
- ☁️ Hébergement backend Flask sur Google Cloud Run
- 🔥 Sauvegarde des interactions dans Firebase Firestore
- ✅ CORS activé

---

## 🗂️ Structure du projet

```
/edu_gemini_ai
├── app.py                # Backend Flask principal
├── templates/
│   └── index.html        # Interface utilisateur (mobile responsive)
├── static/
│   └── style.css         # Design de l’interface
├── prompt_context.txt    # Contexte utilisé pour les réponses IA
├── firebase_config.json  # Configuration Firebase Admin SDK
├── requirements.txt      # Dépendances Python
└── Dockerfile            # Pour déploiement sur Cloud Run
```

---

## ⚙️ Installation locale (développement)

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
python app.py
```

Accessible sur `http://localhost:8080`

---

## ☁️ Déploiement sur Google Cloud Run

```bash
gcloud run deploy assistant-etudiant --source . --region us-central1 --allow-unauthenticated
```

Après déploiement, une URL publique sera fournie. Exemple :
```
https://assistant-etudiant-xxxxx.a.run.app
```

---

## 📱 Responsive design mobile

L’interface HTML a été adaptée avec :

- Flexbox + media queries CSS
- Un champ de saisie fluide
- Une disposition mobile first

---

## 🧠 Bonus / Améliorations possibles

- 🔒 Auth Firebase (restreindre accès)
- 📤 Export Firestore en CSV
- 📈 Intégrer analytics Firebase ou GA4

---

## 👤 Auteur

Fidèle Lukeka – Projet BuildWithAi GDG on Campus UCB

✉️ Contact : 
+243 827 808 428
+243 979 413 421
fidelelukeka@gmail.com

Gloire Mikololombi – Projet BuildWithAi GDG on Campus UCB

✉️ Contact : 
+243 836 879 425

---

## 📄 Licence

Projet open source – MIT License

