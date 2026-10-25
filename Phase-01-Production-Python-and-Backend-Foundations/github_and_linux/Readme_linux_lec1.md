# Lecture 1: Introduction to the Shell

Revision notes, reorganised from the original lecture notes. Typos are fixed and the content is regrouped by topic, but the ideas and examples are yours.

Anything marked **Added note** or **Correction** is something I added or fixed while formatting. Everything else comes from your original notes.

## Table of contents

1. [Terminal, interface, shell](#1-terminal-interface-shell)
2. [Reading the prompt](#2-reading-the-prompt)
3. [Escape characters](#3-escape-characters)
4. [Getting help: `man`](#4-getting-help-man)
5. [Where programs live: `PATH` and `which`](#5-where-programs-live-path-and-which)
6. [Navigating: `cd`, absolute and relative paths](#6-navigating-cd-absolute-and-relative-paths)
7. [Working with files](#7-working-with-files)
8. [Searching file contents: `grep`](#8-searching-file-contents-grep)
9. [Editing file contents: `sed`](#9-editing-file-contents-sed)
10. [Globs](#10-globs)
11. [Finding files: `find`](#11-finding-files-find)
12. [Commands, options and arguments](#12-commands-options-and-arguments)
13. [Parsing with `awk`](#13-parsing-with-awk)
14. [Single vs double quotes](#14-single-vs-double-quotes)
15. [Redirection and pipes](#15-redirection-and-pipes)
16. [Command substitution](#16-command-substitution)
17. [Arithmetic expansion](#17-arithmetic-expansion)
18. [Conditions](#18-conditions)
19. [Loops](#19-loops)
20. [Exit status](#20-exit-status)
21. [Bash scripts](#21-bash-scripts)
22. [Arrays and `${}`](#22-arrays-and-)
23. [User management](#23-user-management)
24. [`cut`](#24-cut)
25. [Quick revision sheet](#25-quick-revision-sheet)

---

## 1. Terminal, interface, shell

| Term | Meaning |
|---|---|
| **Terminal** | A graphical application. It takes input from the keyboard and passes it to the shell. When the shell has processed the input and produced output, the terminal receives it and displays it on screen. |
| **Interface** | A way by which we interact with a computer. There are many: GUI, shell, etc. |
| **Shell** | A **textual** interface. It is itself a program: it accepts input and processes it by interacting with the OS, then gives back the output. It is an interpreter that translates your commands into something the OS understands. |

Analogy:

| Restaurant | Computer |
|---|---|
| Waiter | Terminal |
| Chef | Shell |

---

## 2. Reading the prompt

```text
username@hostname:<current-directory>($/#)
```

| Symbol | Meaning |
|---|---|
| `$` | You are **not** the root user |
| `#` | You are the root user |
| `~` | Shortcut for your home directory |

- `/home/jayesh` is the home directory of the user `jayesh`.
- The root user has no directory under `/home`. Root's home is `/root`.

Examples:

```text
root@Jayesh:/mnt/c/Users/2019j#
jayesh@Jayesh:~$
```

### Log in as root (WSL)

```powershell
wsl -u root
```

---

## 3. Escape characters

A backslash `\` removes the special meaning of the next character so it is treated literally.

```text
$ echo hello       world
hello world
$ echo hello\ \ \ \ \ world
hello     world
```

In the first command, spaces between arguments are separators, so `echo` receives two arguments (`hello` and `world`). Escaping each space with `\` makes it part of a single argument.

---

## 4. Getting help: `man`

`man` takes the name of another program and shows its manual.

```bash
man echo
```

---

## 5. Where programs live: `PATH` and `which`

When I run `echo`, where does the program live?

The shell uses an environment variable called **`PATH`**. It searches for the program in each folder listed in `PATH`, in order.

```text
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/WINDOWS/system32:...
$ which echo
/usr/bin/echo
$ /usr/bin/echo "hello"
hello
```

- `which` is a program that tells you the path of a program.
- Instead of typing the whole path, we type just the name and the shell searches `PATH` for us.
- `which -a echo` (or `--all`) lists **every** program named `echo` found in `PATH`. If several exist, **the first one found is the one the shell runs**.

---

## 6. Navigating: `cd`, absolute and relative paths

`cd` switches between directories.

```bash
cd /bin
```

A leading `/` means we start from the root (the beginning of the file system). Folders are separated by `/`.

There are two ways to write a path:

| Kind | Meaning | Example |
|---|---|---|
| **Absolute** | Full path from the root | `/home/jayesh/jk` |
| **Relative** | Relative to the current directory | `./` (current directory), `../` (parent) |

```text
$ cd ../jk/../jk/./      # you end up in the same directory you started in
```

---

## 7. Working with files

| Command | What it does |
|---|---|
| `cat file` | Print the contents of a file |
| `head -n2 names.txt` | First 2 lines |
| `tail -n3 names.txt` | Last 3 lines |
| `sort names.txt` | Sort lexicographically |
| `sort -r` | Reverse order |
| `sort -n` | Numeric sort |
| `sort -rn` | Numeric, reversed |
| `uniq names.txt` | Remove **consecutive** duplicate lines |
| `uniq -c names.txt` | Same, but prefix each line with its count |
| `sort -u names.txt` | Sort and remove duplicates |

### `sort -n`

`names.txt`:

```text
2 Jayesh
Jayesh
Ka 1 nnan
Sub 11 a
Kannan
    23Jk
```

How `sort -n` reads each line:

| Line | Number at the beginning | Numeric value used |
|---|---|---|
| `2 Jayesh` | 2 | 2 |
| `Jayesh` | none | 0 |
| `Ka 1 nnan` | none | 0 |
| `Sub 11 a` | none | 0 |
| `Kannan` | none | 0 |
| `    23Jk` | 23 (leading spaces ignored) | 23 |

> **Correction:** your original note said `sort -n` ignores leading whitespace "and considers the first occurring digit in each line". That's not what happens, and your own table shows it: `Ka 1 nnan` counts as 0 even though it contains a `1`. Numeric sort uses only the number at the **start** of the line (after optional leading blanks). Lines that don't start with a number count as 0.

### `uniq` only removes consecutive duplicates

(Your notes wrote `unique`; the command is `uniq`.)

`names.txt`:

```text
Jayesh
Jayesh
Kannan
Suba
Kannan
```

`uniq -c names.txt` gives:

```text
      2 Jayesh
      1 Kannan
      1 Suba
      1 Kannan
```

The two `Kannan` lines are not adjacent, so both are kept. To remove all duplicates, sort first: `sort names.txt | uniq`, or use `sort -u names.txt`.

> **Added note:** the empty output in your original notes is filled in above.

---

## 8. Searching file contents: `grep`

```bash
grep 3 names.txt            # search for "3" in names.txt
grep -r 3 ./                # -r: search recursively through all files under ./
```

To search only `.txt` files under a directory:

```bash
grep 3 -r --include="*.txt" ./
```

`--include` limits which file names are searched. The `-E` flag makes `grep` interpret its **search pattern** as an extended regular expression.

By default, grep searches for the string/pattern on each line, if the line has the string/pattern it returns the entire line. To return only the match string we use -o option:

`names.txt`:

```text
Jayesh 20
Kan 1 nan
0 Latha
Sub23a
```

```bash
grep -o Jayesh names.txt     # Return only "Jayesh" in names.txt
grep Jayesh names.txt        # Return the whole line "Jayesh 20" in names.txt
```

> **Added note:** `--include` takes a glob (like `*.txt`), not a regular expression.

### Mistake I made

```bash
grep -r 3 ./*.txt
```

The shell expands the glob first, so grep actually receives `grep -r 3 ./names.txt`. `-r` is pointless here because we passed a file, not a directory. `-r` is for directories: `grep -r 3 ./` works.

---

## 9. Editing file contents: `sed`

`sed` is a **line editor**.

- By default it modifies the content and prints it to the terminal. It does **not** save changes.
- `-i` tells it to modify the file in place and save. It prints nothing.
- `s/regex/replacement/g`: `s` stands for substitute, `g` for global.

```bash
sed -i 's/kannan/Jayesh/g' */*.txt
```

This goes over each line and replaces **all** occurrences of `kannan` with `Jayesh`. Without `g`, only the **first** occurrence on each line is replaced.

---

## 10. Globs

A glob is a simple pattern language, like regular expressions, for matching file and directory names. It has very few symbols.

| Pattern | Matches |
|---|---|
| `*` | Zero or more characters, **except** the directory separator `/` |
| `?` | Any single character (`?.txt` matches `a.txt`, `b.txt`, `0.txt`) |
| `[0-9]` | One character in the range |
| `[!0-9]` | One character **not** in the range |
| `[CB]at` | `Cat` or `Bat` |
| `**` | Like `*`, but when `globstar` is enabled it also crosses directory boundaries (recursive) |
| `[[:digit:]]`, `[[:lower:]]`, `[[:upper:]]` | POSIX character classes, used inside `[]` |

> **Correction:** your original notes wrote `[[:digits:]]`. The class name is `[[:digit:]]`.
>
> **Added note:** `{a,b}` (brace expansion) is a separate shell feature that's often learned alongside globs. See Exercise 3 in the exercises notes.

### `*` does not cross `/`

```text
/home/jayesh/jk/
    names.txt
    jk1/
        names.txt
```

`*/*.txt`: the first `*` matches **one** directory level (`jk1`), never `jk1/something/deeper`.

### `**` and `globstar`

```bash
shopt -s globstar     # turn globstar ON
shopt -u globstar     # turn globstar OFF
```

Example tree:

```text
/home/jayesh/
    names.txt
    jk/
        hello.txt
        jk1/
            hello.txt
```

With `globstar` on, `ls **` expands to **every** file and directory in the tree, so `ls` receives something like `names.txt`, `jk`, `jk/hello.txt`, `jk/jk1`, `jk/jk1/hello.txt`. Because `ls` lists the **contents** of each directory argument as well as the files given explicitly, entries show up more than once in the output.

---

## 11. Finding files: `find`

```bash
find .          # list every file and folder under the current directory, recursively
```

### Options

| Option | Meaning |
|---|---|
| `-type f` / `-type d` | Only files / only directories |
| `-name "*.txt"` | Match the **basename** only (the part after the last `/`) |
| `-wholename "./[!.]*"` | Match the **entire path**, not just the basename. The * here can consume directory separator(/) as well |
| `-maxdepth N` | Limit how deep `find` goes |
| `-mtime ...` | Filter by modified time |
| `-exec ... \;` | Run a program on each result |

**`-name`** checks only the basename. For `/usr/bin/.data` it checks just `.data`.

```bash
find . -name "*.txt"          # basenames ending in .txt
```

**`-wholename`** applies the pattern to the full path:

```bash
find . -wholename "./[!.]*"   # ignores hidden files and folders directly under the current directory
```

**`-maxdepth`**:

| Value | Meaning |
|---|---|
| `0` | Only the starting point itself |
| `1` | The starting directory plus one level down |

**`-mtime`** works in units of 24 hours:

| Expression | Meaning |
|---|---|
| `-mtime +0` | Modified more than 24 hours ago |
| `-mtime +1` | Modified more than 48 hours ago |
| `-mtime -1` | Modified less than 24 hours ago |
| `-mtime +0.1` | (24/10) more than 2.4 hours ago |
| `-mtime +0.01` | (24/100) more than 14.4 minutes ago |

> **Added note:** with whole numbers, `find` ignores fractions of a day, so `+1` really means "at least 2 full days old". Fractional values like `+0.1` are a GNU `find` extension, so test them on your system before relying on them. For minutes, `-mmin` is simpler (`-mmin +14`).

### `-exec`

`-exec` runs a program on each result. `{}` is where `find` puts each result, and `\;` marks the end of the arguments.

```bash
find ./ -name "*.txt" -exec echo {} \;
```

```text
./jk1/names.txt
./names.txt
```

#### IMPORTANT: `cd` is not a program

`cd` is a shell built-in, and `-exec` only runs programs. To run shell commands, start a shell:

```bash
find ./ -name "*.txt" -exec sh -c 'cd $1' sh {} \;
```

- **Use single quotes.** With double quotes, the *current* shell expands `$1` first, and it has no variable `1`, so the command becomes just `cd`. Single quotes let the *inner* shell expand it.
- `sh` is a shell program. `-c` tells it to run a command string instead of a file (like `python -c`).
- When you run `sh ./hello.sh`, a new shell starts and `$0` is the script name (`./hello.sh`).
- Here, `sh` and `{}` become `$0` and `$1`. `$0` is set to `sh` by convention, and `$1` is `{}`, the path `find` found.

> **Added note:** safer to quote the variable too: `'cd "$1"'`. Also, `cd` here only changes that inner shell's directory, so it is only useful as a demonstration.

### Mistake I made

```bash
-exec "echo hello"
```

The shell passes `echo hello` as **one** word, so `find` looks for a program literally named `echo hello` in `PATH`. There is only `echo`. Write `-exec echo hello` (or `-exec "echo" hello`).

---

## 12. Commands, options and arguments

```bash
sh -c "echo hello"      # sh = command, -c = option, "echo hello" = argument
chmod 777 names.txt     # no options, only arguments
```

There are different kinds of options:

| Kind | Meaning |
|---|---|
| **Global options** | Affect the whole search. Must be given **before** all other options, tests and actions. |
| **Positional options** | Affect only what comes after them. |

For `find` specifically:

| Part | Meaning | Example |
|---|---|---|
| **Global option** | Impacts how the entire search works. Place it after the starting path and before tests and actions. | `-maxdepth` |
| **Test** | Applies a condition to each result | `-name "*.txt"` keeps only paths ending in `.txt` |
| **Action** | What to do with the result | `-exec` runs a program on it |

> **Correction:** your original note said positional options "can be specified anywhere". More precisely, they can appear anywhere, but they only affect the tests and actions that come **after** them.

---

## 13. Parsing with `awk`

- `awk` has its own programming language for parsing files.
- By default each **line** is a row (record), and fields are separated by **spaces**. Each space-separated word is a column (field).
- The code goes inside `{}`.

```bash
awk '{print $1}' names.txt
```

`names.txt`:

```text
kannan
Jayesh Jayesh Jayesh
```

Output:

```text
kannan
Jayesh
```

- `awk` runs the code once for each line.
- `$1` is the first field of the current line.
- `$0` is the **whole current line**.

> **Correction:** your original note said `$0` holds "all the file contents". It holds only the current line (record).

### Mistake I made: double quotes

```bash
awk "{print $1}" names.txt
```

- Double quotes let the *current shell* interpret `$1`.
- The shell has no variable `1`, so it expands to an empty string before `awk` ever sees it.
- `awk` receives `{print }`, which prints whole lines instead of the first field.
- Use single quotes so the shell leaves the contents alone.

### Options

| Option | Meaning |
|---|---|
| `-F ,` | Set the field separator (default is space). Here, comma. |

If a line contains no `,`, the entire line is treated as one field, and `$1` is that whole line.

---

## 14. Single vs double quotes

| | Single quotes `'...'` | Double quotes `"..."` |
|---|---|---|
| Shell interprets contents? | **No**, passed exactly as written | Partly: variables (`$var`), command substitution (`$(...)`) are expanded |
| Prevents word splitting | Yes | Yes |
| Prevents globbing | Yes | Yes |

```text
$ echo '$PATH'
$PATH
$ echo "$PATH"       # the shell replaces $PATH with its value, then passes it to echo
/usr/local/sbin:...
$ echo $PATH         # same expansion, but unquoted (subject to word splitting)
```

Double quotes are normally used to stop the space from acting as an argument separator.

> **Correction:** your original note said double quotes "won't execute another program". They do: `"$(cmd)"` and backticks run the command inside double quotes. What double quotes prevent is **word splitting** and **globbing**.

### `"echo hello"` as a command

```text
$ "echo hello"
```

The shell treats the whole quoted string as one word, so it looks for a program named `echo hello`, and fails. The quotes don't call `echo`.

### Arguments that start with `-`

```bash
grep "-d" names.txt
```

This errors. The shell strips the quotes before `grep` runs, so `grep` receives `-d names.txt`: `-d` is taken as an **option**, and `names.txt` as that option's value.

> **Correction:** your original note suggested `"\-d"` as the fix. That doesn't work either, because the shell also strips the backslash, so `grep` still receives plain `-d`. Quoting and escaping protect characters from the **shell**, not from the program. The fix is to tell the program where options end:
>
> ```bash
> grep -- -d names.txt      # -- marks the end of options
> grep -e -d names.txt      # -e marks the next word as the search pattern
> ```

---

## 15. Redirection and pipes

By default every program's stdin, stdout and stderr are the **terminal**.

| Operator | Meaning | Example |
|---|---|---|
| `<` | Take stdin from a file | `cat < names.txt` |
| `>` | Redirect stdout; **replaces** the file's contents | `cat names.txt > out.txt` |
| `>>` | Redirect stdout; **appends** | `cat names.txt >> out.txt` |
| `\|` | Pass one program's output to the next program's input | `cat names.txt \| grep 'Jayesh'` |

`echo < names.txt` doesn't work. `echo` doesn't read stdin; it only prints its arguments. The shell does attach the file to its stdin, but `echo` ignores it.

---

## 16. Command substitution

`$(...)` makes bash start a **subshell**, run the command, and substitute its output.

```bash
$(cat names.txt)
echo $(cd /)
```

In `echo $(cd /)` the subshell changes **its own** directory and then ends. The current shell's directory stays the same. And since `cd /` prints nothing, `echo` gets no argument.

---

## 17. Arithmetic expansion

```bash
$((1+1))
$((2%2))
num=$((10+10)) && echo $num      # 20
```

All the usual arithmetic operators work inside `$(( ))`.

---

## 18. Conditions

### Syntax

```bash
if condition; then statement; statement; else statement; statement; fi
```

### Which form should I use? Ask yourself:

1. Am I comparing values? Use `[ "$a" = "$b" ]`.
2. Am I checking whether a command succeeded? Use `if command; then`.
3. Am I comparing what a command **printed**? Use `$(command)` inside the test.
4. Could a value contain spaces or be empty? Quote it, as in `"$a"`.

### `[ ]` and `test`

- `[` (also written `test`) compares values or checks a condition.
- Exit status: `0` means success (true); any non-zero means failure (false).
- `[ "hello" = "hello" ]` and `test hello = hello` are equivalent. The `[ ]` form is preferred.
- `=` and `==` both work, but `=` is the common choice.
- Useful test option: `-f filename` succeeds if the file exists.

```bash
if cat < names.txt; then echo "contents of names.txt is printed"; else echo ":(  failed"; fi
if [ $(cat < hello.txt) = hello ]; then echo "printed contents of hello.txt"; else echo ":( failed"; fi
if [ "$name" = "Jayesh" ]; then echo success; else echo failure; fi
if [ -f names.txt ]; then echo "file exists"; fi
```

> **Added note:** quote the substitution in the second example, `[ "$(cat < hello.txt)" = hello ]`, so an empty or multi-word output doesn't break the test.

### Mistakes I made

**1. `if [echo hello = hello]`**

There's no space after `[`, so the shell looks for a program named `[echo`, which doesn't exist. `[` is itself a program (`which [` gives `/usr/bin/[`). It needs spaces around it, and a final `]` that is also separated by a space.

**2. `if [ echo hello = hello ]`**

`[` receives four arguments: `echo hello = hello`. It expects a value, an operator and a value, so it complains about **too many arguments**. It's equivalent to `test echo hello = hello`.

Fix: `[ $(echo hello) = hello ]`, so the shell passes the command's **output** to `test`.

**3. `if [ cat < hello.txt = hello ]`**

The shell applies the `< hello.txt` redirection to the `[` command itself, which ignores stdin. `test` just sees `cat = hello`. The contents of `hello.txt` never reach `cat`, because `cat` isn't run as a command here.

Fix: `if [ $(cat < hello.txt) = hello ]`.

> **Correction:** your original notes wrote the equivalent `test` calls without the `=`. I added it back since `test` needs the operator.

---

## 19. Loops

### While loop

```bash
while condition; do statement; statement; done
```

Use `break` to leave an infinite loop.

### For loop

```bash
for var in (some iterable); do statement; statement; done
```

### Example: number 1 to 10, odd or even

```text
$ for var in $(seq 1 10); do echo "The number is: $var"; if [ $(($var % 2)) == 0 ]; then echo "$var is even"; else echo "$var is odd"; fi; done
The number is: 1
1 is odd
The number is: 2
2 is even
The number is: 3
...
```

- `seq 1 10` prints numbers 1 to 10.
- `seq 2 2 10` starts at 2, steps by 2, ends at 10: `2 4 6 8 10`.
- `{1..10}` also generates a sequence.

### Example: infinite loop with a break

```text
$ cnt=1; while [ $(cat < hello.txt) = hello ]; do echo "hello"; cnt=$(($cnt +1)); echo $cnt; sleep 2; if [ $(echo $cnt) = 2 ]; then break; fi; done
hello
2
```

The loop would run forever (as long as `hello.txt` contains `hello`), but it breaks when `cnt` reaches 2.

---

## 20. Exit status

`$?` holds the exit status of the **previous command**: `0` for success, non-zero for failure.

```bash
ls /tmp; echo $?             # 0
ls /nonexistent; echo $?     # non-zero
```

---

## 21. Bash scripts

### Shebang

The first line of a script starts with `#!`, called the **shebang**. It tells the OS which program should run the code below.

```bash
#! /bin/bash          # run this script with bash
#! /usr/bin/python    # run it with python
```

`which bash` should print the same path you wrote after `#!`.

> **Correction:** your original sample wrote `#! bin/bash` (missing the leading `/`), which is a relative path and wouldn't work. Also, shebang isn't only a Linux feature; it works on Unix-like systems generally (Linux, macOS, BSD). A portable form is `#!/usr/bin/env bash`.

### `set -euo pipefail`

Placed at the very top of a script, right after the shebang.

`set` turns shell features on (`-`) or off (`+`) while the script runs.

| Option | Meaning |
|---|---|
| `-e` | If any command fails, **exit immediately** |
| `+e` | Opposite: disable the strict failing |
| `-u` | If a variable has no value, **exit** instead of silently using an empty string |
| `-o pipefail` | A pipeline (`a \| b \| c`) counts as failed if **any** command in it fails, not only the last one |

> **Added note:** more precisely, with `pipefail` the pipeline's exit status is that of the last command that failed. Combined with `-e`, that makes the script exit.

Example: temporarily turning strict mode off.

```bash
#! /bin/bash

set -euo pipefail

set +e          # strict mode temporarily turned off
cat < hello.t
set -e          # turned back on
echo "end"
```

```text
$ ./hello.sh
./hello.sh: line 6: hello.t: No such file or directory
end
```

`cat` fails, but the script continues and prints `end`.

### Why `./hello.sh` instead of just `hello.sh`?

Suppose the shell allowed running `hello.sh` without `./`. If you created your own program called `ls` and typed `ls`, the shell would always run the one in the **current directory**, instead of the real `ls`.

To avoid this, user-created programs must be run with their path. The standard programs are found by searching `PATH`.

### Why can't I run it right after creating it?

Files you create don't have the **execute** permission by default. Add it first:

```bash
chmod +x hello.sh
```

---

## 22. Arrays and `${}`

### Creating an array

```bash
numbers=(10 Jayesh 90 "Jayesh Krishna")
```

| Index | Value |
|---|---|
| 0 | `10` |
| 1 | `Jayesh` |
| 2 | `90` |
| 3 | `Jayesh Krishna` |

Values are space separated (quote one to keep a space inside it).

```bash
echo $numbers            # 10        (just index 0)
echo $numbers[1]         # 10[1]     (wrong: $numbers is expanded, then "[1]" is literal text)
echo ${numbers[1]}       # Jayesh    (correct)
```

### How `[@]`, `[*]` and quotes behave in a `for` loop

| Loop | Expands to | Output |
|---|---|---|
| `for v in ${numbers[@]}` | `10 Jayesh 90 Jayesh Krishna` (5 words) | `10`, `Jayesh`, `90`, `Jayesh`, `Krishna` |
| `for v in "${numbers[@]}"` | `"10" "Jayesh" "90" "Jayesh Krishna"` (4 words) | `10`, `Jayesh`, `90`, `Jayesh Krishna` |
| `for v in "${numbers[*]}"` | `"10 Jayesh 90 Jayesh Krishna"` (1 word) | `10 Jayesh 90 Jayesh Krishna` |
| `for v in ${numbers[*]}` | `10 Jayesh 90 Jayesh Krishna` (5 words) | `10`, `Jayesh`, `90`, `Jayesh`, `Krishna` |

Full loop:

```bash
for eachValue in "${numbers[@]}"; do echo $eachValue; done
```

**Rule of thumb:** `"${array[@]}"` keeps each element intact; this is almost always what you want.

### What is `${}`?

It's **parameter expansion**, different from `$()` (command substitution). It marks where a variable name ends.

```bash
name=Jayesh
echo $name123       # looks for a variable called "name123" (prints nothing)
echo ${name}123     # Jayesh123
```

---

## 23. User management

### Users

```bash
useradd -m jk
```

| Part | Meaning |
|---|---|
| `useradd` | The program |
| `-m` | Create a home directory under `/home` (named after the user) |
| `jk` | The username |

**Primary group:** every user gets a primary group. When a user is created, a group with the same name is created and made their primary group.

**Change a user's primary group:**

```bash
usermod -g developers jk
```

At any given time a user has **one** primary group and can belong to **any number** of supplementary groups.

**Change supplementary groups:**

```bash
usermod -aG testers jk
```

| Option | Meaning |
|---|---|
| `-a` | Append: keep the existing supplementary groups |
| `-G` | The supplementary group(s) to set |

Using `-G` **without** `-a` removes the user from all their current supplementary groups and sets only the ones you list.

**Change the login shell:**

```bash
usermod -s /usr/bin/bash jk
```

- The default shell is `sh` (`/usr/bin/sh`), which only shows `$` or `#` as the prompt.
- `bash` shows `username@hostname:<current dir>$/#`.
- `-s` works with both `usermod` and `useradd`.

**Delete a user:**

```bash
userdel jk        # deletes the user but leaves the home directory
userdel -r jk     # also removes the home directory
```

If the user has a running process, `userdel` refuses with an error. Use `ps` to see processes and `kill` to stop them (more on that later).

> **Correction:** your original notes wrote `usedel`; the command is `userdel`.

**Set a password:**

```bash
passwd jk
```

> There is also a *database* called `passwd`, which is different from this program.

**Add a description to a user:**

```bash
usermod -c "Im a tester" sb
```

(See the `getent passwd` explanation below.)

### Groups

Groups exist to manage file permissions for many users effectively. Imagine giving 50 users read and write access to a file, and another 50 users only execute access. Without groups that is painful; with groups it is easy.

```bash
groupadd developers      # create a group
groupdel developers      # delete a group
```

**Why are there two kinds of groups?**

- When a user creates a file, Linux has to decide which group the file belongs to. That's the job of the **primary group**: files and directories a user creates go to their primary group by default.
- **Supplementary groups** give a user extra access. Example:
  - Developers must be in both `developers` and `testers`.
  - Testers must be only in `testers`.
  - Both groups can access all files, but `developers` get write and execute permissions, while `testers` only get read.

**Change a file's group:**

```bash
chgrp developers hello.sh
```

This changes only which group the file belongs to. It does **not** change the permissions the group has on it.

### Permissions: `chmod`

```text
-   rwx   r-x   r--
    │     │     │
    │     │     └── Others
    │     └──────── Group
    └────────────── Owner
```

| Symbol | Meaning |
|---|---|
| `+` | Add a permission |
| `-` | Remove a permission |
| `=` | Set exactly this permission |
| `u` | Owner (user) |
| `g` | Group |
| `o` | Others |

```bash
chmod +x hello.sh        # add execute for all three
chmod -x hello.sh        # remove execute for all three
chmod u=rwx hello.sh     # owner gets exactly rwx
chmod u= hello.sh        # remove all three permissions for the owner
```

> **Correction:** your original note wrote `chmod u hello.sh` to remove all permissions for the owner. That isn't a valid mode. Use `chmod u= hello.sh` (set the owner's permissions to nothing).

### Verifying what we did

#### `ls -l`

```text
$ ls -l hello.sh
-rwxrw-r-- 1 root testers 160 Oct 18 13:40 hello.sh
```

| Part | Meaning |
|---|---|
| `-rwxrw-r--` | First character is the type (`-` file, `d` directory), then owner `rwx`, group `rw-`, others `r--` |
| `1` | Number of hard links. |
| `root` | Owner (the user who created it) |
| `testers` | The group the file belongs to |
| `160` | Size in bytes |
| `Oct 18 13:40` | Last modified |
| `hello.sh` | File name |

> **Correction:** your original note said `ls -lH` prints human-readable sizes. It's lowercase: `ls -lh` (for example `160K` instead of `163840`). `-H` is a different option.
>
> **Added note:** the `1` (hard link count) was missing from your explanation.

#### `id`

```text
$ id jk
uid=1001(jk) gid=1001(developers) groups=1001(developers),1002(testers)
```

- Every user has a **uid**; every group has a **gid**.
- `gid` is the primary group.
- In `groups=`, the first one is the primary group and the rest are supplementary.

#### `getent`

`getent` reads entries from the system's databases.

- The `passwd` database tracks all users, including system-created ones.
- The `group` database tracks all groups.

```bash
getent passwd jk            # passwd = database, jk = key
getent group developers
```

**`getent passwd sb`**

```text
sb:x:1002:1002:I'm a tester:/home/sb:/usr/bin/bash
```

| Field | Meaning |
|---|---|
| `sb` | Username |
| `x` | Password placeholder (the real password isn't shown) |
| `1002` | uid |
| `1002` | Primary group id |
| `I'm a tester` | Description |
| `/home/sb` | Home directory |
| `/usr/bin/bash` | Login shell |

**`getent group testers`**

```text
testers:x:1002:sb,jk,root
```

| Field | Meaning |
|---|---|
| `testers` | Group name |
| `x` | Group password placeholder |
| `1002` | gid |
| `sb,jk,root` | Users for whom this is a **supplementary** group. Users whose *primary* group it is are not listed here. |

Using these commands together lets you verify user, group and file details and manage permissions properly.

### User-management cheatsheet

| Command | Purpose |
|---|---|
| `useradd` | Create a user |
| `passwd` | Set a password |
| `usermod` | Modify a user (`-g`, `-aG`, `-s`, `-c`) |
| `userdel` | Delete a user (`-r` removes the home directory) |
| `groupadd` | Create a group |
| `groupdel` | Delete a group |
| `chgrp` | Change a file's group |
| `chmod` | Change file permissions |
| `getent` | Look up database entries (`passwd`, `group`) |
| `id` | Show a user's uid, gid and groups |

---

## 24. `cut`

Like `awk`, `cut` parses file contents.

| Option | Meaning |
|---|---|
| `-d:` / `-d" "` / `-d,` | Field separator (like `awk -F ,`) |
| `-f1`, `-f2` | Pick the 1st / 2nd / ... field of each line (like `{print $1}` in awk) |

```bash
getent passwd | cut -d: -f1       # all usernames
```

---

## 25. Quick revision sheet

### Where is a program, and how do I run it?

| Need | Use |
|---|---|
| Find a program's path | `which name` (`which -a name` for all matches) |
| Read a manual | `man name` |
| Run a script in the current directory | `./script.sh` (and `chmod +x script.sh` first) |

### Quotes

| Need | Use |
|---|---|
| No interpretation at all | `'...'` |
| Keep spaces together, but expand variables and `$(...)` | `"..."` |
| Argument that starts with `-` | `cmd -- -arg` (quotes and `\` don't help) |

### Quote rules in common tools

| Tool | Always use |
|---|---|
| `awk` | `'{print $1}'` (single quotes, so `$1` isn't expanded by the shell) |
| `find -exec sh -c` | `'cd "$1"'` (single quotes around the command string) |

### Conditions cheat sheet

```bash
if [ "$a" = "$b" ]; then ...; fi          # compare values
if command; then ...; fi                   # did the command succeed?
if [ "$(command)" = value ]; then ...; fi  # compare what a command printed
[ -f file ]                                # does the file exist?
```

### Safe script header

```bash
#! /bin/bash
set -euo pipefail
```

### Find, grep, sed, awk, cut in one glance

```bash
find . -type f -name "*.txt"                    # files by name
find . -maxdepth 1 -type d                      # directories one level down
find . -name "*.txt" -exec echo {} \;           # run a program on each result
grep -r --include="*.txt" 3 ./                  # search text files recursively
sed -i 's/old/new/g' file.txt                   # replace all, save in place
awk -F , '{print $1}' file.csv                  # first comma-separated field
getent passwd | cut -d: -f1                     # all usernames
```

### Common mistakes

- `grep -r 3 ./*.txt`: the glob expands first, so `-r` is useless; pass a directory.
- `awk "{print $1}"`: use single quotes so the shell doesn't expand `$1`.
- `-exec "echo hello"`: it becomes one program name; write `-exec echo hello`.
- `[echo hello = hello]`: needs spaces around `[` and `]`.
- `[ echo hello = hello ]`: use `[ $(echo hello) = hello ]` to compare output.
- `echo $numbers[1]`: use `${numbers[1]}`.
- `uniq` only removes **adjacent** duplicates; sort first.
- `grep "-d"`: quotes don't hide `-d` from the program; use `--`.
- `usermod -G` without `-a` replaces all supplementary groups.
- `chmod u file` is invalid; use `chmod u= file` to clear permissions.
