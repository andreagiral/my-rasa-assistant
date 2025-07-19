import os
import re

root_dir = "openstax_bio2e_chps"

# Rename chapter and unit folders to standard format
def clean_folder_names():
    for dirpath, dirnames, _ in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            old_full = os.path.join(dirpath, dirname)

            # Rename Unit folders
            unit_match = re.match(r"Unit\s+(\d{1,2})", dirname)
            if unit_match:
                new_dirname = f"Unit {unit_match.group(1)}"
            # Rename Chapter folders
            elif "Chapter" in dirname:
                chapter_match = re.match(r"Chapter\s+(\d{1,2})", dirname)
                if chapter_match:
                    new_dirname = f"Chapter {chapter_match.group(1)}"
                else:
                    continue
            else:
                continue

            new_full = os.path.join(dirpath, new_dirname)
            if old_full != new_full and not os.path.exists(new_full):
                os.rename(old_full, new_full)
                print(f"📁 Renamed folder: {old_full} ➡️ {new_full}")

# Rename HTML files
def clean_file_names():
    keyword_mapping = {
        "summary": "summary.html",
        "key terms": "key-terms.html",
        "review questions": "review-questions.html",
        "critical thinking": "critical-thinking.html",
        "visual connection": "visual-connection.html",
    }

    section_pattern = re.compile(r"\b(\d{1,2})\.(\d)\b")
    chapter_intro_pattern = re.compile(r"(chapter|ch\.)\s*(\d{1,2})\s*(introduction)", re.IGNORECASE)

    renamed = 0
    skipped = []

    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.lower().endswith(".html"):
                continue

            old_path = os.path.join(foldername, filename)
            lower = filename.lower()

            # Section match (e.g., 10.4)
            section_match = section_pattern.search(lower)
            if section_match:
                new_name = f"{section_match.group(0)}.html"

            # Keyword-based files
            elif any(k in lower for k in keyword_mapping):
                matched_keyword = next((k for k in keyword_mapping if k in lower), None)
                new_name = keyword_mapping[matched_keyword]

            # Chapter intros
            elif chapter_intro_pattern.search(lower):
                chapter_num = chapter_intro_pattern.search(lower).group(2)
                new_name = f"chapter-{chapter_num}.html"

            else:
                skipped.append(filename)
                continue

            new_path = os.path.join(foldername, new_name)
            if os.path.exists(new_path):
                print(f"⚠️ Skipping (already exists): {new_name}")
                continue

            os.rename(old_path, new_path)
            print(f"✅ Renamed file: {filename} ➡️ {new_name}")
            renamed += 1

    print(f"\n✅ Renamed {renamed} files.")
    if skipped:
        print("\n❗ Skipped the following files:")
        for name in skipped:
            print(" -", name)

# Run both folder and file cleaning
if __name__ == "__main__":
    clean_folder_names()
    clean_file_names()
