# Chess Games Analysis Pipeline

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

---

## Stage 1 — Load & Profile

| Q   | Question                  | Answer                                      |
| --- | ------------------------- | ------------------------------------------- |
| Q1  | Total records             | **20,058**                                  |
| Q2  | Exact duplicate rows      | **0**                                       |
| Q3  | Duplicate move sequences  | **1,138**                                   |
| Q4  | opening_response missing  | **93.98%**                                  |
| Q5  | opening_variation missing | **28.22%**                                  |
| Q6  | Minimum turns             | **1** suspicious — real game needs ≥2 turns |

---

## Stage 2 — Clean Pipeline

| Step | Action                 | Result                           |
| ---- | ---------------------- | -------------------------------- |
| 2a   | Parse time_increment   | time_base + time_inc added       |
| 2b   | Add rating_diff        | white_rating − black_rating      |
| 2c   | Extract opening_family | from opening_fullname before `:` |
| 2d   | Drop opening_code      | 93.98% null — removed            |
| 2e   | Flag suspicious games  | turns < 5 → is_suspicious        |
| 2f   | Validate               | no nulls · no duplicates         |

---

## Stage 3 — Analytical Questions

### Q10 — Win Rates

| Winner | %      |
| ------ | ------ |
| White  | 49.86% |
| Black  | 45.40% |
| Draw   | 4.74%  |

### Q11 — Most Common Victory Status

> **Resign** is how most games end (55.6%)

### Q12 — Average Turns by Victory Status

| Status      | Avg Turns |
| ----------- | --------- |
| Draw        | 83.8      |
| Out of Time | 72.7      |
| Mate        | 65.4      |
| Resign      | 53.9      |

### Q13 — Most Popular Opening Family

| Winner     | Opening                       |
| ---------- | ----------------------------- |
| White wins | Sicilian Defense (1,173 wins) |
| Black wins | Sicilian Defense (1,273 wins) |

### Q14 — White Win Rate: Rated vs Unrated

| Type    | White Win Rate |
| ------- | -------------- |
| Rated   | 49.84%         |
| Unrated | 49.94%         |

### Q15 — Game Length Distribution

| Length | Turns   | %      |
| ------ | ------- | ------ |
| Short  | < 20    | 8.28%  |
| Medium | 20 – 70 | 58.65% |
| Long   | ≥ 70    | 33.06% |

---

## Stage 4 — Merge, Resolve Conflicts & Plot

| Q   | Question                             | Answer                                    |
| --- | ------------------------------------ | ----------------------------------------- |
| Q16 | White players with no registry entry | **9,238**                                 |
| Q17 | Country name inconsistencies         | **10 forms → 7 clean countries**          |
| Q18 | Win counts by color                  | White: 10,001 · Black: 9,107 · Draw: 950  |
| Q19 | white_rating vs turns                | Higher-rated games not necessarily longer |

### Plots

![Win Counts by Color](output/wins_by_color.png)
![White Rating vs Turns](output/rating_vs_turns.png)

---

## Key Takeaways

- **White has a slight advantage** — wins ~4.5% more than Black
- **Most players resign** rather than play to checkmate
- **Draw games are the longest** — averaging 83.8 turns
- **Sicilian Defense dominates** regardless of who wins
- **Rating doesn't determine game length**
