# 🎬 IMDb Movie Data Analysis

Exploratory data analysis of 1,000 popular movies (2006–2016) using **Python, pandas, seaborn, and matplotlib** — examining rating distributions, genre trends, runtime/revenue relationships, and top directors.

## 📊 Key Findings

- Ratings cluster around **6.7–6.8** on average, reflecting a dataset already filtered to popular/notable releases rather than a random sample.
- **Action, Comedy, and Drama** dominate by volume, but **Biography, Animation, and Crime** tend to earn higher average ratings.
- **Runtime** shows only a weak positive correlation with rating — longer movies aren't reliably better-rated.
- **Revenue and rating are weakly correlated** (r ≈ 0.2) — critical/audience approval doesn't reliably predict box office success.
- **Votes correlate more strongly with rating than revenue does**, suggesting audience engagement tracks quality more closely than earnings do.
- A small group of directors (Christopher Nolan, Damien Chazelle, and others) account for a disproportionate share of the top-rated titles.

## 📁 Repository Structure

```
imdb-movie-analysis/
├── data/
│   └── imdb_movies_dataset.csv       # Raw dataset (1,000 movies, 2006–2016)
├── charts/                           # Generated chart images (PNG)
├── imdb_analysis.py                  # Standalone analysis script
├── IMDb_Movie_Data_Analysis.ipynb    # Jupyter notebook (step-by-step, with output)
├── IMDb_Movie_Data_Analysis_Report.docx  # Full written report
└── README.md
```

## 📦 Dataset

1,000 popular movies released between 2006 and 2016, with the following fields:

| Column | Description |
|---|---|
| Title | Movie title |
| Genre | Comma-separated genre tags |
| Description | Short plot summary |
| Director | Director name |
| Actors | Lead cast |
| Year | Release year |
| Runtime (Minutes) | Runtime |
| Rating | IMDb rating (1–10) |
| Votes | Number of IMDb votes |
| Revenue (Millions) | Box office revenue, USD millions |
| Metascore | Metacritic score |

## 🛠️ Setup & Usage

```bash
git clone https://github.com/<your-username>/imdb-movie-analysis.git
cd imdb-movie-analysis
pip install pandas numpy matplotlib seaborn

# Run the script (regenerates all charts in /charts)
python imdb_analysis.py

# Or explore interactively
jupyter notebook IMDb_Movie_Data_Analysis.ipynb
```

## 📈 Sample Visualizations

| Rating Distribution | Genre vs. Rating | Correlation Matrix |
|---|---|---|
| ![ratings](charts/01_rating_distribution.png) | ![genre](charts/03_avg_rating_by_genre.png) | ![corr](charts/08_correlation_heatmap.png) |

## 🧹 Data Cleaning Notes

- Zero values in `Revenue` and `Metascore` were treated as missing, not literal zero — a movie cannot truly gross $0 or receive a Metascore of 0.
- `Primary_Genre` was derived by taking the first tag from the comma-separated `Genre` field, to simplify genre-level grouping.

## 🔧 Tech Stack

`Python` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `Jupyter`

## 📄 Full Report

See [`IMDb_Movie_Data_Analysis_Report.docx`](./IMDb_Movie_Data_Analysis_Report.docx) for the complete written analysis with all 9 charts and supporting tables.

---
*Dataset originally compiled from IMDb listings; this analysis is for educational/portfolio purposes.*
