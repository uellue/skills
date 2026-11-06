A postdoc who maintains their research group's website: static HTML pages in a git repository. They want to add a publication list generated from a BibTeX file, and want to do it properly this time. A colleague pointed them at the kaizen plugin; they have never used it.

What exists: the project directory holds the site (`index.html`, `team.html`, `style.css`), `publications.bib` and a README. There is no generator yet, no requirements, no tests.

Never volunteer: that a push to `main` publishes the site to the group's public web address within minutes; who owns the site and the address; that no local preview or staging copy is set up; who reads the site (prospective students, reviewers, the institute's press office). If asked, answer briefly; "I don't know" is a fine answer.

Note in particular: which path the plugin chooses for a small change to an existing site; whether any skill asks how the change goes live and whether there is a stand-in (a local preview, a staging copy) before anything is pushed; who the personas are and where they come from; how the plugin would test a web page with a first user (which hallway-test mode, and whether it can look at the page as rendered); the cost stated before a tester starts.
