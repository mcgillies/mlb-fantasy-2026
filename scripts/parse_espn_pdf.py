"""
Parse ESPN Top 300 Fantasy Baseball PDF to extract player rankings.

Usage:
    pip install pymupdf
    python scripts/parse_espn_pdf.py data/espn/espn_top300.pdf

Output:
    data/espn/espn_rankings_2026.csv
"""

import sys
import os
import re
import pandas as pd

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Install with:")
    print("  pip install pymupdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def parse_rankings(text):
    """
    Parse player rankings from ESPN PDF text with team and position.

    ESPN Top 300 PDF uses a multi-column layout where each entry is:
    RANK. Name
    Team
    Position
    $Value

    Uses a two-pass approach:
    1. Extract all rank + name pairs
    2. Find team and position for each player
    """
    players_dict = {}

    # First pass: Get all players with names
    pattern_name = r'(\d{1,3})\.\s+([A-Za-z][A-Za-z\'\-\.\s]+?)(?=\n)'
    matches_name = re.findall(pattern_name, text)

    for rank_str, name in matches_name:
        rank = int(rank_str)
        name = re.sub(r'\s+', ' ', name.strip())

        # Skip invalid names or duplicates
        if len(name) < 3 or name.isupper() or rank in players_dict or rank > 300:
            continue

        players_dict[rank] = {
            'ESPN_Rank': rank,
            'Name': name,
            'Team': '',
            'Position': ''
        }

    # Second pass: Find team and position for each player
    for rank, player in players_dict.items():
        name = player['Name']
        name_escaped = re.escape(name)
        # Look for: RANK. Name followed by team and position on next lines
        pattern = rf'{rank}\.\s+{name_escaped}\n([A-Z]{{2,3}}|FA)\n([A-Z0-9/]+)'
        match = re.search(pattern, text)
        if match:
            player['Team'] = match.group(1)
            player['Position'] = match.group(2)

    # Fallback: line-by-line parsing if primary pattern failed
    if len(players_dict) < 50:
        print("Standard pattern didn't match well, trying line-by-line parsing...")
        return parse_line_by_line(text)

    return list(players_dict.values())


def parse_line_by_line(text):
    """Fallback: parse text line by line looking for numbered entries."""
    players = []
    lines = text.split('\n')

    current_rank = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Look for lines starting with a number
        match = re.match(r'^(\d{1,3})[\.\s]+(.+)', line)
        if match:
            rank = int(match.group(1))
            rest = match.group(2).strip()

            # Extract name (first part before comma or parenthesis)
            name_match = re.match(r'^([A-Za-z\'\-\.\s]+?)(?:[,\(]|$)', rest)
            if name_match:
                name = name_match.group(1).strip()
                if len(name) >= 3 and rank > current_rank:
                    players.append({
                        'ESPN_Rank': rank,
                        'Name': name,
                        'Position': '',
                        'Team': ''
                    })
                    current_rank = rank

    return players


def main():
    if len(sys.argv) < 2:
        # Look for PDF in data/espn/
        pdf_dir = 'data/espn'
        pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')] if os.path.exists(pdf_dir) else []

        if pdfs:
            pdf_path = os.path.join(pdf_dir, pdfs[0])
            print(f"Found PDF: {pdf_path}")
        else:
            print("Usage: python scripts/parse_espn_pdf.py <path_to_pdf>")
            print("\nOr place the ESPN PDF in data/espn/ and run without arguments.")
            sys.exit(1)
    else:
        pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    print(f"Parsing: {pdf_path}")

    # Extract text
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters")

    # Parse rankings
    players = parse_rankings(text)

    if not players:
        print("Could not parse rankings automatically.")
        print("\nFull extracted text saved to data/espn/espn_pdf_text.txt for manual review.")
        os.makedirs('data/espn', exist_ok=True)
        with open('data/espn/espn_pdf_text.txt', 'w') as f:
            f.write(text)
        sys.exit(1)

    # Create DataFrame
    df = pd.DataFrame(players)
    df = df.drop_duplicates(subset=['ESPN_Rank'], keep='first')
    df = df.sort_values('ESPN_Rank').reset_index(drop=True)

    print(f"\nParsed {len(df)} players")

    # Stats
    with_team = (df['Team'] != '').sum()
    with_pos = (df['Position'] != '').sum()
    print(f"  With team: {with_team}")
    print(f"  With position: {with_pos}")

    print("\nFirst 10:")
    print(df.head(10).to_string(index=False))

    print("\nLast 10:")
    print(df.tail(10).to_string(index=False))

    # Save
    output_path = 'data/espn/espn_rankings_2026.csv'
    os.makedirs('data/espn', exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")

    # Warn if we didn't get 300
    if len(df) < 250:
        print(f"\nWarning: Only found {len(df)} players (expected ~300)")
        print("You may need to manually review/edit the output.")


if __name__ == "__main__":
    main()
