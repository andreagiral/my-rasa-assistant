import boto3
from collections import defaultdict
import pandas as pd

# Configure AWS S3
s3 = boto3.client("s3")
bucket_name = "thinktrekai-openstax"
prefix = "openstax_bio2e_chps/"

# Fetch list of files
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Organize files by Unit and Chapter
folder_structure = defaultdict(list)

if "Contents" in response:
    for obj in response["Contents"]:
        key = obj["Key"]
        parts = key.split("/")
        if len(parts) >= 4:
            unit = parts[1]
            chapter = parts[2]
            filename = parts[3]
            folder_structure[(unit, chapter)].append(filename)

# Format as table
rows = []
for (unit, chapter), files in sorted(folder_structure.items()):
    for file in sorted(files):
        rows.append({"Unit": unit, "Chapter": chapter, "File": file})

df = pd.DataFrame(rows)
print(df.to_string(index=False))

# list_s3_files.py
import boto3

bucket = "thinktrekai-openstax"
prefix = "openstax_bio2e_chps/"

s3 = boto3.client("s3")

paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

print("Available files:\n")

for page in pages:
    for obj in page.get("Contents", []):
        print(obj["Key"])
import boto3
import re
from collections import defaultdict
import pandas as pd

# AWS S3 setup
bucket_name = "thinktrekai-openstax"
prefix = "openstax_bio2e_chps/"

# Files we care about
suffixes = [
    "chapter-{num}.html",
    "key-terms.html",
    "summary.html",
    "visual-connection.html",
    "review-questions.html",
    "critical-thinking.html"
]

# Connect to S3
s3 = boto3.client("s3")
paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

# Check presence
chapters = defaultdict(lambda: {sfx: False for sfx in suffixes})

for page in pages:
    for obj in page.get("Contents", []):
        key = obj["Key"]
        match = re.search(r"Chapter (\d{1,2})/", key)
        if match:
            chapter = int(match.group(1))
            for suffix in suffixes:
                if key.endswith(suffix.format(num=chapter)):
                    chapters[chapter][suffix] = True

# Format result
df = pd.DataFrame.from_dict(chapters, orient="index")
df.index.name = "Chapter"
df.columns = [col.replace(".html", "").replace("-", " ").title() for col in df.columns]

# Display
print(df.sort_index())
