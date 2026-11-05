#!/usr/bin/env python3
"""notes: keep short notes in a JSON file.

    notes add TEXT        add a note
    notes list            list notes, newest first
    notes rm ID           delete a note
Notes live in ~/.notes.json (override with NOTES_FILE).
"""
import json, os, sys, time
PATH = os.environ.get("NOTES_FILE", os.path.expanduser("~/.notes.json"))
def load():
    try:
        return json.load(open(PATH))
    except FileNotFoundError:
        return []
def save(notes):
    json.dump(notes, open(PATH, "w"), indent=1)
def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return 0
    cmd, args = argv[0], argv[1:]
    notes = load()
    if cmd == "add":
        nid = max([n["id"] for n in notes], default=0) + 1
        notes.append({"id": nid, "text": " ".join(args), "ts": time.time()}); save(notes); print(nid)
    elif cmd == "list":
        for n in sorted(notes, key=lambda n: -n["ts"]):
            print(f"{n['id']:4d}  {time.strftime('%Y-%m-%d', time.localtime(n['ts']))}  {n['text']}")
    elif cmd == "rm":
        notes = [n for n in notes if str(n["id"]) != args[0]]; save(notes)
    else:
        print(f"unknown command {cmd}", file=sys.stderr); return 2
    return 0
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
