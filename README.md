AI Chatbot Assistant

Quick start

1. (Recommended) Create & activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install requirements:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

3. Set your OpenAI API key (option A or B):

A) set environment variable (recommended):

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

B) create a local `.env` file with `OPENAI_API_KEY=...` or paste it into the app UI (in the API Key expander)

4. Run the app:

```bash
streamlit run app.py
```

If `streamlit` is not found on your shell PATH, use:

```bash
python -m streamlit run app.py
```

You can also use `run_app.bat` on Windows or `run_app.sh` in Git Bash.

Important points in regards to the project
- The app stores the API key only in the Streamlit session state, not on disk.
- A local `.env` file is ignored by git and is the easiest way to keep the key available when you run the app.
- To run from anywhere without `python -m`, add your Python Scripts folder to PATH (e.g. `C:\Users\cason\AppData\Roaming\Python\Python313\Scripts`).
