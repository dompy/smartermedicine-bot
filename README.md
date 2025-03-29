# 📚 SmarterMedicine AutoBot

Ein vollautomatischer Bot zur Durchführung von E-Learnings auf [smartermedicine.easylearn.ch](https://smartermedicine.easylearn.ch) – inklusive Slide-Navigation, Quizbeantwortung via GPT-4 und automatischem Login.

---

## 🔥 Features

- Automatischer Login via `.env`
- Erkennung & Klick auf "Next"-Button (rekursiv durch Frames)
- Quizfragen-Erkennung per OCR (Tesseract)
- Beantwortung der Fragen über GPT-4
- Debug-Screenshots (`debug.png`)

---

## 🧰 Voraussetzungen

- Python >= 3.11
- Eine `.env` Datei mit:

```env
OPENAI_API_KEY=sk-...
USERNAME=deinbenutzername
PASSWORD=deinpasswort
```

---

## 🛠️ Installation

```bash
git clone https://github.com/deinbenutzer/MedMate.git
cd MedMate/smartermedicine-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Falls `requirements.txt` fehlt:

```bash
pip install python-dotenv playwright openai pillow pytesseract
playwright install
```

---

## 🚀 Starten

```bash
python main.py
```

---

## ⚙️ Was passiert intern?

1. Der Bot loggt sich automatisch ein.
2. Du wählst dein gewünschtes E-Learning manuell aus.
3. Sobald der neue Tab geöffnet ist, übernimmt der Bot:
   - Klickt durch Slides
   - Erkennt Quizfragen per Screenshot & OCR
   - Fragt GPT-4 nach der Antwort
   - Klickt die Antwort & submitted sie

---

## ⚠️ Hinweise

- Der Bot ist nur zur eigenen Lernunterstützung gedacht.
- Du trägst die Verantwortung für die Richtigkeit der Antworten.

---

## 🖼️ Debug

Alle Screenshots werden als `debug.png` gespeichert (immer überschrieben).

---

## 🤝 Lizenz

MIT License
