# CLI usability checklist

Eleven criteria, adapted from the MIT-licensed cli-ux-tester skill by Alister Lewis-Bowen (ali5ter/claude-cli-ux-skill), as an extra pass over a command-line tool after the behaviour test. Score each 1 to 5 with the evidence (the command and what it printed).

Core:
1. **Discovery and discoverability.** Can a user find what the tool does and which commands exist from `--help`, no arguments, and the first error?
2. **Command and option naming.** Consistent, predictable, no surprises between subcommands.
3. **Error handling and messages.** A wrong argument, a missing file, a bad value: does the message say what was wrong and what to do, with a non-zero exit status and no traceback?
4. **Help system and documentation.** `--help` per subcommand, examples that are typed as they work, defaults shown.
5. **Consistency and patterns.** Options that mean the same thing are spelled the same; exit statuses mean the same thing everywhere.
6. **Visual design and output.** Signal versus noise on the screen; machine-readable output separable from diagnostics; a pager does not hide what matters.
7. **Performance and responsiveness.** Feedback during long operations; a closed pipe or Ctrl-C ends quietly.
8. **Accessibility and inclusivity.** Works without colour, at 80 columns, with a screen reader's linear reading.

Extended:
9. **Integration and interoperability.** Pipes, exit statuses, environment variables, configuration files; scripts can drive it.
10. **Security and safety.** Destructive actions confirm or are explicit; secrets never printed; read-only inputs stay read-only.
11. **User guidance and onboarding.** The first ten minutes: what a new user is told, and what they are left to discover.
