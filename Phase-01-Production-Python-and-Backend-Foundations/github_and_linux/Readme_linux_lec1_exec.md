# Shell & Command-Line Notes: Exercises 3 to 18, plus systemd basics

Revision notes from the lecture 1 exercises. Typos are fixed and the content is regrouped, but the ideas and examples are yours.

Anything marked **Added note** is something I added or corrected while formatting. Everything else comes from your original notes.

## Table of contents

| # | Topic |
|---|---|
| 3 | [Globbing vs brace expansion](#exercise-3-globbing-vs-brace-expansion) |
| 4 | [Metacharacters, history expansion, multi-line commands, quoting](#exercise-4-metacharacters-history-expansion-and-quoting) |
| 5 | [Redirections and file descriptors](#exercise-5-redirections-and-file-descriptors) |
| 6 | [Create a folder only if it doesn't exist; `tee`](#exercise-6-create-a-folder-only-if-it-doesnt-exist) |
| 7 | [Why `cd` is not a standalone program](#exercise-7-why-cd-is-not-a-standalone-program) |
| 8 | [Check whether a file exists](#exercise-8-check-whether-a-file-exists) |
| 9 | [Executable permission](#exercise-9-executable-permission) |
| 10 | [`set -x`](#exercise-10-set--x) |
| 11 | [Reading and writing the same file](#exercise-11-reading-and-writing-the-same-file) |
| 12 | [Keyboard shortcuts, retry loop, special parameters](#exercise-12-keyboard-shortcuts-retry-loop-and-special-parameters) |
| 13 | [Top 5 file extensions with pipes](#exercise-13-top-5-file-extensions-with-pipes) |
| 14 | [`xargs` and file names with spaces](#exercise-14-xargs-and-file-names-with-spaces) |
| 15 | [`curl` + `grep` + `sed`](#exercise-15-curl-grep-and-sed) |
| 16 | [`jq`](#exercise-16-jq) |
| 17 | [`awk`](#exercise-17-awk) |
| 18 | [`sort -k` and top commands from history](#exercise-18-sort--k-and-top-commands-from-history) |
| | [systemd basics](#systemd-basics) |
| | [Quick revision sheet](#quick-revision-sheet) |

---

## Exercise 3: Globbing vs brace expansion

| Pattern | What it does | Example |
|---|---|---|
| `[110]` (character class) | Matches **one character** from the set (here `1` or `0`) | `ls file[110].txt` looks for `file1.txt` and `file0.txt` |
| `{1,10}` (brace expansion) | The shell **rewrites** it into separate words | `ls file{1,10}.txt` becomes `ls file1.txt file10.txt` |

A character class cannot match `file10.txt`, because `[...]` always matches a single character. To match both `file1.txt` and `file10.txt`, use brace expansion.

> **Added note:** Brace expansion happens before the command runs and does not check the filesystem, so it expands even if the files don't exist. A glob like `[110]` only matches files that actually exist.

---

## Exercise 4: Metacharacters, history expansion and quoting

### Metacharacters

Characters with a special meaning to the shell.

| Char | Meaning |
|---|---|
| `<` | Pass input to a program from a file |
| `>` | Redirect a program's output |
| `&` | Run a command in the background and print its job/process id |
| `&&` | Run the next command **only if the previous succeeded** |
| `\|\|` | Run the next command **only if the previous failed** |
| `\|` | Pass the output of one command to the input of the next |
| `;` | Separate commands; they run one by one regardless of the previous result |
| `$` | Variable expansion and command substitution |
| `()` | Also used for command substitution |
| `{}` | Parameter expansion |
| `\` | Escape a special character |
| space, tab, newline | Also metacharacters |

### Background jobs (`&`)

```bash
sleep 5 &
[1] 6118
```

How do I see the output of a background command? Redirect it to a file when you start it:

```bash
ls -l > out.txt &
```

`jobs` is a shell built-in that shows the status of background jobs. `jobs -l` also shows process ids.

### History expansion

`history` is a shell built-in that lists previously run commands, numbered.

| Syntax | Meaning |
|---|---|
| `!!` | Run the previous command again |
| `!n` | Run command number `n` (if history shows `1046  echo hello &`, then `!1046` runs it again) |
| `!string` | Run the most recent command that **begins with** `string` (after `ls`, `cat names.txt`, `ls -l`, running `!cat` repeats `cat names.txt`) |
| `!$` | The **last argument** of the previous command |
| `!*` | **All arguments** of the previous command |

Example:

```text
$ cat file\[.txt
$ echo !*
echo file\[.txt
file[.txt
$ echo !$
echo file\[.txt
file[.txt
$ cat file\[.txt ../jk/hello.txt
$ echo !*
echo file\[.txt ../jk/hello.txt
file[.txt ../jk/hello.txt
```

### Multi-line commands

- End a line with `\` and press Enter to continue the same command on the next line.
- End a line with `&&` and press Enter to continue with the next command.

```text
$ echo hello &&
> echo jayesh
hello
jayesh

$ echo hello \
> echo jayesh
hello echo jayesh
```

Notice that in the second example `\` only joins the lines, so `echo jayesh` becomes arguments to the first `echo`.

### Quoting

#### Single quotes

No interpretation by the shell. The text is passed to the program exactly as written.

#### Double quotes

Most characters are passed as they are, but the shell still interprets a few:

| Char | What the shell does inside `"..."` |
|---|---|
| `$` | Variable expansion (`$var`, `${var}`, `$(...)`, `$*`, `$@`, `$?`) |
| `` ` `` | Command substitution (`$(...)` is preferred) |
| `!` | History expansion |
| `\` | Escapes only `$`, `` ` ``, `"`, `\` and newline |
| `*` and `@` | **Not globs.** They only matter after `$`, as `$*` and `$@` |

**When is `$` special?** Only if it is followed by a letter, digit, or a special character such as `(`, `{`, `*`, `@`, `?`. Followed by anything else, it is a literal `$`.

```text
$ echo "$`echo hello`"      # $ followed by a backtick is not valid, so it stays literal
$hello
$ echo "`echo hello`"
hello
$ echo "$hello"             # $hello is an unset variable, so it expands to nothing

```

**`"$@"` vs `"$*"`**: run `./names.sh Jayesh Krishna`:

```bash
#! /usr/bin/bash

for everyMember in "$@"; do
        echo hello $everyMember;
done;
```

| Form | Output |
|---|---|
| `"$@"` | `hello Jayesh` then `hello Krishna` (each argument kept separate) |
| `"$*"` | `hello Jayesh Krishna` (all arguments joined into one string) |

**Backslash inside double quotes**

`\` escapes only `$`, `` ` ``, `"`, `\` and newline. Before any other character, the backslash stays as a literal `\`.

```text
$ echo "\n"
\n
$ echo "\$"
$
$ echo "\\"
\
```

A backslash followed by a newline is **line continuation**: the shell removes both and carries on as if it were one line. This works inside double quotes too:

```text
$ echo "hello \
> world"
hello world
$ echo hello \
> world
hello world
```

#### ANSI-C quoting: `$'...'`

`$'string'` interprets escape sequences. It does not work inside double quotes, and note it is plain single quotes after `$`, not backticks.

| Sequence | Meaning |
|---|---|
| `$'\n'` | New line |
| `$'\a'` | Alert (bell) |
| `$'\b'` | Backspace |

```text
$ income=70,000
$ echo "My income is \$$icnome. I'm Poor"$'\n'"I'm a software engineer"
My income is $. I'm Poor
I'm a software engineer
```

> **Added note:** The `$icnome` typo in this example is why no amount appeared: an unset variable expands to nothing. With `$income` the output would be `My income is $70,000.` The line is built from three pieces glued together: a double-quoted part, the `$'\n'` part, and another double-quoted part.

---

## Exercise 5: Redirections and file descriptors

By default, input comes from the terminal and output goes to the terminal.

| Operator | Meaning |
|---|---|
| `>` | Redirect output; **overwrites** the file (existing content is deleted first) |
| `>>` | Redirect output; **appends** without deleting existing content |
| `<` | Take input from a file instead of the terminal |

### File descriptors

A non-negative number each process uses to identify its input, output and error channels.

| FD | Channel |
|---|---|
| `0` | input (stdin) |
| `1` | output (stdout) |
| `2` | error (stderr) |

`ls ./ > out.txt` is the same as `ls ./ 1> out.txt`.

| Operator | Meaning |
|---|---|
| `1>` / `1>>` | Redirect output (overwrite / append) |
| `2>` / `2>>` | Redirect errors (overwrite / append) |
| `&>` / `&>>` | Redirect both output and errors |
| `2>&1` | Send errors to wherever output currently goes |
| `1>&2` | Send output to wherever errors currently go |

```bash
ls /tmp /nonexistent > log.txt 2>&1
```

Output goes to `log.txt`, then errors are told to follow the same place as output.

You **cannot** write `2>>&1` or `1>>&2`. Whether it overwrites or appends is decided by how the target was opened, not by a second `>>`.

### Order matters: `2>&1` copies, it does not bind permanently

```text
$ ls /nonexistent /tmp > out.txt 2>&1 > /dev/tty
/tmp:
snap-private-tmp
systemd-private-...-chrony.service-LBbw2Q
...
```

Step by step, left to right:

1. Output goes to `out.txt`.
2. `2>&1`: errors now point to where output points, which is `out.txt`.
3. `> /dev/tty`: output moves back to the terminal.

Errors are **not** moved back; `2>&1` only copied the destination at that moment. Result: the `/tmp` listing shows on the terminal, and the error message is in `out.txt`.

### Special paths

| Path | Meaning |
|---|---|
| `/dev/null` | Discard everything written to it (works for output and errors) |
| `/dev/stdout`, `/dev/stderr` | Wherever stdout / stderr currently point |
| `/dev/stdin` | Read input from stdin (the terminal by default) |

```bash
ls /nonexistent /tmp &> /dev/stdout     # both streams go where stdout goes (the terminal by default)
cat < /dev/stdin                        # cat echoes what you type; Ctrl+D to stop
```

`cat` normally reads files given as arguments. With no file it reads its own stdin, so the terminal waits for you to type.

---

## Exercise 6: Create a folder only if it doesn't exist

Several ways, from best to worst.

**Using a test:**

```bash
[ -d check/ ] || mkdir check/
```

If the test fails (the folder doesn't exist), run `mkdir`.

**Best way**: use the exit status of `mkdir`:

```bash
mkdir check 2> /dev/null && echo "Folder created" || echo "Folder exists"
```

If `mkdir` succeeds, the `&&` part runs and the `||` part is skipped. If `mkdir` fails, the `&&` part is skipped, and `||` runs because `mkdir` was the last command and it failed.

**Using `$?`** (exit status of the last command):

```bash
mkdir check 2> /dev/null; if [ $? = 0 ]; then echo "Folder created"; else echo "Folder exists"; fi
```

**Worst way**:

```bash
find ./ -type d | grep -oE "check" > out.txt; if [ "$(cat < out.txt)" = "check" ]; then echo "File already exists"; else mkdir check; echo "File created"; fi
```

> **Added note:** `A && B || C` is not a true if/else. If `A` succeeds but `B` fails, `C` also runs. Here it's fine because `echo` almost never fails. Also, `mkdir -p check` creates the folder and quietly succeeds if it already exists.

### `tee`: capture output in the middle of a pipe

`tee` copies what it receives to the terminal, and also to a file if you give one.

```text
$ files=$(ls) && echo $files | tee
a.txt app.txt apple.txt ... out.txt
$ files=$(ls) && echo $files | tee out.txt
a.txt app.txt apple.txt ... out.txt
```

The second one prints to the terminal and also saves to `out.txt`.

---

## Exercise 7: Why `cd` is not a standalone program

`cd` is a shell built-in because **a child process cannot change the working directory of its parent**.

Suppose you are in `/home/jayesh` and run `cd /tmp`, and suppose `cd` were a standalone program:

1. The shell starts a child process to run it.
2. The child changes **its own** working directory to `/tmp`.
3. The child exits.
4. Control returns to your shell, which is **still in `/home/jayesh`**.

The child only changed its own directory, not its parent's.

**`$(cd /)`**: command substitution starts a child (a subshell) and runs the command inside it. The `cd` changes the subshell's directory, and because `cd` prints nothing, the parent substitutes nothing. The subshell ends, and your directory stays the same.

---

## Exercise 8: Check whether a file exists

```bash
#! /usr/bin/bash

if [ -f $1 ]; then
        echo "file exists";
else
        echo "file doesn't exists";
fi
```

> **Added note:** Quote the argument as `[ -f "$1" ]`. Unquoted, a file name with spaces splits into several words and breaks the test, and an empty `$1` makes the test behave unexpectedly.

---

## Exercise 9: Executable permission

- This was already covered in the user management section.
- By default the executable permission is off for all three (user, group, others).
- `chmod u=+x` **removes** read and write for the current user and leaves only execute (`=` sets exactly what follows).
- The owner can still edit the file, because the owner can change permissions again. So it is better to use `chmod u=rwx`.

---

## Exercise 10: `set -x`

Prints each command (prefixed with `+`) before running it. You often see it in Jenkins pipelines.

```text
$ ./isFileExists.sh a.txt
+ '[' -f a.txt ']'
+ echo 'file exists'
file exists
```

Enable it inside the script:

```bash
#! /usr/bin/bash

set -x

if [ -f $1 ]; then
        echo "file exists";
else
        echo "file doesn't exists";
fi
```

---

## Exercise 11: Reading and writing the same file

**Copy or date-stamp a file:**

```bash
cat out.txt > out_$(date +%Y-%m-%d).txt
cp out.txt out1.txt
```

**Avoid `cat out.txt > out.txt`.** The shell empties `out.txt` before `cat` even starts, so `cat` reads an empty file and the file stays empty.

**What about `cat file1.txt >> file1.txt`?**

It could run forever or fail, so avoid it:

1. `>>` opens the file in append mode and does not truncate it.
2. `cat` starts reading from the file.
3. As `cat` writes the contents back into the same file, the file grows.
4. `cat` may keep reading the newly appended data, so the file grows until you interrupt it or the disk is full.

To prevent this, you get:

```text
cat: out.txt: input file is output file
```

> **Added note:** That error comes from GNU `cat` itself, not the shell. It detects that the input and output are the same file and refuses.

---

## Exercise 12: Keyboard shortcuts, retry loop and special parameters

### Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + A` | Move to the beginning of the command |
| `Ctrl + E` | Move to the end of the command |
| `Ctrl + W` | Delete the word before the cursor |
| `Alt + D` | Delete the word after the cursor |
| `Ctrl + U` | Delete everything before the cursor |
| `Ctrl + K` | Delete everything after the cursor |

### The retry loop

Task: run a program repeatedly until it fails, and show the failing run's log.

`exec_12.sh`:

```bash
#! /usr/bin/bash

logfile=logs_$(date +%s).txt
run=1
echo "Log is going to be stored in $logfile"
echo $run
while $1 $2 $run > $logfile 2>&1; do
        echo "Test passed"
        run=$((run+1))
        echo $run
done

echo "Test Failed"
echo "Failed log:"$'\n'
cat $logfile
```

`hello.py`:

```python
import sys

print(sys.argv)
if sys.argv[1] == "10":
    raise ValueError("'run' env variable should not reach the value 10")

print("Test passed")
```

Run (output shortened):

```text
$ ./exec_12.sh python3 hello.py $run
Log is going to be stored in logs_1792567046.txt
1
Test passed
2
Test passed
...
10
Test Failed
Failed log:

['hello.py', '10']
Traceback (most recent call last):
  File "/home/jayesh/lec1_exercises/hello.py", line 5, in <module>
    raise ValueError("'run' env variable should not reach the value 10")
ValueError: 'run' env variable should not reach the value 10
```

How it works:

- `while command; do ...; done` loops as long as the command's exit status is 0.
- `> $logfile 2>&1` sends both output and errors to the log file, overwriting it each run, so at the end it holds only the failing run's log.
- `$((run+1))` is arithmetic expansion.
- `date +%s` (seconds since 1970) gives a unique log file name.

### Special parameters

Characters after `$` that have their own meaning.

| Parameter | Expands to |
|---|---|
| `$0` | Name of the shell or script being run |
| `$$` | Process id of the shell running the commands |
| `$!` | Process id of the most recent background job |
| `$#` | Number of positional parameters passed (useful to check the user passed all needed arguments) |
| `$@`, `$*`, `$?` | Seen earlier (all args separately / all args as one string / last exit status) |

```text
$ /usr/bin/sh
$ echo $0
/usr/bin/sh
$ exit
$ echo $0
-bash
```

> **Added note (correction):** Your original note said `$$` inside a subshell returns the subshell's pid. In bash, `$$` keeps returning the pid of the **main shell**, even inside a subshell. Use `$BASHPID` to get the subshell's own pid.

---

## Exercise 13: Top 5 file extensions with pipes

**Task:** use pipes to find the 5 most common file extensions in your home directory.

Files in the current folder:

```text
 1                 dummy.cpp   'file[.txt'         logs.txt              logs_1792567018.txt   names.sh
 a.txt             error.txt    file].txt          logs_1792566566.txt   logs_1792567046.txt   names.txt
 app.txt           exec_12.sh   file_creation.sh   logs_1792566605.txt   logs_1792567327.txt   out.txt
 apple.txt         file1.txt    hello.py           logs_1792566664.txt   logs_1792567375.txt   out_2026-10-20.txt
 application.txt   file10.txt   hello.sh           logs_1792566869.txt   name.md
 check             file2.txt    isFileExists.sh    logs_1792566908.txt   names.cpp
```

### My first attempt

```bash
find . -type f | cut -d . -f 3 | sort | uniq -c | tail -n 3
```

```text
      1 py
      5 sh
     23 txt
```

Without `tail -n 3` the output is:

```text
      1
      2 cpp
      1 md
      1 py
      5 sh
     23 txt
```

Issues found:

- `cpp` has 2 files but is missing from the final output. `sort` orders by **extension name**, not by count, so `tail -n 3` just takes the last three alphabetically.
- To rank by count you need `sort -rn` on the count column.
- `cut -d . -f 3` is unreliable. It breaks if a file name contains extra dots. Also, `find .` lists hidden files too (only plain `ls` hides them).

### Working solutions

Version 1 (from ChatGPT):

```bash
find . -type f | grep -E '\.[^.]+$' | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -n 3
```

Version 2 (my simplified version):

```bash
find . -type f | grep -oE "[^.]+$" | sort | uniq -c | sort -rn | head -n 5
```

```text
     23 txt
      5 sh
      2 cpp
```

### Why `grep -E '\.[^.]+$'`?

- `\.` matches a literal dot.
- `[^.]+$` matches one or more characters that are **not** a dot, up to the end of the line.
- Together they match the extension including the dot (`.txt`, `.cpp`, `.sh`).

In this exercise it makes no difference to the final output, so I replaced it with `grep -oE "[^.]+$"`, which prints only the part after the last dot.

### Why `sed 's/.*\.//'`?

`s/regex/replacement/` replaces the match; with an empty replacement it **deletes** the match.

For `/lec/jayesh/a.txt`:

- `.*` first matches the whole string `/lec/jayesh/a.txt`.
- Then `\.` has nothing left to match, so the regex **backtracks** one character at a time until a `.` can be matched.
- Final split: `.*` = `/lec/jayesh/a`, `\.` = `.`.
- `sed` deletes `/lec/jayesh/a.`, leaving only `txt`.

> **Added note:** Both versions have an edge case for files **without** an extension (for example `./Makefile`). They would be counted under a strange key like `/Makefile`, because there is no dot after the leading `./`. If that matters, filter those out first, for example with `grep -E '\.[^./]+$'`.

---

## Exercise 14: `xargs` and file names with spaces

**Task:** get the `.sh` files in a directory and print the number of lines in each. File names may contain spaces.

### `xargs`

- A program that takes items from standard input and passes them as **arguments** to another command.
- By default the delimiters are space, newline and tab.

The `.sh` files:

```text
./isFileExists.sh
./hello.sh
./exec_12.sh
./file_creation.sh
./na a.sh
./names.sh
```

### The problem

```text
$ find . -type f -name "*.sh" | xargs wc -l
  9 ./isFileExists.sh
  0 ./hello.sh
 17 ./exec_12.sh
 10 ./file_creation.sh
wc: ./na: No such file or directory
wc: a.sh: No such file or directory
  5 ./names.sh
 41 total
```

Space is a default delimiter, so `./na a.sh` was split into `./na` and `a.sh`.

### Fix 1: `-d` (set the delimiter yourself)

```text
$ find . -type f -name "*.sh" | xargs -d $'\n' wc -l
  9 ./isFileExists.sh
  0 ./hello.sh
 17 ./exec_12.sh
 10 ./file_creation.sh
  0 ./na a.sh
  5 ./names.sh
 41 total
```

### Fix 2: `-0` with `find -print0` (the most robust)

```text
$ find . -type f -name "*.sh" -print0 | xargs -0 wc -l
```

`-print0` makes `find` end each path with a null character (`\0`) instead of a newline, and `-0` tells `xargs` to split on null. A file name can never contain `\0`, so this is safe for any name.

```text
$ find . -type f -name "*.sh" -print0
./isFileExists.sh./hello.sh./exec_12.sh./file_creation.sh./na a.sh./names.sh
```

(The nulls are invisible, so the names look glued together.)

### Useful `xargs` options

| Option | Meaning |
|---|---|
| `-0` | Use the null character as the delimiter |
| `-d` | Use a custom delimiter |
| `-n N` | Pass at most `N` arguments per run. Instead of one run with everything, it runs the command in batches |
| `-t` | Print each command before running it (helps tracing) |
| `-r` | Don't run the command if there is no input (by default it runs once even with no input) |
| `-I {}` | Replace the placeholder `{}` with each input item |

Example for `-n 1 -t`:

```text
$ find . -type f -name "*.sh" -print0 | xargs -0 -n 1 -t wc -l
wc -l ./isFileExists.sh
9 ./isFileExists.sh
wc -l ./hello.sh
0 ./hello.sh
wc -l ./exec_12.sh
17 ./exec_12.sh
wc -l ./file_creation.sh
10 ./file_creation.sh
wc -l './na a.sh'
0 ./na a.sh
wc -l ./names.sh
5 ./names.sh
```

Example for `-I {}`: make a backup of every `.txt` file in the current directory.

```bash
find . -type f -name "*.txt" -print0 |
xargs -0 -I {} cp "{}" "{}.bak"
```

---

## Exercise 15: `curl`, `grep` and `sed`

`curl` is a program that sends or receives data from a server using a URL.

**Task:** get the list of lecture titles from `https://missing.csail.mit.edu/`. The unique pattern is `href="/2026/`, which appears only on the course links.

```bash
curl https://missing.csail.mit.edu/ | grep -oE "^.*<a href=\"/2026/.*\">.+</a>$" | sed "s/.*<a href=\"[^>]*//" | sed "s/>//" | sed 's/<\/a>//'
```

Output:

```text
Course Overview + Introduction to the Shell
Command-line Environment
Development Environment and Tools
Debugging and Profiling
Version Control and Git
Packaging and Shipping Code
Agentic Coding
Beyond the Code
Code Quality
```

Pipe it into `wc -l` to count the lectures.

**Shorter version (from ChatGPT)**: it doesn't print the titles, only counts them:

```bash
curl -s https://missing.csail.mit.edu/ | grep -oE 'href="/2026/[^"]+"' | wc -l
```

### `curl -s`

Silent mode. Without it `curl` prints a progress table (`% Total % Received ...`) that you usually don't want when piping.

### Why does `curl ... | head -n 5` show an error?

```text
$ curl https://missing.csail.mit.edu/ | head -n 5
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
...
<!DOCTYPE html>
<html lang="en">

  <head>
  <meta charset="utf-8">

curl: (23) Failure writing output to destination, passed 1246 returned 725
```

The pipe delivers `curl`'s output to `head` as it arrives. `head` reads the first 5 lines and **exits immediately**. `curl` is still sending data, but nobody is reading the pipe any more, so its write fails and it reports error 23.

---

## Exercise 16: `jq`

`jq` is a program for parsing JSON.

- `jq .` (or just `jq`) pretty-prints JSON with indentation and colors.
- `.` is a **filter** meaning "the current input".

Sample data used below:

```json
[{"name": "Jayesh", "place": "Coimbatore", "age": 24}, {"name": "Kannan", "place": "Bhavani", "age": 52}]
```

| Filter | Result | Python equivalent |
|---|---|---|
| `'.'` | The whole array, pretty-printed | `print(people)` |
| `'.[]'` | Each object in the array, one by one | `for p in people: print(p)` |
| `'.[] \| .name'` | Only the `name` of each object (`"Jayesh"`, `"Kannan"`) | `for p in people: print(p["name"])` |

The pipe `|` passes each output of the left filter into the right filter.

### `select`

`select(condition)` passes data through only if the condition is true.

```bash
echo '[{"name" : "Jayesh", "place": "Coimbatore", "age" : 24}, {"name" : "Kannan", "place" : "Bhavani", "age" : 52}]' | jq '.[] | select(.age > 50)'
```

```json
{
  "name": "Kannan",
  "place": "Bhavani",
  "age": 52
}
```

Use `>`, `<`, `==`. **Do not use a single `=`** inside `select`: in `jq` it is **assignment**, which succeeds and returns a (truthy) object, so every item passes through.

### Mistakes I made

| Wrong | Why it's wrong |
|---|---|
| `select("age" > 50)` | A key must be referenced with a leading dot: `.age` |
| `select(.name = "Jayesh")` | `=` assigns, so it is always true and every item passes; use `==` |
| `select(.name = Jayesh)` | Strings need quotes (`"Jayesh"`), numbers don't |

### Modifying data

```bash
... | jq '.[] | select(.age > 50) | .name = "Jayesh"'
```

```json
{
  "name": "Jayesh",
  "place": "Bhavani",
  "age": 52
}
```

It filters by age, then changes the `name` field.

### The exercise command

```bash
curl -s https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json | jq '.[] | select(.version > 6) | .name'
```

---

## Exercise 17: `awk`

### Syntax

```text
awk 'CONDITION {ACTION}'
```

The condition can use `>`, `<`, `==`, and `~` (regex match).

How it works:

- `awk` reads input **one line (record) at a time** and splits it into **fields** using the field separator.
- For the line `a 50 x`: `$0` = `a 50 x`, `$1` = `a`, `$2` = `50`, `$3` = `x`.
- It tests the condition. If true, it runs the action on that line; if not, the action is skipped.

```bash
printf 'a 50 x\nb 150 y\nc 200 z\n' | awk -F " " '$2 ~ /[0-9]+/ {$1 = "Jayesh"; print $0}'
```

### What can an action do?

- Change field values
- Print
- Use conditions and loops
- Do calculations
- Print fields in a different order

```text
$ printf 'a 50 x\nb 150 y\nc 200 z\n' | awk -F " " '{if ($2 ~ /[0-9]+/) { $2 = $2 + 50; print $2 $1 $3}}'
100ax
200by
250cz
```

### `FS` and `OFS`

- `FS`: input field separator. `awk -F " "` sets it.
- `OFS`: output field separator. By default it is the same as `FS`.
- Both are ordinary awk variables.
- With `print a b`, the values are glued together with **no** separator. With `print a, b`, the comma is replaced by `OFS`.

```text
$ printf 'a 50 x\nb 150 y\nc 200 z\n' | awk -F " " '{if ($2 ~ /[0-9]+/) { $2 = $2 + 50; print $2"Hi"$1,$3}}'
100Hia x
200Hib y
250Hic z
```

Here `$1` and `$3` are separated by `OFS` (because of the comma), but `"Hi"` and `$1` are glued together (no comma).

### Setting variables with `BEGIN`

`BEGIN { ... }` runs **before** any lines are read.

```bash
printf 'a 50 x\nb 150 y\nc 200 z\n' | awk -F " " 'BEGIN {FS=","} $2 ~ /[0-9]+/ {print}'
```

`-F " "` sets `FS` first, then `BEGIN` overrides it to `,`, so while processing lines `FS` is `,`. Use `BEGIN {OFS=","}` the same way for the output separator. Don't forget the quotes around the value.

### The exercise command

```bash
printf 'a 50 x\nb 150 y\nc 200 z\n' | awk 'BEGIN {FS=" "; OFS=","} $2 > 100 {print $3,$2,$1}'
```

```text
y,150,b
z,200,c
```

---

## Exercise 18: `sort -k` and top commands from history

### Top 10 commands I use

```text
$ cat /root/.bash_history | awk -F " " '{print $1}' | sort | uniq -c | sort -rn | head -n 10
    266 echo
    204 find
    143 curl
    100 ls
     89 cat
     74 cd
     69 printf
     68 man
     64 grep
     56 if
```

Pipeline: take the first word of each history line, sort so identical words are adjacent, count them with `uniq -c`, sort by count descending, and keep the top 10.

### Understanding `sort -k`

`-k` tells `sort` which field of each line to use as the sorting key.

- The default field separator is blank space.
- For `Ka 1 nnan`: field 1 = `Ka`, field 2 = `1`, field 3 = `nnan`.
- `-k2,2`: the key **starts at field 2 and ends at field 2**. For `Ka 1 nnan` the key is `1`.
- `-k2`: the key starts at field 2 and runs **to the end of the line**. For `Ka 1 nnan` the key is `1 nnan`.
- The default is lexicographic (text) sorting. `-n` makes it numeric.

> **Added note:** By default, leading blanks are part of a field (they are not ignored). Use `-b` to ignore leading blanks when picking the key.

`names.txt`:

```text
2 Jayesh\0Jayesh
Ka 1 nnan
Sub 11 a
Kannan
22JK
```

Results:

```text
$ cat names.txt | sort -nk2,2
2 Jayesh\0Jayesh
22JK
Kannan
Ka 1 nnan
Sub 11 a

$ cat names.txt | sort -k2,2
22JK
Kannan
Ka 1 nnan
Sub 11 a
2 Jayesh\0Jayesh

$ cat names.txt | sort -k2
22JK
Kannan
Ka 1 nnan
Sub 11 a
2 Jayesh\0Jayesh

$ cat names.txt | sort -s -k2
Kannan
22JK
Ka 1 nnan
Sub 11 a
2 Jayesh\0Jayesh
```

### Why `sort -nk2,2` gives that order

| Line | Key (field 2) | Numeric value |
|---|---|---|
| `2 Jayesh\0Jayesh` | `Jayesh\0Jayesh` | 0 (doesn't start with a number) |
| `Ka 1 nnan` | `1` | 1 |
| `Sub 11 a` | `11` | 11 |
| `Kannan` | empty | 0 (field doesn't exist) |
| `22JK` | empty | 0 (field doesn't exist) |
| `Latha 0` | `0` | 0 (This zero has more priority than the record's which has no numeric value and are considered as zero)

The three lines with value 0 come first. They tie, so `sort` falls back to comparing the **entire line** lexicographically, which gives `2 Jayesh\0Jayesh`, `22JK`, `Kannan`.

With **`-s`** (stable), `sort` skips that last-resort comparison and keeps tied lines in their **original input order**. That's why `Kannan` comes before `22JK` in the `-s` output.

---

## systemd basics

### Init system

- The first program started by the Linux kernel; it gets **PID 1**.
- Its job is to start the other programs the system needs.
- Every other process is a child of PID 1.

What an init system does:

- Starts services in the right order
- Stops them cleanly at shutdown
- Collects logs (systemd does this through its `systemd-journald` service)

Common init systems:

| Init system | Where |
|---|---|
| `systemd` | Modern Linux systems |
| SysV init | Old Linux systems |

Check which one you have:

```bash
ps -p 1 -o comm=
```

- `-p` selects the pid.
- `-o` chooses what to display.

| `-o` field | Shows |
|---|---|
| `comm` | Process name only |
| `args` / `cmd` / `command` | Full command line (for `python3 app.py`: `comm` shows `python3`, `args` shows `python3 app.py`) |
| `pid` | The pid |

The trailing `=` removes the column header.

### What is systemd?

- The most commonly used init system on Linux distributions.
- The `d` stands for **daemon**, a background process (more on this in the full guide).

What it does:

- **Manages units.**
- **Handles dependencies.** A unit can say it needs other units started first, and systemd starts them. Independent units start in parallel, which makes boot faster.
- **Supervises processes.** It can restart them on crash and limit their CPU and memory.
- **Stores all service logs** (the journal), via `systemd-journald`.
- **Schedules jobs**, using timer units.

### What is a unit?

- Anything systemd manages.
- Each unit has a **unit file** that says what it is and what to do with it.
- There are several types: service, target, timer, and others.

Analogy: a restaurant manager's cards.

| Card | Meaning |
|---|---|
| "Kitchen stove: turn on at 9am, turn off at 11pm" | A thing to run (service) |
| "Cleaning: do it every night at 10pm" | A scheduled job (timer) |
| "Opening routine: needs stove, lights and music all ready" | A group of things (target) |

Each card is a unit file. The manager (systemd) reads the cards and does what they say.

### What is a service?

A program that keeps running in the background, so you don't have to manage it yourself.

**How is it different from a normal program?**

When you run `python hello.py` in a terminal:

- It runs in the terminal; its stdin, stdout and stderr are tied to it.
- If you close the terminal, the program dies.
- If it crashes, you must restart it yourself.
- If the computer reboots, it is gone until you start it again.

A service fixes all of these. The same program becomes a service once systemd handles it through a unit file.

### What is a target?

- A bundle (group) of units.
- A simple unit with no type-specific section.
- A service becomes part of a target through its `[Install]` section, which usually has `WantedBy=multi-user.target`.
- `multi-user.target` is run by systemd during boot. When it is reached, systemd collects the units that belong to it and starts them. This is how a service starts automatically after boot.

### What is a timer?

- It decides **when** to run a unit. It doesn't run a program itself.
- It is systemd's version of cron.

### Structure of a unit file

- A text file in **INI format**, a common configuration format.
- Split into `[Sections]` containing `key=value` pairs.
- Both section names and keys are **case sensitive** (for example `WantedBy`, not `wantedby`).

See the full systemd guide (`systemd.md`) for details on each unit type, and your symlink notes for how `enable` uses symlinks.

---

## Quick revision sheet

### Shell basics

| Need | Use |
|---|---|
| Run in background | `cmd &`, view with `jobs -l` |
| Run next only on success / failure | `&&` / `\|\|` |
| Run regardless | `;` |
| Repeat last command / last arg / all args | `!!` / `!$` / `!*` |
| Literal text, no interpretation | single quotes `'...'` |
| Expand variables but keep spaces | double quotes `"..."` |
| Newline and escapes | `$'...\n...'` |
| Each argument separately / joined | `"$@"` / `"$*"` |

### Redirections

| Need | Use |
|---|---|
| Overwrite / append output | `>` / `>>` |
| Errors only | `2>` |
| Both output and errors | `&>` or `> file 2>&1` |
| Discard | `> /dev/null` |
| Show and save | `cmd \| tee file` |
| Order rule | Redirections are processed **left to right** |

### Special parameters

`$0` script name, `$$` shell pid, `$!` last background pid, `$#` argument count, `$?` last exit status, `$@` / `$*` all arguments.

### Text-processing pipeline patterns

```bash
# count and rank
... | sort | uniq -c | sort -rn | head -n N

# safe handling of file names with spaces
find . -type f -name "*.sh" -print0 | xargs -0 wc -l

# first word of each history line, ranked
awk '{print $1}' ~/.bash_history | sort | uniq -c | sort -rn | head

# JSON filtering
jq '.[] | select(.version > 6) | .name'

# awk with separators
awk 'BEGIN {FS=" "; OFS=","} $2 > 100 {print $3,$2,$1}'
```

### Common mistakes

- `cat f > f` empties the file; `cat f >> f` fails or grows forever.
- `cd` can't be an external program; a child can't change its parent's directory.
- Unquoted `$1` or `$var` breaks on spaces; quote it.
- `2>&1` copies the destination at that moment; put it **after** the `>` it should follow.
- `xargs` splits on spaces by default; use `-print0 | xargs -0`.
- In `jq`, `=` assigns and `==` compares.
- `sort` without `-n` sorts text; `uniq` only collapses **adjacent** duplicates, so sort first.
- `A && B || C` is not a true if/else.
