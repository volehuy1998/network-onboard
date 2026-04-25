# Publish Pipeline Scripts

Phase C6a Interim Publish Pipeline — build distributable artifacts từ sdn-onboard curriculum Vietnamese markdown sources.

## Prerequisites

### Ubuntu 22.04+

```bash
sudo apt install -y \
  pandoc \
  texlive-xetex \
  texlive-lang-other \
  texlive-fonts-recommended \
  fonts-noto
```

### macOS

```bash
brew install pandoc basictex
tlmgr install collection-xetex collection-langother
```

## Usage

### Build PDF + EPUB artifact

```bash
bash scripts/build-sdn-pdf.sh [version]
```

Default version string: `v1.0-preVerified`.

Example:

```bash
bash scripts/build-sdn-pdf.sh v1.0-preVerified
# Output:
#   dist/sdn-onboard-v1.0-preVerified.pdf
#   dist/sdn-onboard-v1.0-preVerified.epub
```

### Versioning strategy

- **v1.0-preVerified**: current state, Phase C2-C5 complete, C1b deferred (lab outputs doc-plausible chưa verified-lab). Labeled "Pre-Verified" in title.
- **v2.0-Verified**: after Phase C1b complete (user có lab host + run all exercises). Real lab outputs replace doc-plausible. Labeled "Verified".
- **v2.1+**: future content expansion (Block XIV/XV/XVI skeletons → content, additional advanced case studies).

## Estimated artifact size

Based on 70+ markdown files, ~25,000 lines total content:
- **PDF**: 300-450 pages A4, ~3-5 MB
- **EPUB**: ~1-2 MB

## File ordering logic

Build script orders files as:
1. Block 0 (Entry): `0.0`, `0.1`
2. Block I-XIII (Foundation): `1.*` → `13.*` sorted by version
3. Block XIV-XVI (Expert Extension): `14.*` → `16.*`
4. Block XVII-XIX (Advanced Case Studies): `17.*`, `18.*`, `19.*`

## Known limitations (Phase C6a interim)

1. **Lab outputs chưa verified-lab**: ~45 exercises have doc-plausible CLI output, will be replaced in v2.0 after C1b.
2. **Vietnamese prose polish partial**: Rule 11 first pass complete (paradigm/rebrand/troubleshoot), remaining patterns (approach, deployment, adoption, trade-off) need per-file context review.
3. **Block XIV/XV/XVI skeleton only**: Content phase deferred; PDF includes placeholder sections marked "Skeleton — nội dung sẽ bao gồm".
4. **3 dead URLs fixed in Phase C4**, 379/384 URLs verified OK.

## Rule 9 file integrity

Build script checks null bytes in all markdown inputs before Pandoc. Aborts if any file has null bytes (prevent GitHub render-as-binary issue).

## CI/CD integration (future C6b)

For v2.0 release pipeline, wrap this script in GitHub Actions workflow:

```yaml
# .github/workflows/publish.yml (placeholder, C6b scope)
name: Publish v2.0
on:
  push:
    tags: ['v2.*']
jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt install -y pandoc texlive-xetex texlive-lang-other
      - run: bash scripts/build-sdn-pdf.sh ${{ github.ref_name }}
      - uses: actions/upload-artifact@v4
        with:
          name: sdn-onboard-pdf
          path: dist/*.pdf
```

Not activated in Phase C6a; wait until Phase C1b validates all lab outputs.

## Related tracker files

- `memory/lab-verification-pending.md` — Exercise inventory for C1b
- `plans/sdn-foundation-architecture.md` Phụ lục E — master plan C1-C6b
- `memory/session-log.md` — session history
