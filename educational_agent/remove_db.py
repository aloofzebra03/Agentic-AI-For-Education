import os, glob

def rm(p):
    try:
        os.remove(p)
        print("Deleted:", p)
    except FileNotFoundError:
        pass
    except PermissionError:
        print("Permission denied:", p)

# 1) Common filenames
candidates = []
for root in [os.getcwd(), os.path.expanduser("~")]:
    candidates += glob.glob(os.path.join(root, "**", ".lg_memory.db"), recursive=True)

# 2) If you hard-coded a connection string, also derive its absolute path
conn_str = "sqlite:///./.lg_memory.db"
if conn_str.startswith("sqlite:///"):
    rel = conn_str.replace("sqlite:///","")
    candidates.append(os.path.abspath(rel))

# 3) Dedup and delete
seen = set()
for p in candidates:
    p = os.path.normpath(p)
    if p not in seen and os.path.isfile(p):
        seen.add(p)
        rm(p)

if not seen:
    print("No .lg_memory.db files found.")
