# Open vSwitch lab transcripts

This directory holds the verbatim record of every hands-on lab session executed under plan v3.13. Each lab session produces three files: a raw byte-stream typescript captured by `script -f -t` on the lab host, a per-byte timing log captured alongside, and a rendered Markdown curriculum file that wraps the transcript with pedagogical commentary. The typescript is the evidence; the Markdown is the commentary on the evidence.

For the full plan v3.13 specification, see [`plans/sdn/v3.13-ovs-hands-on-mastery-and-source-deep-dive.md`](../../plans/sdn/v3.13-ovs-hands-on-mastery-and-source-deep-dive.md).

## Verbatim integrity policy

Per CLAUDE.md Rule 18, every artefact captured from a lab host appears in this directory exactly as it appeared on the host. Not a single character is modified, omitted, or rewritten. The shell prompt `root@lab-openvswitch:~#` is preserved exactly, lab IPs are not anonymised, MAC addresses and UUIDs are preserved character for character, log timestamps are preserved to the millisecond.

Long output that would be unreadable inline (typically anything over about 200 lines) is referenced by the Markdown file rather than embedded; the full byte stream is always present in the corresponding typescript file. Where the Markdown rendering omits intermediate lines, the omission is marked explicitly with `[N other lines omitted, context: ...]` so a reader can always reconstruct what was dropped and why.

The pre-commit hook [`scripts/lab_verbatim_check.py`](../../scripts/lab_verbatim_check.py) enforces these invariants automatically. Every line of every fenced code block in a Markdown transcript under this directory must appear as a substring of some line in the referenced typescript file, after stripping ANSI Control Sequence Introducer escapes, Operating System Command escapes, and the `Script started` and `Script done` banner lines. Anonymised IPs, shortened UUIDs, rewritten prompts, and rounded timestamps all break the substring match and reject the commit.

## File naming convention

For each lab sprint `R<N>` of plan v3.13:

- `v3.13-R<N>-<topic>.md` is the rendered curriculum transcript. Read this first.
- `v3.13-R<N>-<topic>.typescript` is the raw byte stream from `script -f`. Open this when the rendering raises a question that the verbatim record would settle.
- `v3.13-R<N>-<topic>.timing` is the per-byte timing log from `script -t`. Used by `scriptreplay v3.13-R<N>-<topic>.timing v3.13-R<N>-<topic>.typescript` to replay the session at original speed.

Provisioning and snapshot transcripts that are not tied to a specific R-sprint live under `sdn-onboard/labs/v3.13-provisioning/`. See [`v3.13-provisioning/README.md`](v3.13-provisioning/README.md) once that directory is created.

## How to read a transcript

Open the `.md` file. The header block names the typescript and timing files, the capture window, and the host. Read the "Why this transcript exists" section to understand what the sprint is establishing. Each subsequent section pairs one logical group of commands with a fenced code block of the verbatim host output and a short pedagogical commentary.

The fenced blocks use the `text` info string and contain only output that is byte-identical to the typescript. The surrounding prose is plain English and is the only place where the author has any editorial latitude. If you need the absolute byte stream (every CR, every escape, every interleaved prompt redraw), open the typescript directly in a hex viewer.

## Capture conventions for new transcripts

When capturing a new lab session under plan v3.13, follow these conventions so the verbatim record stays clean and an experienced operator could reproduce the session by retyping the commands:

1. **No synthetic structure inside fenced blocks.** Per CLAUDE.md Rule 18 practice 8, every fenced code block in a curriculum-side lab `.md` contains only real operator commands and the real host output those commands produce. The following are forbidden inside any fenced block: `echo === ... ===` start-and-end banners, `echo --- ... ---` mid-session section banners, any `echo` whose only purpose is to print a section title, and `# <section title>` shell-comment label lines. Section structure lives in surrounding prose: H2 / H3 headings introduce each phase, and plain paragraphs explain the why and the what.
2. **Run only commands an operator would actually type.** If a step is just narration, drop it from the orchestrator entirely and explain it in the surrounding prose. The typescript records a real lab session, not a guided tour.
3. **Set `TERM=xterm-256color` and `tmux new-session -x 200 -y 50`** so output formatting (`lscpu`, `systemctl`, `dmesg`) does not wrap awkwardly and the typescript stays readable after `lab_verbatim_check.py` strips ANSI and OSC escapes.
4. **Capture every command's exit status implicitly through the prompt.** If a command's exit status matters explicitly, follow it with `echo "rc=$?"` so the rendered `.md` can cite the status without recomputing.

**No grandfather clause.** Earlier transcripts (R0 baseline, R1.A apt-distro-install) were captured before practice 8 was codified and originally contained `echo === ... ===` and `echo --- ... ---` banners inside their fenced blocks. The owner directive of 2026-04-29 ("Use words to explain instead of this stuff") retracted the prior R1.A grandfather and applied the rule retroactively to every lab `.md`. The fix is `.md`-only: every banner-and-echo line pair was removed from the curriculum file and replaced with a prose paragraph above the affected fenced block. The typescript files themselves were not modified, because the typescript is the verbatim historical record of what actually ran on the lab host. `lab_verbatim_check.py` is unaffected by the trim: it fails only when an `.md` line is missing from the typescript, never when the `.md` is shorter than the typescript.

## Available transcripts

| Transcript | Sprint | Topic | Capture window |
|------------|--------|-------|----------------|
| [`v3.13-R0-baseline.md`](v3.13-R0-baseline.md) | R0 | Green-field baseline of `lab-openvswitch` (Ubuntu 22.04.5, kernel 5.15.0-173, two NICs, no Open vSwitch installed) | 2026-04-29 15:57 to 15:59 UTC |
| [`v3.13-R1A-apt-distro-install.md`](v3.13-R1A-apt-distro-install.md) | R1.A | Open vSwitch install path A: Ubuntu distro package via `apt-get install openvswitch-switch`. Install, verify, purge, observe residual state. | 2026-04-29 17:13 to 17:16 UTC |

Future R-sprints add their entries here as they close.

## Pedagogical sidebars

Plan v3.13 §R0.1 specifies a permanent pedagogical sidebar titled "Why most OVS labs use network namespaces instead of virtual machines" intended to live in this README. The sidebar answers the most common newcomer question on first encounter with an Open vSwitch tutorial: why are there no virtual machines in the topology when OpenStack and similar cloud platforms always show VMs.

The sidebar is queued as a separate authoring task and is not yet present in this file. It will appear as a top-level section here once authored, and a one-paragraph callout will be cross-referenced from `sdn-onboard/0.1 - lab-environment-setup.md` so a learner following the curriculum reading order encounters it at the moment the lab convention is introduced.

## Cross-references

- CLAUDE.md Rule 18 governs the verbatim-integrity policy enforced here.
- CLAUDE.md Rule 7 and Rule 7a govern terminal output fidelity and system-log absolute integrity, both of which Rule 18 extends.
- [`memory/shared/file-dependency-map.md`](../../memory/shared/file-dependency-map.md) Tier 6 records the dependency between each Markdown transcript and its raw typescript file.
- [`scripts/lab_verbatim_check.py`](../../scripts/lab_verbatim_check.py) and its [test suite](../../scripts/tests/test_lab_verbatim_check.py) implement the pre-commit gate.
