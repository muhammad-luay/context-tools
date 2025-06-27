# 🧩 Context Tools — File Combiner Utility

This Python script helps you generate a single, unified text file by walking through a folder (e.g., a project directory) and extracting the contents of text/code files. It's ideal for:

- Sharing full project context in a single file (for ChatGPT, Claude, etc.)
- Reviewing large codebases more efficiently
- Exporting a summary of a folder’s contents without including binaries or dependencies

---

## 📦 Features

- ✅ Skips common junk folders (`venv`, `.git`, `__pycache__`, etc.)
- ✅ Filters out large/binary/unwanted files (`.db`, `.env`, `.DS_Store`, etc.)
- ✅ Partial preview for large files (e.g., `.csv`, `.json`)
- ✅ Truncates long outputs to avoid memory overload
- ✅ Easy to customize for your project structure

---

## 🛠️ Usage

### 1. Clone the repo

```bash
git clone https://github.com/muhammad-luay/context-tools.git
cd context-tools
````

### 2. Run the script

```bash
python context.py
```

---

## 🧪 Example Output Format

Each file gets grouped like this:

```
================================================================================
FILE: /Users/luay/myproject/app/main.py
--------------------------------------------------------------------------------
def hello():
    print("Hello World")

...

```

---

## ⚙️ Customization

You can adjust:

* `SKIP_DIRS`, `SKIP_FILES`, `SKIP_EXTS` → what to ignore
* `PREVIEW_EXTS`, `PREVIEW_NUM_LINES` → how large files are previewed

---

## 📜 License

MIT — free to use, share, modify. Attribution appreciated.

---

## 🧠 Tip

Pair this tool with a ChatGPT prompt like:

> “You are a senior software engineer. Here is the structure of my entire codebase — help me refactor, debug, or analyze it.”

```

