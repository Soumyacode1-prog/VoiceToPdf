import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from reportlab.pdfgen import canvas
from word2number import w2n

# Load Vosk model
model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

q = queue.Queue()
items = []


def callback(indata, frames, time, status):
    q.put(bytes(indata))


print("🎤 Speak (say 'exit' to stop)...")

with sd.RawInputStream(
    samplerate=16000,
    blocksize=8000,
    dtype='int16',
    channels=1,
    callback=callback
):

    while True:
        data = q.get()

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()

            if not text:
                continue

            print("You said:", text)

            # ✅ Exit condition
            if any(word in text for word in ["exit", "stop", "quit"]):
                print("Exiting and generating PDF...")
                break

            words = text.split()
            price = ""

            # Extract numeric price
            for w in words:
                if w.replace('.', '').isdigit():
                    price = w
                    break

            # Convert word numbers
            if not price:
                try:
                    price = str(w2n.word_to_num(text))
                except:
                    price = ""

            # Extract item name
            item_name = " ".join(
                w for w in words
                if not w.replace('.', '').isdigit() and w != "rs"
            )

            if price:
                items.append((item_name, price))
                print(f"Added item: {item_name}  Rs {price}")
            else:
                print("Say item with price clearly")


# ✅ Generate PDF
c = canvas.Canvas("Items_Report.pdf")

c.setFont("Helvetica-Bold", 16)
c.drawString(100, 800, "Item Report")

c.setFont("Helvetica", 12)
y = 770
total = 0

for i, (name, price) in enumerate(items, 1):
    c.drawString(50, y, f"{i}. {name} ------------ Rs {price}")
    y -= 20

    try:
        total += int(float(price))
    except:
        pass

c.setFont("Helvetica-Bold", 12)
c.drawString(50, y - 10, f"Total Amount: Rs {total}")

c.save()

print("\n✅ Report PDF saved: Items_Report.pdf")