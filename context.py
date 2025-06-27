import os
import itertools   # new

# Folders to skip entirely
SKIP_DIRS  = {'venv', '.venv', 'node_modules', '.git', 'alembic', '__pycache__'}
# Exact filenames to skip
SKIP_FILES = {'package-lock.json', '.gitignore', '.DS_Store', '.env'}
# File extensions to skip outright
SKIP_EXTS  = {'.db'}

# --- NEW “preview-only” knob -----------------------------------------------
PREVIEW_EXTS       = {'.csv', '.json'}   # any extension you only want a head-preview for
PREVIEW_NUM_LINES  = 10                  # how many lines to keep for those files
# ---------------------------------------------------------------------------

def combine_files_to_single_txt(base_dir, section='all', output_path='combined_output.txt'):
    """
    Walk base_dir (or its backend/frontend sub-folder), copy every text file into
    a single text file, but for extensions listed in PREVIEW_EXTS only copy the
    first PREVIEW_NUM_LINES lines.
    """
    if section not in ('backend', 'frontend', 'all'):
        raise ValueError("section must be 'backend', 'frontend', or 'all'")

    # Decide which roots to walk
    if section == 'all':
        subs = [base_dir]
    else:
        subs = [os.path.join(base_dir, section)]

    with open(output_path, 'w', encoding='utf-8') as out_f:
        for root in subs:
            if not os.path.isdir(root):          # guard against missing paths
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

                for fname in filenames:
                    if fname in SKIP_FILES:
                        continue
                    ext = os.path.splitext(fname)[1]
                    if ext in SKIP_EXTS:
                        continue

                    full_path = os.path.join(dirpath, fname)
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as in_f:
                            if ext in PREVIEW_EXTS:
                                # Grab only the first N lines
                                head_lines = ''.join(itertools.islice(in_f, PREVIEW_NUM_LINES))
                                content = head_lines
                                content += '\n... (truncated)\n'
                            else:
                                content = in_f.read()
                    except Exception:
                        continue  # silently ignore unreadable files

                    out_f.write('=' * 80 + '\n')
                    out_f.write(f"FILE: {full_path}\n")
                    out_f.write('-' * 80 + '\n')
                    out_f.write(content + '\n\n')

    print(f"All files combined into: {output_path}")


if __name__ == "__main__":
    base_directory = '/Users/muhammadluay/Desktop/hard repo'
    section        = 'all'      # 'backend', 'frontend', or 'all'
    output_file    = 'combined_output.txt'

    combine_files_to_single_txt(base_directory, section, output_file)
