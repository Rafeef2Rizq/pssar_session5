## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install pandas matplotlib numpy
```

## Run

```bash
python index1.py
```

## Pipeline Stages

| Stage | Description                     |
| ----- | ------------------------------- |
| 1     | Load & profile raw data         |
| 2     | Clean & engineer features       |
| 3     | Analyse & answer questions      |
| 4     | Merge, resolve conflicts & plot |

## Key Findings

### Win Rates

{chr(10).join(f"- **{k}**: {v:.2f}%" for k, v in win_rates.items())}

### Victory Status

- Most common: **{df['victory_status'].value_counts().idxmax()}**
  {chr(10).join(f"- {s}: {t:.1f} avg turns" for s, t in avg_turns.items())}

### Openings

{chr(10).join(f"- **{pos} wins** → {df[df['winner']==pos]['opening_family'].value_counts().idxmax()}" for pos in ['white','black'])}

### Rated vs Unrated

{chr(10).join(f"- **{label}**: {val:.2f}%" for label, val in q14.items())}

### Game Length

{chr(10).join(f"- **{label}**: {pct:.2f}%" for label, pct in length_pct.items())}

## Plots

![Win Counts by Color](output/wins_by_color.png)
![White Rating vs Turns](output/rating_vs_turns.png)
"""

    with open(f'{output_dir}/README.md', 'w', encoding='utf-8') as f:
        f.write(md)
    print("✅ Saved → README.md")
