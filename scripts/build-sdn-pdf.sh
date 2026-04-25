#!/bin/bash
# Build SDN curriculum PDF via Pandoc
#
# Phase C6a Interim Publish Pipeline (v1.0 pre-verified)
# Output: dist/sdn-onboard-v1.0-preVerified.pdf + .epub
# Status: pre-verified — lab outputs still doc-plausible, replaced với
#         real output sau Phase C1b (lab host available)
#
# Prerequisites:
#   sudo apt install pandoc texlive-xetex texlive-lang-other fonts-noto
# Or on macOS:
#   brew install pandoc basictex && tlmgr install collection-xetex collection-langother
#
# Usage:
#   bash scripts/build-sdn-pdf.sh [version]
#
# Default version = v1.0-preVerified if unset.

set -euo pipefail

VERSION="${1:-v1.0-preVerified}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$REPO_ROOT/sdn-onboard"
DIST_DIR="$REPO_ROOT/dist"

mkdir -p "$DIST_DIR"

# Build ordered file list: Block 0-XIII foundation + XIV-XVI extension + XVII-XIX advanced
cd "$SRC_DIR"

FILES=(
  "0.0 - how-to-read-this-series.md"
  "0.1 - lab-environment-setup.md"
)

# Add foundation files (Block I-XIII) in order
for block in 1 2 3 4 5 6 7 8 9 10 11 12 13; do
  for f in $(ls "$block."*.md 2>/dev/null | sort -V); do
    FILES+=("$f")
  done
done

# Add expert extension (Block XIV-XVI)
for block in 14 15 16; do
  for f in $(ls "$block."*.md 2>/dev/null | sort -V); do
    FILES+=("$f")
  done
done

# Add advanced case studies (Block XVII-XIX)
for block in 17 18 19; do
  for f in $(ls "$block."*.md 2>/dev/null | sort -V); do
    FILES+=("$f")
  done
done

echo "Building $VERSION with ${#FILES[@]} source files..."

# Pandoc metadata + options
cat > /tmp/sdn-metadata.yml << EOF
---
title: "SDN Onboard Curriculum"
subtitle: "OVS + OpenFlow + OVN — portable primitives"
author: "VO LE"
date: "2026-04-22"
lang: vi
documentclass: book
toc: true
toc-depth: 3
numbersections: true
---
EOF

# Build PDF with XeLaTeX for Vietnamese support
pandoc \
  --from=markdown \
  --to=pdf \
  --pdf-engine=xelatex \
  --variable=mainfont:"Noto Serif" \
  --variable=sansfont:"Noto Sans" \
  --variable=monofont:"Noto Sans Mono" \
  --variable=geometry:margin=2cm \
  --variable=papersize:a4 \
  --variable=colorlinks:true \
  --variable=linkcolor:blue \
  --variable=toccolor:blue \
  --metadata-file=/tmp/sdn-metadata.yml \
  --output="$DIST_DIR/sdn-onboard-$VERSION.pdf" \
  "${FILES[@]}"

echo "PDF: $DIST_DIR/sdn-onboard-$VERSION.pdf"

# Build EPUB
pandoc \
  --from=markdown \
  --to=epub3 \
  --metadata-file=/tmp/sdn-metadata.yml \
  --toc --toc-depth=3 \
  --output="$DIST_DIR/sdn-onboard-$VERSION.epub" \
  "${FILES[@]}"

echo "EPUB: $DIST_DIR/sdn-onboard-$VERSION.epub"

# Rule 9: verify output has no null bytes (PDF/EPUB are binary, skip — check markdown input)
for f in "${FILES[@]}"; do
  count=$(python3 -c "print(open('$f','rb').read().count(b'\x00'))" 2>/dev/null || \
          py -c "print(open('$f','rb').read().count(b'\x00'))")
  if [ "$count" != "0" ]; then
    echo "ERROR: $f has $count null bytes — aborting before publish"
    exit 1
  fi
done

echo "Build complete: $VERSION"
echo "Output artifacts:"
ls -lh "$DIST_DIR/sdn-onboard-$VERSION".{pdf,epub}
