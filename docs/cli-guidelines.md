# CLI Guidelines

Define standard options to create a consistent CLI experience across tools.
When developers get used to certain option behavior, having them available
across all tools makes things much easier & smoother.
Conversely, when the same option name is used but with wildly different
meanings, this can be very surprising for developers, and possibly lead them
to do something destructive they didn't intend.

[TOC]

## Required Option Conventions

Tools should adhere to these conventions whenever possible, and any deviation
should be strongly reconsidered.

| Short | Long          | Description |
|:-----:|---------------|-------------|
|       | [--debug]     | Show debugging information. |
| [-f]  | [--force]     | Force an operation. |
| [-h]  | [--help]      | Show tool help/usage output. |
| [-j]  | [--jobs]      | Control parallelization. |
| [-n]  | [--dry-run]   | Show what would be done. |
| [-q]  | [--quiet]     | Quiet(er) output. |
| [-v]  | [--verbose]   | Verbose(r) output. |
|       | [--version]   | Show tool version information. |
| [-y]  | [--yes]       | Skip prompts. |

### --debug {#debug}

Show internal debugging information that the user would find helpful.
This may be very verbose.

[--debug] may be specified multiple times to make the output even debuggier.

The short option [-d] may be used depending on the tool, but usually enabling
extra debugging is not a common operation.

[-d]: #debug
[--debug]: #debug

### --force {#force}

The user wants to bypass any safety checks.
The help text should provide clear guidance on how this will affect behavior
since it can potentially be very dangerous and lead to data loss.

For example, when imaging a device, do not prompt the user whether they really
meant to erase the non-removable `/dev/sda` hard drive.
Or if there are mismatches in hashes or other integrity checks, attempt to do
the operation anyways (installing files, etc...).

Do not confuse this with the [--yes] option for agreeing to common prompts.

The short option [-f] may be used or omitted depending on how dangerous the
option actually is in practice.
If the tool might delete the user's desktop or source, probably safer to make
them type out the full [--force].
If the tool would only delete some temporary files or something that could be
recreated (even if it requires a bit of effort), then [-f] is OK.

[-f]: #force
[--force]: #force

### --help {#help}

Show the tool usage, examples, and other helpful information.
Since the user has explicitly requested the help output, this does not need to
be terse.
Normal output should only go to stdout, and the tool should exit 0.

When processing unknown or invalid options, it's OK to show a short summary of
the specific option, or of valid options, but it should not be the full detailed
output like [--help].
The user should be able to focus on what they got wrong, not wade throw pages of
output to try and track down the one error line.
This output should only go to stderr, and the tool should exit non-zero (either
`1` or `64`).

Use of the short [-h] option is recommended out of wide convention.
Avoid reusing this for something else like `--human`, and definitely never use
it for something destructive or unrecoverable.

[-h]: #help
[--help]: #help

### --jobs {#jobs}

Limit how much parallelism should be used.
This typically translates to how many threads or CPUs to utilize.

The special value `0` should be used to indicate "use all available CPU cores".

The default does not have to always be `1` thus forcing users to manually pick
a value, nor does it have to always be `0`.
Try to balance how expensive a particular job is (network, servers, I/O, RAM,
etc...) with a reasonable default.
For example, when talking to a network service, high values like 72 will
probably cause many connections to be rejected so it won't be overwhelmed, so
find a default that balances real world improvements (compared to `-j1`) with
the server costs.

The default should rarely be hardcoded to a value above 1 -- run it through a
max function with how many cores are available.
For example, the default could be `max(4, os.cpu_count())`.

To determine how many CPU cores are available:
* Python: `os.cpu_count()`
* Shell: `getconf _NPROCESSORS_CONF 2>/dev/null || echo 1`

Use of the short [-j] option is recommended out of wide convention.

[-j]: #jobs
[--jobs]: #jobs

### --dry-run {#dryrun}

Show what would be done, but don't actually "do" anything.
Users should be able to add this option anywhere and expect that the tool will
not make any changes anywhere.
Basically this should always be a harmless idempotent operation.

Use of [--dry-run] is, by itself, not an error, thus it should normally exit 0.
This allows the user to quickly detect problems before trying to make changes.
For example, if invalid options were specified, the tool can show fatal errors.
Or if inputs don't exist, or are corrupt, they may be diagnosed.

The tool may talk to network services, or otherwise make expensive computations,
as long as it doesn't make any changes, and may be rerun many times.

The tool should display what it would have done were [--dry-run] not specified.
This will often take the form like `Would have run command: git push ...`.

Bypassing reasonable prompts is permitted as long as no changes are made.
In other words, this may behave like [--yes] or [--force] in some situations.
Use your best judgment as to what constitutes the best user experience.

Use of the short [-n] option is recommended out of wide convention, and because
use of dry-run first is a common user flow.

The [--dryrun] option should be accepted as an alias to [--dry-run], but should
be omitted from documentation (i.e. [--help] output).
This helps users who typo things, and because some tools have adopted one that
convention instead of [--dry-run] (although the latter is still more common).

[-n]: #dryrun
[--dry-run]: #dryrun
[--dryrun]: #dryrun

### --quiet {#quiet}

Make the output less verbose.
General information should be omitted, and only display warnings or errors.

[--quiet] may be specified multiple times to make the output even quieter.
Some recommended settings:
* *default*: Show important events, warnings, and worse.
* `-q`: Only show warnings and worse.
* `-qq`: Only show (fatal) errors and worse.
* `-qqq`: Don't show any output -- rely on exit status to indicate pass/fail.

Use of the short [-q] option is recommended out of wide convention.

If desired, [--silent] may be used as an alias to `-qqq` behavior; i.e. do not
emit any output, only exit 0/non-zero.

[-q]: #quiet
[--quiet]: #quiet
[--silent]: #quiet

### --verbose

Make the output more verbose.
This may include some helpful info or progress steps.
Important information for the user should not be hidden behind [--verbose];
i.e. users should not be expected to use [--verbose] all the time.

[--verbose] may be specified multiple times to make the output even verboser.

Debugging information should not be included here -- use [--debug] instead.
Use your best judgement as to what is verbose output and what is debug output.

Use of the short [-v] option is recommended out of wide convention, and because
it can be common to type `-vvv` to quickly get more verbose output when trying
to track down problems.

[-v]: #verbose
[--verbose]: #verbose

### --version {#version}

Show version information for the current tool.
Normal output should only go to stdout, and the tool should exit 0.

The default output should be short & to the point, and cheap to produce.
This may include terse authorship information if desired.

If combined with [--verbose], related package/tool information may be included.

If combined with [--quiet], the output should be just the version number.

For example, common output might look like:
```
$ tool --version
CrOS tool v1.2.3
Written by some decent engineers.

$ tool --version --quiet
1.2.3

$ tool --version --verbose
CrOS tool v1.2.3
Current git repo is at add119cea9ebfd7ba89f7606ed04cac7cacaa43d.

Some important library information:
  foo lib v2
  another lib v3.4

Written by some decent engineers.
```

No short option should be provided for [--version].
It's not a common operation, so allocating one of the limited short options
is a waste.

[--version]: #version

### --yes {#yes}

The user wants to "agree" to any standard prompts shown by the tool.
This should not be used by itself to bypass safety checks -- see [--force]
instead, with which this can be combined.

The prompts that would have been shown should still be emitted so it's clear
what the user has agreed to, and include fake input.  For example:
```
$ do-something --yes
Do you want to do something? (Y/n) <yes>
```

Use of the short [-y] option is recommended out of wide convention, and because
skipping the same set of prompts is a common flow to avoid annoying users.

[-y]: #yes
[--yes]: #yes
