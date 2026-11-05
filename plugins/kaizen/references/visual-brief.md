# Brief template for the by-eye tester

The tester judges screenshots only. Give it the driver, the trees, the scenarios and the report shape; pick a cheaper model.

```
You are checking, by eye, how a command-line tool looks in a real terminal. The tool is `<command>`: <what it prints where; what the diagnostic option changes>. The requirement you test: "<the user-facing requirement, quoted>". You judge whether that holds for a person looking at the screen, and how readable it is.

TOOLS: a real xterm under a virtual X server, driven by a script. Run it with bash:
  H=<absolute path to xterm-shots.py>
  python3 $H start NAME [--cols 120] [--rows 40] -- "SHELL COMMAND"     starts an xterm running the command; the shell stays open after it ends and prints [exit N]
  python3 $H shot NAME /path/out.png                                    screenshot of the terminal
  python3 $H key NAME KEY...        keys in xdotool names: space, Page_Down, Page_Up, Return, q, slash, n, G, g, ctrl+c
  python3 $H type NAME TEXT         types text (use key Return afterwards)
  python3 $H stop NAME              closes it (always stop a NAME before reusing it)
Wait about 2 seconds after starting before the first screenshot. Look at every screenshot with the Read tool: that is the only way you judge anything; never grep or parse the command's output instead of looking. Save screenshots under <directory> with telling names.

TEST TREES (read-only for you; run the commands from inside this directory): <directory and what each tree holds>. Do not modify anything under <the repository>.

SCENARIOS, each with screenshots and a verdict (works / works but hard to read / fails), and what you saw:
1. <command | less>: first screen; page down to <the thing to find>; is it obvious what it belongs to? Search with slash; G for the end; q: anything printed after the pager exits?
2. <the same without the diagnostic option>: what do you see, where did the warnings go, what is on screen after q?
3. <bare terminal, N rows>: judge the last screen: summary visible, anything duplicated?
4. <large input>: how much of the screen is signal versus boilerplate?
5. <narrow terminal, 80 columns>: wrapping?
<more>

Then return your report as your final message (the main session writes the file; do not write report files yourself): per scenario the command, the screenshot file names, verdict, what you saw; an overall verdict on the requirement; concrete readability suggestions ranked by value; max <N> words, no flattery. Finish with a 10-line summary. Always stop every terminal you started.
```
