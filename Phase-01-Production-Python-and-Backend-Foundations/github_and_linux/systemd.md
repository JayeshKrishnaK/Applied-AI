# systemd, journalctl and unit files: a learning guide (WSL)

Notes from learning systemd from scratch on WSL. Organised by topic, with the doubts, follow-up questions and edge cases that came up along the way.

## Table of contents

1. [Background: kernel, init, systemd](#1-background-kernel-init-systemd)
2. [Enabling systemd on WSL](#2-enabling-systemd-on-wsl)
3. [Core vocabulary](#3-core-vocabulary)
4. [Units: what they are and where they live](#4-units-what-they-are-and-where-they-live)
5. [Unit file structure](#5-unit-file-structure)
6. [Service units](#6-service-units)
7. [Timer units](#7-timer-units)
8. [Target units](#8-target-units)
9. [Controlling units with systemctl](#9-controlling-units-with-systemctl)
10. [journalctl and the journal](#10-journalctl-and-the-journal)
11. [Other logging systems](#11-other-logging-systems)
12. [Symlinks, hard links and how systemd uses them](#12-symlinks-hard-links-and-how-systemd-uses-them)
13. [Edge cases and gotchas](#13-edge-cases-and-gotchas)
14. [Cheat sheet](#14-cheat-sheet)
15. [Practice exercises](#15-practice-exercises)

---

## 1. Background: kernel, init, systemd

Boot sequence in short:

1. Firmware (BIOS/UEFI) runs, then a bootloader loads the **Linux kernel**.
2. The kernel sets up hardware and memory, then starts the **init system** as **PID 1**.
3. The init system starts everything else: mounts disks, brings up networking, starts services, shows the login prompt.

Every other process on the machine is a child (or grandchild) of PID 1.

**systemd** is the most common init system (Ubuntu, Debian, Fedora, RHEL, Arch). It is more than "the first program": it is a family of programs.

| Piece | Role | Tool |
|---|---|---|
| `systemd` | PID 1, the manager | `systemctl` |
| `systemd-journald` | Collects and stores logs | `journalctl` |
| `systemd-logind` | Tracks logins and sessions | `loginctl` |
| `systemd-networkd` | Network config (optional) | `networkctl` |
| `systemd-resolved` | DNS (optional) | `resolvectl` |
| `systemd-analyze` | Boot time and unit verification | `systemd-analyze` |

`ctl` means **control**. `systemctl` = "system control", `journalctl` = "journal control".

Other init systems exist: SysV init (old), OpenRC (Alpine, Gentoo), runit (Void). They have no `journalctl`.

What systemd does:

- Starts services in the right order, in parallel where possible
- Stops them cleanly
- Restarts them on crash
- Adopts and cleans up orphan processes
- Collects their output into the journal
- Schedules jobs (timers)

---

## 2. Enabling systemd on WSL

Older WSL setups do not run systemd, so `journalctl` shows nothing and `systemctl` fails with errors like:

```
No journal files were found.
System has not been booted with systemd as init system
```

Check what PID 1 is:

```bash
ps -p 1 -o comm=
```

- `systemd` means systemd is running.
- `init` means it is not.

Enable it (WSL 0.67.6 or newer):

```bash
sudo nano /etc/wsl.conf
```

```ini
[boot]
systemd=true
```

Then in **PowerShell** run `wsl --shutdown` and reopen the distro.

Why WSL is different: it is not booted like a normal machine (no bootloader), and it historically used a tiny custom init instead of systemd. The `wsl.conf` setting makes WSL start real systemd as PID 1.

Other WSL notes:

- Timers only fire while WSL is running. WSL can shut down when no terminal is open and nothing is running.
- `WakeSystem=` in timers is meaningless on WSL.
- If a broken default target ever locks you out, open a root shell from PowerShell with `wsl -u root` and fix it there.

---

## 3. Core vocabulary

| Term | Meaning |
|---|---|
| **Program** | A file on disk, not running |
| **Process** | A running program, with a PID |
| **Daemon** | A background process, no terminal, long-lived, providing something. Names often end in `d`: `sshd`, `systemd`, `journald` |
| **Service** | A systemd unit (`.service`) describing how to run and manage a daemon. Also used casually for the running daemon itself |
| **Unit** | Anything systemd manages. A service is one type of unit |

Relationship:

```
Unit (general) > Service (a unit type) --manages--> Daemon (background process) --is a--> Process
```

Examples: `sshd` is the daemon, `ssh.service` is the service unit, `ls` is a process but not a daemon, a `.timer` is a unit but not a service.

### What is a service, practically?

A **service** is a program that keeps running in the background without you starting or watching it.

| | Script run by hand | Service |
|---|---|---|
| Needs a terminal | Yes | No |
| Closing the terminal | Kills it | Keeps running |
| Crashes | Stays dead | Can auto-restart |
| After reboot | Gone | Can auto-start |
| Output | Lost with the terminal | Saved in the journal |

### Is the service a different process from the program it starts?

A service is not a process. It is a managed group of processes. systemd starts your program as the "main process" and tracks it.

```bash
systemctl status ssh
```

```
Main PID: 812 (sshd)
CGroup: /system.slice/ssh.service
        └─812 "sshd: /usr/sbin/sshd -D ..."
```

- **Service** = the unit (definition and bookkeeping)
- **Process** = the running program (PID 812)
- **CGroup** = a kernel feature systemd uses to keep every process the service creates in one group, so `stop` reliably kills the main process and its children

A service can contain several processes (nginx runs a master plus workers; your Python script may spawn subprocesses). The unit still exists when no process is running.

---

## 4. Units: what they are and where they live

A unit is **one thing systemd manages, described by one small text file**. The name ends with the type: `ssh.service`, `backup.timer`, `multi-user.target`. When you type `systemctl start ssh`, `.service` is assumed.

### Unit types

| Type | Manages | Example |
|---|---|---|
| `.service` | A program/process | `ssh.service` |
| `.timer` | Schedule that triggers another unit | `apt-daily.timer` |
| `.target` | A group of units / boot milestone | `multi-user.target` |
| `.socket` | A socket; can start a service on connection | `docker.socket` |
| `.mount` | A filesystem mount | `home.mount` |
| `.path` | Watches a file/folder and triggers something | |
| `.device` | A hardware device | |
| `.slice` | CPU/memory limits for a group of processes | `user.slice` |

Most important for now: **service, timer, target**.

### Where systemd looks for unit files

Searched in priority order, first match wins:

| Folder | Who puts files here | Priority |
|---|---|---|
| `/etc/systemd/system/` | **You** (the admin) | Highest |
| `/run/systemd/system/` | Temporary, runtime-generated | Middle |
| `/usr/lib/systemd/system/` (also `/lib/systemd/system/` on Ubuntu/Debian) | **Packages** (`apt install`) | Lowest |

- Put your own units in `/etc/systemd/system/`.
- Never edit files under `/usr/lib/...`; package updates overwrite them.
- `systemctl cat <unit>` shows the file systemd found and its path.
- Per-user units live in `~/.config/systemd/user/` and are managed with `systemctl --user` (not needed at first).

### Customising a package's unit: `edit` vs `edit --full`

Both avoid touching the package's original file.

| | `systemctl edit ssh` | `systemctl edit --full ssh` |
|---|---|---|
| Creates | A **drop-in**: `/etc/systemd/system/ssh.service.d/override.conf` | A **full copy**: `/etc/systemd/system/ssh.service` |
| You write | Only the keys you want to change | The whole file |
| Original file | Still used, your changes merged on top | Ignored completely |
| Package updates | Still apply to everything not overridden | Stop reaching you; you own the file |

Example drop-in:

```ini
[Service]
Restart=always
```

`systemctl cat ssh` then shows the original followed by the drop-in.

**List-type keys such as `ExecStart=`**: a drop-in *adds* to the list. To replace, clear it first:

```ini
[Service]
ExecStart=
ExecStart=/usr/sbin/sshd -D -e
```

Both commands run `daemon-reload` for you. To undo: `sudo systemctl revert ssh` (removes drop-ins and/or the full copy in `/etc`; it does not delete a unit file you created yourself that has no vendor version).

---

## 5. Unit file structure

Plain text, INI format: `[Sections]` containing `Key=Value` lines. `#` and `;` start comments. Keys are case-sensitive.

```ini
[Unit]        # who am I, what do I depend on
Description=My hello service
After=network.target

[Service]     # type-specific section: what to run and how
ExecStart=/usr/bin/python3 /home/YOURUSER/hello.py
User=YOURUSER
Restart=on-failure

[Install]     # used by "systemctl enable"
WantedBy=multi-user.target
```

- `[Unit]` and `[Install]` exist for every type.
- The middle section matches the type: `[Service]`, `[Timer]`, `[Socket]`, `[Mount]`...
- Targets have no type-specific section.

### `[Unit]` keys (common to all types)

| Key | Meaning |
|---|---|
| `Description=` | Text shown in `systemctl status` |
| `Documentation=` | Link or man page, e.g. `man:sshd(8)` |
| `After=` / `Before=` | Ordering only |
| `Wants=` | Soft dependency: also start these; I can run without them |
| `Requires=` | Hard dependency: if they fail or stop, I stop |
| `Conflicts=` | Cannot run together; starting me stops them |
| `OnFailure=` | Start this unit if I fail |
| `StartLimitIntervalSec=` / `StartLimitBurst=` | Give up restarting after too many starts in a window |

### What does `man:sshd(8)` mean?

The number in brackets is the **manual section**:

| Section | Contains |
|---|---|
| 1 | Commands for normal users (`ls`) |
| 2 | System calls |
| 3 | Library functions |
| 5 | File formats and config files (`sshd_config`) |
| 7 | Overviews and concepts |
| 8 | Admin commands (`sshd`, `mount`) |

Read with `man 8 sshd` or `man 5 sshd_config`.

### Ordering vs dependency: `After=` with and without `Wants=`/`Requires=`

Two separate questions:

| Question | Key |
|---|---|
| Should that unit also be started? | `Wants=` / `Requires=` |
| If both start, who goes first? | `After=` / `Before=` |

For `myapp` and `postgres`:

- **Only `Wants=postgres.service`**: both start in parallel. myapp may start before the database is ready.
- **Only `After=postgres.service`**: starting myapp does *not* start postgres. If postgres is being started anyway (e.g. both enabled at boot), myapp waits for it. If not, the line is ignored.
- **Both** (the usual pairing): postgres is pulled in and myapp waits for it.

`After=network.target` is a typical "ordering only" use: don't start the network, just wait if it is being set up.

### `Before=` a unit that is already running

Nothing happens. `After=`/`Before=` only matter when both units are being started together (e.g. at boot). systemd does not stop or restart an already-running unit.

### StartLimitIntervalSec and StartLimitBurst

They stop a crashing service from restarting forever. Both go in `[Unit]`:

```ini
[Unit]
StartLimitIntervalSec=60
StartLimitBurst=3

[Service]
Restart=on-failure
RestartSec=5
```

Meaning: at most 3 starts within 60 seconds, then give up. The unit enters `failed` with `start-limit-hit`. Clear it with:

```bash
sudo systemctl reset-failed myapp
sudo systemctl start myapp
```

Notes: default is 5 starts in 10 seconds; `StartLimitIntervalSec=0` disables the limit; if `RestartSec` is large relative to the window, the limit may never trigger.

---

## 6. Service units

### `[Service]` keys

**What to run**

| Key | Meaning |
|---|---|
| `ExecStart=` | The main command (required, with exceptions for some oneshot units) |
| `ExecStartPre=` / `ExecStartPost=` | Commands before / after the main one |
| `ExecReload=` | Command run on `systemctl reload` |
| `ExecStop=` | Command to stop; if omitted systemd sends a stop signal |

`ExecStart` needs a **full path** and is **not run by a shell**, so `|`, `&&`, `~` and `>` do not work directly. Use `ExecStart=/bin/bash -c '...'` if you need them.

**Who and where**

| Key | Meaning |
|---|---|
| `User=` / `Group=` | Run as this user/group (default is root, so set it) |
| `WorkingDirectory=` | Folder to start in |
| `Environment=` | `Environment=DEBUG=1` |
| `EnvironmentFile=` | Load `KEY=value` lines from a file; prefix `-` means "don't fail if missing" |

**Restart behaviour**

| Key | Meaning |
|---|---|
| `Restart=` | `no` (default), `on-failure`, `always`, `on-success` |
| `RestartSec=` | Wait before restarting |

**Timeouts and output**

| Key | Meaning |
|---|---|
| `TimeoutStartSec=` / `TimeoutStopSec=` | Startup wait / wait after stop signal before force-kill |
| `StandardOutput=` / `StandardError=` | Default `journal`; also `null` or `append:/path/file.log` |
| `SyslogIdentifier=` | Name that tags this service's journal lines |

### `[Install]` keys

| Key | Meaning |
|---|---|
| `WantedBy=` | Start me when this target is reached; almost always `multi-user.target` |
| `RequiredBy=` | Hard version (rare) |
| `Alias=` | Extra name |
| `Also=` | Enable these units together with me |

### `Type=`: how systemd knows the service has "started"

| Type | systemd says "started" when... | Use for |
|---|---|---|
| `simple` (default) | the process is launched (not checked) | long-running programs |
| `exec` | the program is confirmed launched | same, with better error reporting |
| `oneshot` | the process has **finished** | run-and-exit scripts that others depend on |
| `forking` | the parent process **exits** (a child carries on) | old daemonizing programs |
| `notify` | the program tells systemd it is ready | programs written for systemd |

#### simple vs oneshot, and why it matters for ordering

`After=job.service` waits until job.service is "started". With `simple` that is immediate; with `oneshot` that is after the script finishes.

Example: `setup` takes 10 s to create `/tmp/ready.txt`; `app` needs it.

```ini
# app.service
[Unit]
Wants=setup.service
After=setup.service

[Service]
Type=oneshot
ExecStart=/usr/bin/cat /tmp/ready.txt
```

- `setup` as `Type=simple`: app starts immediately, the file does not exist yet, error.
- `setup` as `Type=oneshot`: systemd waits ~10 s, then starts app, it prints "ready".

Behaviour of a 10-second script:

| | simple | oneshot |
|---|---|---|
| `systemctl start` returns | immediately | after the script finishes |
| While running | `active (running)` | `activating` |
| Units ordered `After=` it | start right away | wait for completion |

With `oneshot`, add `RemainAfterExit=yes` to keep the unit shown as `active (exited)` after it ends.

#### forking

Old-style daemons start, split a copy of themselves into the background, and the original exits. With `Type=simple`, systemd sees the original exit, thinks the service ended, and kills the leftover child. With `Type=forking`, systemd waits for the parent to exit and treats the child as the real service (optionally `PIDFile=` to say which).

Demo launcher (`~/launcher.sh`):

```bash
#!/bin/bash
/usr/bin/python3 /home/YOURUSER/hello.py &
exit 0
```

- `Type=simple`: ends up `inactive (dead)`, hello.py gets killed.
- `Type=forking`: `active (running)`, counting keeps appearing in the journal.

Your own Python scripts should run in the foreground and use `simple`.

#### exec vs simple

Both mean "the process is the service". The difference is when systemd says "started":

- `simple`: right after it *tries* to launch.
- `exec`: after the launch really succeeded.

With a wrong path like `ExecStart=/usr/bin/doesnotexist`:

- `simple`: `systemctl start` reports success; the failure only shows up afterwards in `status` (`status=203/EXEC`).
- `exec`: `systemctl start` itself fails.

`exec` does not wait for the program to finish (that is `oneshot`) or be ready (that is `notify`).

### Template for a long-running Python service

```ini
[Unit]
Description=My Python app
After=network.target

[Service]
Type=simple
User=YOURUSER
WorkingDirectory=/home/YOURUSER/myapp
EnvironmentFile=-/home/YOURUSER/myapp/.env
ExecStart=/home/YOURUSER/myapp/venv/bin/python app.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Point at the virtualenv's python directly; a service does not activate venvs like your shell does.

### Creating your own service, step by step

1. **Run the command by hand first.** Whatever goes in `ExecStart` must work in your terminal.
2. **Create the file** in `/etc/systemd/system/` with a name ending `.service`:
   ```bash
   sudo nano /etc/systemd/system/myapp.service
   ```
3. **Check it:**
   ```bash
   systemd-analyze verify /etc/systemd/system/myapp.service
   ```
   No output means no problems found.
4. **Reload systemd's view of the files** (needed after every edit):
   ```bash
   sudo systemctl daemon-reload
   ```
5. **Start and check:**
   ```bash
   sudo systemctl start myapp
   systemctl status myapp
   ```
6. **Read the output:** `journalctl -u myapp -f`
7. **Start at boot (optional):** `sudo systemctl enable myapp` (or `enable --now`)
8. **To change something:** edit, `daemon-reload`, `restart`.

Minimal hello service for practice:

```python
# ~/hello.py
import time

n = 0
while True:
    n += 1
    print(f"hello, count={n}", flush=True)
    time.sleep(5)
```

`flush=True` matters: without a terminal Python buffers output, so lines would appear late or not at all in the journal.

### Using `input()` in a service: `EOFError`

EOF means "end of file": no more data to read. `input()` reads from **stdin**. A service has no terminal or keyboard, so systemd connects stdin to `/dev/null`, which is always empty. The first `input()` raises `EOFError: EOF when reading a line`.

Reproduce without systemd:

```bash
python3 -c "input('name: ')" < /dev/null
```

A background service cannot ask anyone anything. Pass settings another way:

- Arguments: `ExecStart=/usr/bin/python3 app.py --port 8080`
- Environment: `Environment=PORT=8080` or `EnvironmentFile=`
- A config file

For secrets, use an `EnvironmentFile=` with restricted file permissions.

---

## 7. Timer units

A timer **never runs a command itself**. It decides *when*, then starts a **service** that does the work. You always make two files:

```
hello.timer  --(schedule)-->  hello.service  --> runs the script
```

By default `x.timer` triggers `x.service` (same name). Override with `Unit=`.

### `[Timer]` keys

**Calendar-based (clock time)**

| Key | Meaning |
|---|---|
| `OnCalendar=` | Fire at a date/time pattern |
| `Persistent=` | `true`: if the machine was off at the scheduled time, run once at next startup |

**Monotonic (relative to an event)**

| Key | Counts from |
|---|---|
| `OnBootSec=` | when the machine booted |
| `OnStartupSec=` | when systemd started |
| `OnActiveSec=` | when **this timer** was activated |
| `OnUnitActiveSec=` | when the service **last started** |
| `OnUnitInactiveSec=` | when the service **last stopped** (success or failure) |

Time values: `30s`, `5min`, `2h`, `1d`, `1h 30min`.

**Other keys**

| Key | Meaning |
|---|---|
| `Unit=` | Which unit to start (default: same-name service) |
| `AccuracySec=` | How late the timer may fire (default **1 min**) |
| `RandomizedDelaySec=` | Add a random delay up to this much |
| `FixedRandomDelay=` | `true`: the random delay is the same on each run of this machine |
| `WakeSystem=` | `true`: wake the computer from suspend to run |

### `[Install]` for timers

```ini
[Install]
WantedBy=timers.target
```

### OnCalendar format

```
DayOfWeek Year-Month-Day Hour:Minute:Second
```

`*` is "any"; day-of-week and seconds are optional.

| Expression | Meaning |
|---|---|
| `*-*-* 02:00:00` | Every day at 2:00 AM |
| `*-*-* *:*:00` | Every minute |
| `*-*-* *:00/15:00` | Every 15 minutes |
| `Mon *-*-* 09:00:00` | Mondays at 9:00 AM |
| `Mon..Fri *-*-* 18:30` | Weekdays at 6:30 PM |
| `*-*-01 00:00:00` | First of every month at midnight |

Shortcuts: `minutely`, `hourly`, `daily`, `weekly`, `monthly`.

Test an expression before using it:

```bash
systemd-analyze calendar "Mon..Fri *-*-* 18:30"
```

### The keys that were confusing

**OnActiveSec** fires once, this long after the timer itself was started. It does not repeat on its own.

```ini
OnActiveSec=10s          # first run 10 s after the timer starts
OnUnitActiveSec=1min     # then every minute after each start
```

Restarting the timer restarts the `OnActiveSec` countdown.

**AccuracySec** is the lateness tolerance. The timer may fire anywhere from the scheduled time to scheduled time + `AccuracySec`. Default 1 minute, so systemd can group wake-ups and save power. For precise timing set `AccuracySec=1s`.

**RandomizedDelaySec** always adds a random delay between 0 and the value. Use it to spread load, e.g. 1000 servers with `OnCalendar=daily` each picking a delay within `30min` instead of all hitting a server at midnight.

| | AccuracySec | RandomizedDelaySec |
|---|---|---|
| Purpose | Save power by grouping wake-ups | Spread load across machines |
| Behaviour | systemd *may* fire late within the window | systemd *always* adds a random delay |
| Default | 1 min | 0 |

**WakeSystem** wakes the machine from suspend (needs RTC alarm hardware). Default `false`: a timer that comes due during suspend runs when the machine wakes. Not meaningful on WSL.

### Do I always need `OnBootSec`? What does "you need the first one" mean?

No. `OnBootSec` is not required.

`OnUnitActiveSec=` counts from when the service **last started**. If the service has never started there is nothing to count from, so the timer never fires. This alone does nothing:

```ini
[Timer]
OnUnitActiveSec=10min
```

You need **some other starter** for the first run, after which `OnUnitActiveSec` repeats it. Any of these work: `OnBootSec=`, `OnActiveSec=`, `OnStartupSec=`, or `OnCalendar=`.

The same applies to `OnUnitInactiveSec=`. (If you manually start the service once, it gets a "last start" time and `OnUnitActiveSec` can count from it, but that is fragile; use a starter.)

If you list several keys, **any one** firing triggers the service:

```ini
OnCalendar=*-*-* 02:00:00
OnBootSec=5min
```

### Why `Persistent=true` has no effect with OnBootSec / OnUnitActiveSec

`Persistent=true` means "remember when I last fired; if a scheduled time was missed while the machine was off, fire once when it is back" (timestamps are stored under `/var/lib/systemd/timers/`).

That only makes sense for clock-based schedules, which have a specific moment that can be missed.

- `OnCalendar=*-*-* 02:00:00` with `Persistent=true`: PC off at 2 AM, turned on at 8 AM, the job runs at 8 AM.
- `OnBootSec=5min` / `OnUnitActiveSec=`: relative times, recalculated fresh each boot or run, nothing can be "missed". `Persistent=true` is silently ignored.

### OnUnitActiveSec vs OnUnitInactiveSec, and failures

For a service that takes 10 s:

```
OnUnitActiveSec=1min     start--10s--end ........ start   (60 s after previous START)
OnUnitInactiveSec=1min   start--10s--end --60s--- start   (60 s after previous END)
```

`OnUnitInactiveSec` counts from when the service *stopped*, and a **failure also counts as stopped**, so the timer keeps working whether the last run succeeded or failed. Edge cases:

- With `Restart=on-failure`, systemd is still restarting it, so it isn't "stopped" yet; the countdown starts once it finally stops.
- If it fails repeatedly and fast, it can hit the start limit and later starts are refused until `systemctl reset-failed <service>` or the window passes. The timer keeps trying at each interval.

### Creating a timer, step by step

1. **Script that runs once and exits** (`~/hello_once.py`):
   ```python
   from datetime import datetime

   print(f"hello at {datetime.now():%H:%M:%S}", flush=True)
   ```
2. **Service** `/etc/systemd/system/hello-once.service`:
   ```ini
   [Unit]
   Description=Print hello once

   [Service]
   Type=oneshot
   User=YOURUSER
   ExecStart=/usr/bin/python3 /home/YOURUSER/hello_once.py
   ```
   No `[Install]` section is needed; the timer starts it.
3. **Timer** `/etc/systemd/system/hello-once.timer`:
   ```ini
   [Unit]
   Description=Run hello-once every minute

   [Timer]
   OnCalendar=*-*-* *:*:00
   AccuracySec=1s

   [Install]
   WantedBy=timers.target
   ```
4. **Verify and load:**
   ```bash
   systemd-analyze verify /etc/systemd/system/hello-once.service /etc/systemd/system/hello-once.timer
   sudo systemctl daemon-reload
   ```
5. **Enable and start the timer, not the service:**
   ```bash
   sudo systemctl enable --now hello-once.timer
   ```
6. **Check:** `systemctl list-timers`
7. **Logs (from the service):** `journalctl -u hello-once.service -f`

Monotonic example: "2 minutes after boot, then every 10 minutes":

```ini
[Timer]
OnBootSec=2min
OnUnitActiveSec=10min
```

Cleanup:

```bash
sudo systemctl disable --now hello-once.timer
sudo rm /etc/systemd/system/hello-once.{service,timer}
sudo systemctl daemon-reload
```

### Timer without an `[Install]` section

- No `[Install]` means `systemctl enable` has nothing to read, so it warns "The unit files have no installation config" and the timer is **not started at boot**. After a reboot it is inactive and never fires.
- You can still `systemctl start` it; it works until the next reboot or stop.
- It would also run if another unit pulls it in with `Wants=`.
- `WantedBy=timers.target` is a **convention, not a rule**. `WantedBy=multi-user.target` also works. `timers.target` is preferred because it is the "all timers" group reached early in boot, so other units can use `After=timers.target`, and it keeps timers and services tidy.

---

## 8. Target units

A target has **no program and no schedule**; it is a named group of units or a boot milestone. There is no `[Target]` section, only `[Unit]` and usually `[Install]`.

### Keys

| Key | Meaning |
|---|---|
| `Description=` | Name |
| `Wants=` | Soft dependency |
| `Requires=` | Hard dependency |
| `After=` / `Before=` | Ordering |
| `Conflicts=` | Starting me stops these |
| `AllowIsolate=` | `yes` allows `systemctl isolate` to switch to this target |
| `WantedBy=` (in `[Install]`) | Rarely needed for custom targets |

### Real example

```bash
systemctl cat multi-user.target
```

```ini
[Unit]
Description=Multi-User System
Requires=basic.target
Conflicts=rescue.service rescue.target
After=basic.target rescue.service rescue.target
AllowIsolate=yes
```

It does nothing itself; services attach from outside with `WantedBy=multi-user.target`.

### Two ways a group is formed (equivalent)

1. From the target's side: `Wants=a.service b.service` in the target file.
2. From the service's side: `[Install] WantedBy=my.target`; `enable` creates a symlink in `/etc/systemd/system/my.target.wants/`.

### Common targets

| Target | Meaning |
|---|---|
| `multi-user.target` | Normal system, text mode |
| `graphical.target` | Multi-user plus a desktop |
| `network.target` / `network-online.target` | Network configured / actually connected |
| `timers.target` | All timers loaded |
| `rescue.target` | Minimal recovery mode |
| `poweroff.target`, `reboot.target` | Shutdown / reboot |

### Creating your own target

Two services `demo-a.service` and `demo-b.service` (copies of the hello loop), then `/etc/systemd/system/demo.target`:

```ini
[Unit]
Description=Demo group
Wants=demo-a.service demo-b.service
After=demo-a.service demo-b.service
```

```bash
sudo systemctl daemon-reload
sudo systemctl start demo.target
systemctl status demo-a demo-b
systemctl list-dependencies demo.target
```

Starting the target starts both services. Stopping the target does not stop them by default:

```bash
sudo systemctl stop demo-a demo-b demo.target
```

For propagation, add `PartOf=demo.target` in each service's `[Unit]`; then stopping or restarting the target does the same to them.

To start the group at boot, add `[Install] WantedBy=multi-user.target` to the target and `enable` it.

### How boot actually picks targets; making your own target the boot target

At boot systemd starts exactly one target: **`default.target`**, a symlink to a real target (usually `multi-user.target` or `graphical.target`). Everything else starts because it is reachable by dependencies from that one target. A target nothing points to never starts by itself.

Two ways in:

1. **Hang it off an existing target** (`WantedBy=multi-user.target`). The normal choice.
2. **Make it the root** by pointing `default.target` at it. It must itself pull in the normal system, otherwise you boot an almost empty system (no networking, no login, no ssh):

```ini
# /etc/systemd/system/myapp.target
[Unit]
Description=My custom boot target
Requires=multi-user.target
After=multi-user.target
Wants=demo-a.service demo-b.service
AllowIsolate=yes
```

```bash
systemctl get-default                    # note the current value first
sudo systemctl daemon-reload
sudo systemctl set-default myapp.target
ls -l /etc/systemd/system/default.target
```

`set-default` needs no `[Install]` section; it just creates the symlink. Revert with `sudo systemctl set-default multi-user.target` (or whatever `get-default` showed before).

On WSL with `systemd=true`, systemd really is PID 1 and honours `default.target`, but a broken default is harder to recover from because there is no bootloader or rescue menu. Because the target above requires `multi-user.target` it is reasonably safe. Recover with `wsl -u root` from PowerShell.

`systemctl isolate <target>` stops everything not part of that target; avoid it on WSL.

---

## 9. Controlling units with systemctl

```bash
systemctl start ssh         # start now
systemctl stop ssh          # stop
systemctl restart ssh       # stop then start
systemctl reload ssh        # re-read config without stopping (if supported)
systemctl status ssh        # state + last log lines
systemctl enable ssh        # start at boot (reads [Install], creates a symlink)
systemctl disable ssh       # remove that symlink
systemctl enable --now ssh  # enable and start in one go
systemctl is-enabled ssh
systemctl is-active ssh
systemctl cat ssh           # show the unit file(s)
systemctl list-units --type=service
systemctl list-unit-files --type=service
systemctl list-timers
systemctl list-dependencies multi-user.target
systemctl reset-failed ssh
```

### start vs enable vs --now

| Command | Effect | Survives reboot? |
|---|---|---|
| `start` | Activates now | No |
| `enable` | Creates the boot-time symlink from `[Install]`, does not start now | Yes |
| `enable --now` | Both | Yes, and running now |

Timers can be started with `start` like any unit.

### reload vs restart vs daemon-reload

| | restart | reload |
|---|---|---|
| What happens | Stopped then started | Told to re-read its config while running |
| Process | New PID | Same PID |
| Downtime | Brief | Usually none |
| Needs support | Always works | Needs `ExecReload=` or signal handling |

Example: nginx `reload` applies new config without dropping connections. Without `ExecReload=` you get "Job type reload is not applicable"; Python scripts need `restart` unless you build reload in. `systemctl reload-or-restart x` picks whichever works.

| Command | What it reloads |
|---|---|
| `systemctl daemon-reload` | systemd's knowledge of unit **files** (do this after editing one) |
| `systemctl reload x` | the service's own config |
| `systemctl restart x` | the whole service process |

### `systemctl mask`

Masking blocks a unit completely by linking its name to `/dev/null`.

| Command | Effect |
|---|---|
| `disable` | Removes the boot link only; you can still `start` it, and other units can still pull it in |
| `mask` | **Nothing** can start it: not you, not boot, not another unit |
| `unmask` | Removes the block |

```bash
sudo systemctl mask ssh
ls -l /etc/systemd/system/ssh.service     # -> /dev/null
sudo systemctl start ssh                  # Unit ssh.service is masked.
sudo systemctl unmask ssh
```

Used for "this service must never run on this machine" or to stop a dependency that keeps pulling something in. `--runtime` masks only until reboot.

Caution: if `/etc/systemd/system/hello.service` is a real file you created, `mask` refuses; `mask --force` would **overwrite your file** with the link. Don't.

---

## 10. journalctl and the journal

The **journal** is systemd's log store. A service just prints to stdout/stderr; systemd captures it and stores it with extra metadata (timestamp, unit, PID, severity). `systemd-journald` does this, `journalctl` reads it.

- Stored under `/var/log/journal/` (persistent) or `/run/log/journal/` (until reboot), in a **binary format**. `cat` shows garbage; use `journalctl`.
- Everything systemd manages goes into **one shared journal**, tagged by unit. `journalctl -u ssh` just filters by tag.
- Some programs also write their own text logs (nginx under `/var/log/nginx/`), which `cat` and `tail` can read. Their stdout/stderr still reaches the journal too.

### Common commands

```bash
journalctl                       # everything, oldest first (pager; q to quit)
journalctl -e                    # jump to the end
journalctl -n 50                 # last 50 lines
journalctl -f                    # follow live
journalctl -r                    # newest first
journalctl -u ssh                # one unit
journalctl -u ssh -u hello       # several units
journalctl -b                    # since this boot
journalctl -b -1                 # previous boot
journalctl --list-boots
journalctl --since "10 min ago"
journalctl --since "2026-10-25 09:00" --until "2026-10-25 10:00"
journalctl -p err                # errors and worse
journalctl -p warning..err       # a priority range
journalctl -k                    # kernel messages
journalctl -g "timeout"          # built-in pattern search
journalctl --no-pager | grep x   # pipe-friendly output
journalctl -o json-pretty -n 1   # all fields of the latest entry
journalctl _PID=812              # filter by a field
journalctl --disk-usage
```

Priorities, most to least severe: `emerg(0) alert(1) crit(2) err(3) warning(4) notice(5) info(6) debug(7)`. `-p err` shows levels 0 to 3.

### Structure of a log line

```
Oct 25 12:51:03 mypc hello[1204]: hello, count=7
```

| Part | Meaning |
|---|---|
| `Oct 25 12:51:03` | Timestamp |
| `mypc` | Hostname |
| `hello` | Tag identifying the program (syslog identifier; set with `SyslogIdentifier=`) |
| `[1204]` | PID that wrote it |
| `hello, count=7` | The message |

Behind each line, journald stores structured fields (see `journalctl -o json-pretty -n 1`):

| Field | Meaning |
|---|---|
| `MESSAGE` | The text |
| `_SYSTEMD_UNIT` | Source unit |
| `_PID`, `_UID` | Process and user |
| `PRIORITY` | Severity 0-7 |
| `_COMM`, `_EXE` | Command and path |
| `_BOOT_ID` | Which boot |
| `__REALTIME_TIMESTAMP` | Exact time |

Fields starting with `_` are added by journald and cannot be faked by programs. The structure is why `-u`, `-p` and `_PID=` filters are fast.

### What does `-xeu` mean?

Three joined short options:

- `-x`: add **explanatory help text** to certain entries (from a message catalog)
- `-e`: jump to the **end** (newest)
- `-u`: filter by **unit**

`journalctl -xeu ssh` = ssh's log, starting at the newest, with extra explanations. `u` goes last because the unit name must follow it. systemd error messages point you to it: `See "journalctl -xeu ssh.service" for details`.

Quick debug routine for a failing service:

```bash
systemctl status myapp
journalctl -xeu myapp
```

### `-u` when `ssh.service` and `ssh.timer` both exist

A name without a suffix means `.service`, so `journalctl -u ssh` shows only `ssh.service`.

```bash
journalctl -u ssh.timer                       # the timer only
journalctl -u ssh.service -u ssh.timer        # both
journalctl -u 'ssh*'                          # pattern (quote it)
```

A timer logs little ("Started"/"Stopped"); the work's output comes from the **service**, so you usually want `-u name.service`.

---

## 11. Other logging systems

"Journal" is systemd's logging system, not the only one.

- **Classic syslog**: `rsyslog` or `syslog-ng` writes plain text files in `/var/log/` (`syslog`, `auth.log`...). Readable with `cat`, `tail -f`, `grep`. Many Ubuntu/Debian systems run **both** journald and rsyslog.
- **Programs writing their own log files**: nginx, Apache, MySQL, etc.
- **Other init systems** (OpenRC, runit, SysV): no journal; they use syslog and text files.
- **Outside plain Linux**: `docker logs <container>`, `kubectl logs <pod>`, Windows Event Viewer, macOS `log show`.
- **Production setups**: logs shipped from many machines to a central place (Loki, ELK, CloudWatch, Datadog).

Rule of thumb for debugging: `systemctl status <service>`, then `journalctl -u <service>`; if that is not enough, look for the program's own log under `/var/log/`.

---

## 12. Symlinks, hard links and how systemd uses them

A file's data and info live in an **inode**. A file *name* is an entry pointing to an inode.

- **Hard link**: another name pointing to the **same inode**.
- **Soft link (symlink)**: a tiny separate file that **stores a path** to another name. Like a Windows shortcut.

```bash
echo "hello" > original.txt
ln original.txt hard.txt          # hard link
ln -s original.txt soft.txt       # soft link   (ln -s TARGET LINKNAME)
ls -li
```

```
1234 -rw-r--r-- 2 you you 6 ... hard.txt
1234 -rw-r--r-- 2 you you 6 ... original.txt
1240 lrwxrwxrwx 1 you you 12 ... soft.txt -> original.txt
```

`hard.txt` and `original.txt` share inode 1234 with link count 2; `soft.txt` has its own inode and shows `->`.

| | Hard link | Soft link |
|---|---|---|
| Points to | The same inode (the data) | A path (a name) |
| Original name deleted | Other name still works; data lives on | Link **breaks** (dangling) |
| Edit via one name | Visible via both | Visible via both |
| Across filesystems | No | Yes |
| Can link a directory | No | Yes |
| Looks like | An ordinary file, indistinguishable | Clearly a link |

```bash
rm original.txt
cat hard.txt      # still prints "hello"
cat soft.txt      # No such file or directory (broken)
```

Data is freed only when every name (link count 0) is removed.

### Removing links

Both kinds are removed the same way, since you remove only a *name*:

```bash
rm hard.txt
rm soft.txt
unlink soft.txt
```

For a symlink to a directory use `rm mylink` (no trailing slash, no `-r`). Avoid `rm -rf mylink/`, which can reach into the real folder's contents.

Inspect: `ls -l` (leading `l`, `->`), `ls -li` (inode numbers), `readlink -f linkname` (final target).

### Where systemd uses symlinks

1. **`enable`** creates symlinks, e.g. `/etc/systemd/system/multi-user.target.wants/hello.service -> /etc/systemd/system/hello.service`. `disable` removes the link; the unit file is never moved or deleted.
2. **`default.target`** is a symlink to the boot target.
3. **`Alias=`** names are symlinks.
4. **`mask`** links the unit to `/dev/null`.

---

## 13. Edge cases and gotchas

**Unit files**
- Forgot `daemon-reload` after editing a unit file: systemd keeps using the old version.
- Relative path in `ExecStart` (`python app.py`) fails; use full paths.
- Shell features (`|`, `&&`, `~`, `>`) in `ExecStart` do not work without `/bin/bash -c '...'`.
- Forgot `User=`: the service runs as root.
- A service does not activate virtualenvs; call `venv/bin/python` directly.
- `After=` alone does not start the other unit; pair it with `Wants=`/`Requires=`.
- A drop-in **adds** to list-type keys like `ExecStart=`; clear with an empty `ExecStart=` first.
- Editing a package's file in `/usr/lib/...` gets overwritten on update; use `/etc/systemd/system/` or `systemctl edit`.

**Services and Type**
- Script exits immediately with `Type=simple`: systemd sees it finished. Use `oneshot` for run-and-exit scripts.
- Programs that daemonize themselves need `Type=forking`; otherwise systemd kills the child.
- `Type=simple` with a wrong path: `systemctl start` still reports success; use `Type=exec` to catch it.
- `input()` in a service raises `EOFError` (stdin is `/dev/null`); use arguments, environment variables or a config file.
- Missing `flush=True` (or `python -u`) in Python: output appears late or not at all in the journal.
- A service that hits `StartLimitBurst` stays `failed` until `systemctl reset-failed`.
- `reload` fails if the service has no `ExecReload=`; use `restart`.

**Timers**
- Enable the **timer**, not the service.
- The service should run and exit (`oneshot`); the timer does the repeating, not a loop in the script.
- Names must match (`backup.timer` triggers `backup.service`) unless `Unit=` is set.
- `OnUnitActiveSec=`/`OnUnitInactiveSec=` alone never fire; they need a starter (`OnBootSec`, `OnActiveSec`, `OnCalendar`...).
- `Persistent=true` only matters with `OnCalendar`.
- Default `AccuracySec` is 1 minute, so timers may fire up to a minute late; set `AccuracySec=1s` for precision.
- A failed run does not stop a timer from firing again (but repeated fast failures can hit the start limit).
- Timer without `[Install]`: not started at boot.
- On WSL, timers fire only while WSL is running.

**Targets**
- Stopping a target does not stop its services unless they have `PartOf=`.
- A custom default target must require `multi-user.target`, or you boot a nearly empty system.
- `systemctl isolate` stops everything outside the target; avoid on WSL.

**Masking and links**
- `mask --force` overwrites a real unit file you created.
- A masked unit cannot be started by anything, including dependencies.
- Deleting the original of a symlink leaves it broken; hard links survive.

**Logs**
- Journal files are binary; `cat` gives garbage.
- `journalctl -u ssh` means `ssh.service` only.
- `journalctl` on WSL without systemd shows nothing.

---

## 14. Cheat sheet

```bash
# check systemd is running (WSL)
ps -p 1 -o comm=

# create / change a unit
sudo nano /etc/systemd/system/NAME.service
systemd-analyze verify /etc/systemd/system/NAME.service
sudo systemctl daemon-reload
sudo systemctl enable --now NAME

# inspect
systemctl status NAME
systemctl cat NAME
systemctl list-timers
systemctl list-dependencies TARGET

# logs
journalctl -u NAME -f
journalctl -xeu NAME
journalctl -b -p err

# test a calendar expression
systemd-analyze calendar "Mon..Fri *-*-* 18:30"

# undo
sudo systemctl disable --now NAME
sudo rm /etc/systemd/system/NAME.service
sudo systemctl daemon-reload
```

Minimal service:

```ini
[Unit]
Description=My app
After=network.target

[Service]
User=YOURUSER
ExecStart=/usr/bin/python3 /home/YOURUSER/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Minimal timer pair (`x.service` with `Type=oneshot`, plus):

```ini
[Unit]
Description=Run x on a schedule

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Minimal target:

```ini
[Unit]
Description=My group
Wants=a.service b.service
After=a.service b.service
```

---

## 15. Practice exercises

1. `systemctl cat ssh | head -3`: find which folder the unit file comes from.
2. Make `hello.service`, start it, and follow it with `journalctl -u hello -f`.
3. Run the `job.py` experiment (sleep 10 s) with `Type=simple` then `Type=oneshot` and compare how `systemctl start` behaves.
4. Run the `setup`/`app` ordering example with both types and watch `app` fail, then succeed.
5. Run the `launcher.sh` demo with `Type=simple` then `Type=forking`.
6. Point `ExecStart` at a non-existent path with `Type=simple`, then `Type=exec`.
7. Build `hello-once.timer`; run `systemctl list-timers`; try `OnActiveSec=10s` plus `OnUnitActiveSec=30s`.
8. Set only `OnUnitActiveSec=30s` and confirm `NEXT` is empty in `list-timers`; add `OnActiveSec=10s` and see it appear.
9. Remove `[Install]` from the timer, `wsl --shutdown`, reopen, confirm it is inactive; restore `[Install]`, `enable --now`, repeat.
10. Build `demo.target` with two services; test `PartOf=`.
11. Use `sudo systemctl edit hello` to add a drop-in; compare with `systemctl cat hello`; undo with `systemctl revert`.
12. Run `python3 -c "input()" < /dev/null` to see `EOFError`.
13. Create hard and soft links, delete the original, compare.
14. Break a service on purpose and diagnose it with `journalctl -xeu`.

### Suggested mini-project

A Python script run every few minutes by a timer, with its logs read through `journalctl`, and the service and timer grouped under one custom target.
