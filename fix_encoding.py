import os

files = [".env", ".env.local", ".env.production.local"]

for filename in files:
    if not os.path.exists(filename):
        continue
        
    print(f"Checking {filename}...")
    content = ""
    try:
        # Try reading as UTF-16 (PowerShell default)
        with open(filename, "r", encoding="utf-16") as f:
            content = f.read()
        print(f" - detected UTF-16, converting...")
    except Exception:
        try:
            # Try reading as UTF-8
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            print(f" - detected UTF-8")
        except Exception:
            print(f" - unknown encoding, skipping.")
            continue

    # Write back as clean UTF-8
    if content:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f" - Fixed {filename}")

print("Done fixing encodings.")
