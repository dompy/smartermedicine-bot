import os
import asyncio
import base64
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from openai import OpenAI
from PIL import Image
import pytesseract

# .env laden
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

client = OpenAI(api_key=OPENAI_API_KEY)

if not OPENAI_API_KEY or not USERNAME or not PASSWORD:
    raise ValueError("❌ .env muss OPENAI_API_KEY, USERNAME und PASSWORD enthalten!")

# Screenshot als base64 kodieren und speichern
async def take_screenshot_base64(page):
    screenshot = await page.screenshot(path="debug.png", full_page=False)
    print("🖼️ Screenshot gespeichert als debug.png")
    return base64.b64encode(screenshot).decode("utf-8")

# OCR-Text extrahieren
def extract_text_with_ocr():
    try:
        image = Image.open("debug.png")
        text = pytesseract.image_to_string(image)
        print("🔍 OCR-Text extrahiert:")
        print(text[:300])
        return text
    except Exception as e:
        print(f"❌ OCR-Fehler: {e}")
        return ""

# GPT-Antwort holen (Text statt Vision)
async def get_answer_from_text(text):
    try:
        prompt = (
            "Hier ist eine Multiple-Choice-Frage:\n\n"
            f"{text}\n\n"
            "Was ist die richtige Antwort? Gib nur den Buchstaben zurück (z. B. A, B, C, D)."
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=10
        )
        return response.choices[0].message.content.strip().upper()
    except Exception as e:
        print(f"❌ GPT-Fehler: {e}")
        return ""

# REKURSIVER Frame-Scan für Next-Button oder Continue-Button
async def click_next_button_recursive(frame):
    selectors = [
        'button:has-text("Next")',
        'button:has-text("Continue")',  # Hinzugefügt: Continue-Button
        ".navigation-controls__button_next",
        "button.uikit-primary-button_next"
    ]
    for selector in selectors:
        try:
            next_button = await frame.query_selector(selector)
            if next_button and await next_button.is_visible():
                await next_button.click()
                print(f"➡️ Weiter mit Button: {selector}")
                return True
        except:
            continue
    # Kinderframes prüfen
    for child in frame.child_frames:
        if await click_next_button_recursive(child):
            return True
    return False


# Hauptfunktion
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Automatischer Login
        await page.goto("https://smartermedicine.easylearn.ch/login")
        await page.fill("#username", USERNAME)
        await page.fill("#password", PASSWORD)
        await page.click("[name='_submit']")
        print("🔐 Login durchgeführt.")

        await page.wait_for_timeout(3000)
        print("🌐 Katalog geladen. Bitte starte dein gewünschtes E-Learning.")
        input("➡️ Drücke ENTER, sobald du auf der ersten Slide bist...")

        # Warten auf neuen Tab (E-Learning)
        while len(context.pages) == 1:
            print("⌛ Warte auf neues E-Learning-Tab...")
            await asyncio.sleep(1)
        page = context.pages[-1]  # neuester Tab
        await page.bring_to_front()
        print("🗂️ Tab gewechselt – E-Learning erkannt.")

        while True:
            clicked = await click_next_button_recursive(page.main_frame)
            if clicked:
                await page.wait_for_timeout(1500)
                continue
            print("🔍 Kein Next-Button gefunden oder nicht sichtbar")

            try:
                await take_screenshot_base64(page)
                text = extract_text_with_ocr()
                print("📨 Sende OCR-Text an GPT...")
                answer = await get_answer_from_text(text)
                print(f"✅ GPT sagt: {answer}")

                # Antwort auswählen (manuell)
                if answer:
                    await page.get_by_text(answer, exact=False).first.click()  # Klick auf Antwort
                    print(f"🖱️ Antwort {answer} angeklickt")
                else:
                    print("⚠️ Keine gültige Antwort erhalten.")
            except Exception as e:
                print(f"❌ Antwort konnte nicht geklickt werden: {e}")

            try:
                await page.click("text=Submit")
                print("📤 Antwort abgeschickt.")
            except:
                print("⚠️ Kein Submit gefunden – evtl. auto weiter")
                
            await page.wait_for_timeout(2000)

            # Neue Eingabeaufforderung für ENTER, bevor es weitergeht
            input("✅ Drücke ENTER, um mit der nächsten Folie fortzufahren...")

            # Suche den "Next" oder "Continue"-Button nach der Frage
            clicked = await click_next_button_recursive(page.main_frame)
            if not clicked:
                print("🛑 Kein weiterer Next/Continue-Button – vermutlich fertig")
                break

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())