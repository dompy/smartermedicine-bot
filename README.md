# 🤖 SmarterMedicine Autobot

Dieses Python-Tool automatisiert das Durcharbeiten von E-Learning-Kursen auf [smartermedicine.easylearn.ch](https://smartermedicine.easylearn.ch) mithilfe von:

- 🧠 GPT-4 (OpenAI)
- 📸 OCR (Tesseract)
- 🎭 Playwright (Browsersteuerung)

---

## ⚙️ Funktionen

- Automatischer Login mit gespeicherten Zugangsdaten
- Automatisches Klicken durch Slides
- Erkennung von Quizfragen via Screenshot & OCR
- Beantwortung von Multiple-Choice-Fragen durch GPT-4
- Klicken der korrekten Antwort + "Submit" → Weiter

---

## 🚀 Setup

### 1. Repository klonen

```bash
git clone https://github.com/deinuser/smartermedicine-bot.git
cd smartermedicine-bot
```

### 2. Virtuelle Umgebung erstellen

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
playwright install
```

### 4. `.env` Datei anlegen

Erstelle eine Datei `.env` mit folgendem Inhalt:

```
OPENAI_API_KEY=dein-openai-key
USERNAME=dein-login
PASSWORD=dein-passwort
```

(Hinweis: Diese Datei ist bereits in `.gitignore` ausgeschlossen.)

---

## ▶️ Ausführung

```bash
python main.py
```

1. Tool loggt sich automatisch ein  
2. Starte das gewünschte E-Learning manuell  
3. Drücke ENTER sobald du auf der ersten Slide bist  
4. Der Bot übernimmt von da an automatisch

---

## 📦 Verzeichnisstruktur

```text
smartermedicine-bot/
├── main.py             # Hauptskript
├── .env                # Login + API-Key (nicht committen!)
├── .env.example        # Vorlage für eigene .env
├── README.md
├── debug.png           # Letzter Screenshot (zur Analyse)
├── venv/               # Lokale virtuelle Umgebung
```

---

## 🧠 Hinweis

Dieses Tool ist rein zu Lern- und Demonstrationszwecken gedacht. Bitte beachte die Nutzungsbedingungen der jeweiligen Plattform.

---
