# AuraCards

https://auracards.onrender.com/

Turn your notes into flashcards, organise them into decks, and study at your own pace.

AuraCards runs on your computer. Upload **PDF, DOCX, or PPTX** files, generate cards, review the results, and start studying.

## What you can do

- Generate flashcards using the built-in offline generator, a local AI model, or optional Cloud AI.
- Edit questions and answers before saving.
- Create categories, organise decks, and delete categories while keeping their decks.
- Study with answer reveals, recall ratings, starred cards, and progress tracking.
- Choose themes, card animations, and heading styles.
- Connect the Focus companion to the separate Pomodoro app.
- Export and import your decks as a JSON backup.

## 1. Set up AuraCards

You need **Python 3.10 or newer**, a browser, and an internet connection for the initial dependency installation.

Download and extract the project. Open a terminal inside the folder containing `app.py` and `requirements.txt`.

### macOS / Ubuntu / Linux

Run these commands one at a time:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

If Ubuntu reports that `venv` is missing, install it, then repeat the setup:

```bash
sudo apt install python3-venv
```

### Windows

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

### Open the website

Visit **[http://localhost:5000](http://localhost:5000)** in your browser.

Keep the terminal open while using AuraCards. Press **Ctrl+C** in that terminal to stop the server.

Docker, Node.js, and a frontend build step are not required.

## 2. Start it next time

You only need to install dependencies once.

**macOS / Ubuntu / Linux:**

```bash
sh start.sh
```

**Windows:** double-click `start.bat`.

Then open [http://localhost:5000](http://localhost:5000).

## 3. Make your first deck

1. Click **Upload notes**.
2. Choose a PDF, DOCX, or PPTX file, up to **20 MB**.
3. Enter a deck name and select a category. Use **+ New** to create a category during upload.
4. Choose the card count, difficulty, and generation method.
5. Click **Generate cards**.
6. Review the draft. Edit questions or answers and remove unwanted cards before saving.
7. Open your deck and click **Study now**.

Clear headings and complete explanations help. The offline generator also recognises notes formatted as questions and answers. Image-only scans need OCR before uploading.

## Choose a generation method

| Method | Best for |
| --- | --- |
| **Offline · lightweight** | Quick generation without an AI model or API key; works best with structured notes. |
| **Local AI · llama.cpp** | Using your running local model to interpret notes and write cards. |
| **Local AI · Ollama** | Using an existing Ollama setup. |
| **Cloud AI · API key** | Optional OpenAI generation; requires a server-side API key, internet, and consent to send document text. API charges may apply. |

After setup, offline generation works without internet. Local AI also works offline when its model and server are already installed. Review AI-generated answers against their source excerpts.

## Use a local model with llama.cpp

If your model already runs in **llama-server**, leave it running and open **Upload notes → Local AI · llama.cpp**.

AuraCards checks local ports **8080, 8081, and 8000**. Select the detected model, then generate your cards. It supports different model names; it is not tied to Qwen.

For another port, expand **Server address**, enter its local URL, and click **Detect again**.

If you need to start a server, a typical command is:

```bash
llama-server -m /path/to/model.gguf --host 127.0.0.1 --port 8080 --ctx-size 8192
```

Replace the model path with your own GGUF file. Use a chat/instruct model with a working chat template and JSON output support. AuraCards connects to your server; it does not install or download the model.

### Pick a processing mode

| Mode | How it works | Processing budget |
| --- | --- | --- |
| **Flash** | Drafts directly from selected passages and runs automatic source, format, number, and duplicate checks. Skips concept mapping and separate model review. | Up to 3 minutes |
| **Balanced** | Maps concepts, drafts cards, and uses the model to review and repair them. | Up to 8 minutes |
| **Thorough** | Uses the same stages with higher limits for coverage and follow-up work. | Up to 15 minutes |

These are work limits, not expected completion times. Speed depends on your model, hardware, document, and card count.

For a quicker run, start with **Flash + Focused answers + 10 cards**. Choose **Expanded explanations** for fuller answers. Large requests or limited source material can produce fewer cards than requested.

See [LLAMA_CPP.md](LLAMA_CPP.md) for detailed setup and troubleshooting.

## Customise your study space

Open **Settings → Appearance** to change themes, card animations, or card headings.

Open **Settings → Categories** to add or delete categories. When deleting a category containing decks, choose where those decks should move.

The **Focus** companion connects to the separate Pomodoro project. Run that project's `server.py` in another terminal, then open Focus in AuraCards. See [LINKING.md](LINKING.md) for the full connection guide.

## Back up your cards

Use **Settings → Backup → Export backup** to download your decks as JSON. Use **Import JSON** to bring them back.

Decks and study progress live in your browser storage. Keep using the same browser profile and address: `localhost` and `127.0.0.1`, or different ports, have separate storage. Export a backup before clearing browser data, changing computers, or updating an existing installation.

## Common fixes

| Problem | What to do |
| --- | --- |
| Website will not open | Start `app.py` and keep its terminal open. Open the website URL rather than double-clicking `index.html`. |
| Port 5000 is busy | Run `.venv/bin/python app.py --port 5001` on macOS/Linux, or `.venv\Scripts\python.exe app.py --port 5001` on Windows. Open `http://localhost:5001`. Export/import existing decks when changing ports. |
| Local model is not detected | Check that `llama-server` is running. Enter its address and click **Detect again**. `llama-cli` alone does not provide the required server API. |
| Generation is slow | Try Flash, Focused answers, fewer cards, or a smaller document. |
| Old interface after updating | Restart AuraCards and hard-refresh: **Cmd+Shift+R** on Mac or **Ctrl+Shift+R** on Windows/Linux. |
| Focus shows offline | Start the separate Pomodoro server. Check [LINKING.md](LINKING.md) if you changed its port. |

## Built with

Python, Flask, HTML, CSS, and JavaScript, with Python libraries for extracting PDF, Word, and PowerPoint text.

