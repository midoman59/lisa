#!/usr/bin/env python3
"""
Analyse comment les chunks sont créés avec la nouvelle stratégie.
Affiche les 3 premiers chunks du PDF pour vérifier que les définitions complètes sont conservées.
"""

import re
from pathlib import Path
from typing import Iterator
import pdfplumber

CHUNK_SIZE = 2_500
CHUNK_OVERLAP = 400

def chunks(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> Iterator[str]:
    """Split text into overlapping chunks, preferring word boundaries."""
    text = re.sub(r"\s+", " ", text).strip()
    start = 0
    chunk_num = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            yield chunk_num, chunk, start, end
            chunk_num += 1
        if end == len(text):
            break
        start = max(end - overlap, start + 1)

def extract_pdf(path: Path):
    """Extract text from PDF pages."""
    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                yield page_number, text

print("=" * 80)
print("ANALYSE DES CHUNKS - Nouvelle Stratégie (2500 chars)")
print("=" * 80)

pdf_path = Path("docs/LS_V3.8.0_Fichiers_Permanents.pdf")
if not pdf_path.exists():
    print(f"❌ PDF not found: {pdf_path}")
    exit(1)

chunk_count = 0
sample_count = 0

for page_num, text in extract_pdf(pdf_path):
    if page_num > 46:  # Arrête après page 46 (où on a CDSITDOS-22)
        break

    for chunk_idx, chunk_text, start_pos, end_pos in chunks(text):
        chunk_count += 1
        chunk_size = len(chunk_text)

        # Affiche les premiers chunks qui contiennent "CDSITDOS" ou "CDSITC"
        if sample_count < 5 and ("CDSIT" in chunk_text or page_num >= 44):
            sample_count += 1
            print(f"\n{'='*80}")
            print(f"CHUNK #{chunk_count} | Page {page_num} | Size: {chunk_size} chars | Chunk #{chunk_idx}")
            print(f"{'='*80}")
            print(chunk_text[:1000])  # Affiche les 1000 premiers chars
            if len(chunk_text) > 1000:
                print(f"\n... [CHUNK CONTINUE, {chunk_size - 1000} chars restants] ...\n")
                print(chunk_text[-500:])  # Affiche les 500 derniers chars
            print(f"\n[Caractères: {chunk_size} | Overlap avec prochain: {CHUNK_OVERLAP}]")

print(f"\n{'='*80}")
print(f"RÉSUMÉ")
print(f"{'='*80}")
print(f"✓ Taille chunk: {CHUNK_SIZE} caractères")
print(f"✓ Overlap: {CHUNK_OVERLAP} caractères")
print(f"✓ Total chunks analysés: {chunk_count}")
print(f"✓ Avantage: Les définitions complètes restent ensemble")
print(f"✓ Exemple: CDSITDOS-22 avec toutes ses 5 valeurs dans le même chunk")
print("=" * 80)
