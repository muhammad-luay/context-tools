# Project Combiner (`combine-files`)

`project-combiner` is a powerful and flexible command-line tool for concatenating text-based files within a directory tree. It's designed to be intuitive, fast, and highly configurable, making it easy to bundle source code, documentation, or any text-like files for analysis, distribution, or large language model contexts.

[![PyPI version](https://badge.fury.io/py/project-combiner.svg)](https://badge.fury.io/py/project-combiner)

## Highlights

- **Intuitive CLI**: Powered by Typer, providing a rich `--help` experience and shell completion.
- **Cross-Platform**: Uses `pathlib.Path` for seamless operation on Windows, macOS, and Linux.
- **Highly Configurable**: Control everything with command-line flags—no hard-coding required. Specify what to include, what to skip, file encodings, output location, and more.
- **`.gitignore` Aware**: Automatically respects your project's `.gitignore` rules (requires `pathspec`).
- **Smart File Handling**: Skips binary files based on MIME types to prevent garbage output **and, by default, any
  directory whose name starts with `.`** (override with `--include-dot-dirs`).
- **Performance-Oriented**: Features optional multithreaded file reading and a `tqdm` progress bar for large projects.
- **Flexible Output**: Stream combined content to standard output (`stdout`) or save it directly to a file.

* **Clipboard‑Ready**: Use `-c/--clipboard` to copy the combined output straight to your system clipboard (requires `pyperclip`).

## Installation

You can install `project-combiner` directly from PyPI.

#### Full Feature Set

For all features, including `.gitignore` support and a progress bar, install with the `[all]` extra:

```bash
pip install project-combiner[all]
```

This installs `typer`, `pathspec`, and `tqdm`.

#### Minimal Installation

For the core functionality without optional dependencies:

```bash
pip install project-combiner
```

> ℹ️ Add clipboard support later with:
>
> ```bash
> pip install pyperclip
> ```

---

## Usage

The basic command is `combine-files`, followed by the path to the directory you want to process and any desired options.

```bash
combine-files [ROOT_DIRS]... [OPTIONS]
```

### Command-Line Options

| Option                                 | Alias | Description                                                                            | Default                    |
| -------------------------------------- | ----- | -------------------------------------------------------------------------------------- | -------------------------- |
| `--output-file, -o`                    |       | Path to the output file. Use `-` for stdout.                                           | `-` (stdout)               |
| `--skip-dirs`                          |       | Space-separated list of directory names to skip.                                       | `.git` `.hg` `__pycache__` |
| `--skip-files`                         |       | Space-separated list of file names to skip.                                            |                            |
| `--skip-exts`                          |       | Space-separated list of file extensions to skip.                                       |                            |
| `--preview-exts`                       |       | Space-separated list of extensions to preview instead of including their full content. |                            |
| `--encoding`                           |       | The encoding to use for reading files.                                                 | `utf-8`                    |
| `--jobs, -j`                           |       | Number of parallel threads for reading files.                                          | `2`                        |
| `--progress`                           |       | Show a progress bar during file processing (requires `tqdm`).                          |                            |
| `--follow-symlinks`                    |       | Follow symbolic links.                                                                 | `False`                    |
| `--skip-dot-dirs / --include-dot-dirs` |       | Skip directories that start with `.` (dot). Use the second form to include them.       | `--skip-dot-dirs`          |
| `--log-level`                          |       | Set the logging level (e.g., `DEBUG`, `INFO`).                                         | `WARNING`                  |
| `--version`                            |       | Show the version and exit.                                                             |                            |
| `--help`                               |       | Show the help message and exit.                                                        |                            |

---

## Example Scenario

Let's walk through how to use `project-combiner` with a typical project structure.

### Sample Project Structure

Imagine you have a project with the following layout:

```
my_project/
├── .gitignore
├── src/
│   ├── main.py
│   ├── utils.py
│   └── data/
│       ├── data.csv
│       └── notes.txt
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── docs/
│   ├── guide.md
│   └── reference.md
├── .venv/
│   └── ... (virtual environment files)
└── README.md
```

Your `.gitignore` file might look like this:

```
# .gitignore
.venv/
__pycache__/
*.log
```

### Use Cases

#### 1. Combine All Relevant Files

To combine all text-based files in the project while respecting the `.gitignore` file, simply run:

```bash
combine-files my_project
```

- **What it does**: It will walk through `my_project`, skip the `.venv` directory (as specified in `.gitignore`), and concatenate the contents of all other text files (`.py`, `.csv`, `.txt`, `.md`).
- **Output**: The combined content is printed to the terminal (`stdout`).

#### 2. Save the Combined Output to a File

To save the output into a single file named `combined_output.txt`:

```bash
combine-files my_project -o combined_output.txt
```

- **What it does**: Same as the first example, but the result is written to `combined_output.txt` instead of the console.

#### 3. Exclude the `tests` Directory

If you want to combine only the application source code and documentation, excluding the tests:

```bash
combine-files my_project --skip-dirs tests
```

- **What it does**: This command will skip the `tests/` directory in addition to the patterns in `.gitignore`. The output will contain files from `src/` and `docs/`.

#### 4. Combine Only Python Source Files

To isolate just the Python source code from the `src` directory:

```bash
combine-files my_project/src --skip-exts .csv .txt .md
```

Or, more simply, if you only want to process the `src` folder:

```bash
combine-files my_project/src
```

Assuming `data` contains non-python files, they will be skipped if they are binary or if you explicitly skip their extensions.

#### 5. Preview Large Data or Markdown Files

Sometimes you don't want the full content of large data files or verbose documentation. You can "preview" them instead.

```bash
combine-files . --preview-exts .md .csv -j 4 --progress
```

- **What it does**:
  - It processes the entire project (`.`).
  - For any file ending in `.md` or `.csv`, it will only include a header indicating the file's path and a "preview" message, rather than its full content.
  - It uses 4 threads (`-j 4`) for faster reading and shows a progress bar (`--progress`).

The output for a previewed file like `docs/guide.md` would look like this:

```
---
File: docs/guide.md (preview)
---
```

### 6. Copy Output Directly to Clipboard

```bash
combine-files . -c
```

No file writing or terminal spam—your combined content is ready to paste.

---

## Advanced Usage

### Working with Encodings

If your project uses a different file encoding, you can specify it with the `--encoding` flag. For example, for projects using legacy Windows encodings:

```bash
combine-files . --encoding cp1252
```

### Performance

For very large projects with thousands of files, you can speed up the process by increasing the number of threads. A good starting point is the number of cores on your CPU.

```bash
# Use 8 threads to read files
combine-files . -j 8 --progress
```

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, feel free to open an issue or submit a pull request on the project's repository.

## Project Links

- **Source & Issue Tracker**: <https://github.com/muhammad-luay/context-tools>
- **PyPI**: <https://pypi.org/project/project-combiner/>

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
