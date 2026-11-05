A scientist who wrote a small command-line tool for their group: `tally`, which counts log lines per level in instrument log files. It works for them; two colleagues will start using it next week. A colleague pointed them at the kaizen plugin and said: "get a critical first user to try your tool before the others do". They have never used the plugin.

What exists: the project directory holds the tool (`tally.py`), its README and a few sample logs. There are no requirements, no design notes, no tests.

Never volunteer: who the users are and what they need, requirements of any kind, which cases matter most. If asked, answer briefly; "I don't know" is a fine answer.

Note in particular: whether the plugin leads this person to the hallway test, and how; what it does when something is built but no requirements exist (stop, warn, offer the playbook, go ahead); whether it says that a tester without requirements tests its own invention; where the tester's persona comes from when there is no stakeholder record; whether it states the cost before starting a tester; at what point you would hand over to the real tester ("that's what I would have done now").
