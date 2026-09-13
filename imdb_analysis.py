import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11

df = pd.read_csv('data/IMDB-Movie-Data.csv')
df.columns = [c.strip() for c in df.columns]
df.rename(columns={'Runtime (Minutes)':'Runtime','Revenue (Millions)':'Revenue'}, inplace=True)

# ---- basic cleaning ----
df['Revenue'] = df['Revenue'].replace(0, np.nan)  # some 0 revenue likely missing/unreported
df['Metascore'] = df['Metascore'].replace(0, np.nan)
df['Primary_Genre'] = df['Genre'].apply(lambda x: x.split(',')[0])

print("Rows, Cols:", df.shape)
print(df.describe(include='all').T[['count','mean','min','max']] if False else "")

# ---- Key summary stats ----
summary = {
    'n_movies': len(df),
    'year_range': (int(df.Year.min()), int(df.Year.max())),
    'avg_rating': round(df.Rating.mean(),2),
    'median_rating': round(df.Rating.median(),2),
    'avg_runtime': round(df.Runtime.mean(),1),
    'avg_revenue_M': round(df.Revenue.mean(skipna=True),1),
    'missing_revenue': int(df.Revenue.isna().sum()),
    'missing_metascore': int(df.Metascore.isna().sum()),
    'n_unique_directors': df.Director.nunique(),
    'top_genre': df.Primary_Genre.value_counts().idxmax(),
}
import json
print(json.dumps(summary, indent=2))
with open('scripts/summary.json','w') as f:
    json.dump(summary, f, indent=2)

# ============ CHART 1: Rating distribution ============
fig, ax = plt.subplots(figsize=(7,4.5))
sns.histplot(df['Rating'], bins=25, kde=True, color='#2E5090', ax=ax)
ax.axvline(df['Rating'].mean(), color='#D64545', linestyle='--', linewidth=1.5, label=f"Mean = {df['Rating'].mean():.2f}")
ax.set_title('Distribution of IMDb Ratings', fontsize=13, fontweight='bold')
ax.set_xlabel('IMDb Rating')
ax.set_ylabel('Number of Movies')
ax.legend()
plt.tight_layout()
plt.savefig('charts/01_rating_distribution.png')
plt.close()

# ============ CHART 2: Top genres by count ============
genre_counts = df['Primary_Genre'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(7,4.5))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis', ax=ax)
ax.set_title('Top 10 Primary Genres by Number of Movies', fontsize=13, fontweight='bold')
ax.set_xlabel('Number of Movies')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('charts/02_top_genres_count.png')
plt.close()

# ============ CHART 3: Avg rating by genre (min 15 movies) ============
genre_stats = df.groupby('Primary_Genre').agg(count=('Rating','size'), avg_rating=('Rating','mean')).query('count>=15').sort_values('avg_rating', ascending=False)
fig, ax = plt.subplots(figsize=(7,4.5))
sns.barplot(x=genre_stats['avg_rating'], y=genre_stats.index, palette='mako', ax=ax)
ax.set_title('Average Rating by Genre (genres with 15+ movies)', fontsize=13, fontweight='bold')
ax.set_xlabel('Average IMDb Rating')
ax.set_ylabel('')
ax.set_xlim(5.5, 8)
plt.tight_layout()
plt.savefig('charts/03_avg_rating_by_genre.png')
plt.close()

# ============ CHART 4: Ratings trend over years ============
yearly = df.groupby('Year').agg(avg_rating=('Rating','mean'), n=('Rating','size')).reset_index()
fig, ax = plt.subplots(figsize=(7,4.5))
sns.lineplot(data=yearly, x='Year', y='avg_rating', marker='o', color='#2E5090', ax=ax)
ax.set_title('Average IMDb Rating by Release Year (2006–2016)', fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Average Rating')
plt.tight_layout()
plt.savefig('charts/04_rating_trend_by_year.png')
plt.close()

# ============ CHART 5: Movies released per year ============
fig, ax = plt.subplots(figsize=(7,4.5))
sns.barplot(x=yearly['Year'], y=yearly['n'], color='#4C7FB0', ax=ax)
ax.set_title('Number of Movies Released per Year', fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Movies')
plt.tight_layout()
plt.savefig('charts/05_movies_per_year.png')
plt.close()

# ============ CHART 6: Runtime vs Rating scatter ============
fig, ax = plt.subplots(figsize=(7,4.5))
sns.scatterplot(data=df, x='Runtime', y='Rating', alpha=0.5, color='#2E5090', ax=ax)
sns.regplot(data=df, x='Runtime', y='Rating', scatter=False, color='#D64545', ax=ax)
ax.set_title('Runtime vs. IMDb Rating', fontsize=13, fontweight='bold')
ax.set_xlabel('Runtime (Minutes)')
ax.set_ylabel('IMDb Rating')
plt.tight_layout()
plt.savefig('charts/06_runtime_vs_rating.png')
plt.close()

# ============ CHART 7: Revenue vs Rating scatter ============
fig, ax = plt.subplots(figsize=(7,4.5))
sub = df.dropna(subset=['Revenue'])
sns.scatterplot(data=sub, x='Rating', y='Revenue', alpha=0.5, color='#2E5090', ax=ax)
ax.set_title('IMDb Rating vs. Box Office Revenue', fontsize=13, fontweight='bold')
ax.set_xlabel('IMDb Rating')
ax.set_ylabel('Revenue ($ Millions)')
plt.tight_layout()
plt.savefig('charts/07_revenue_vs_rating.png')
plt.close()

# ============ CHART 8: Correlation heatmap ============
num_cols = ['Rating','Votes','Revenue','Metascore','Runtime','Year']
corr = df[num_cols].corr()
fig, ax = plt.subplots(figsize=(6,5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1, ax=ax, square=True)
ax.set_title('Correlation Matrix of Key Numeric Features', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/08_correlation_heatmap.png')
plt.close()

# ============ CHART 9: Top 10 directors by avg rating (min 3 movies) ============
dir_stats = df.groupby('Director').agg(count=('Rating','size'), avg_rating=('Rating','mean')).query('count>=3').sort_values('avg_rating', ascending=False).head(10)
fig, ax = plt.subplots(figsize=(7,4.5))
sns.barplot(x=dir_stats['avg_rating'], y=dir_stats.index, palette='crest', ax=ax)
ax.set_title('Top 10 Directors by Average Rating (3+ movies)', fontsize=13, fontweight='bold')
ax.set_xlabel('Average IMDb Rating')
ax.set_ylabel('')
ax.set_xlim(6, 9)
plt.tight_layout()
plt.savefig('charts/09_top_directors.png')
plt.close()

print("\nAll charts saved.")

# Extra tables for the report
top10_rated = df.sort_values('Rating', ascending=False)[['Title','Year','Rating','Votes','Director']].head(10)
top10_rated.to_csv('scripts/top10_rated.csv', index=False)

top10_revenue = df.sort_values('Revenue', ascending=False)[['Title','Year','Revenue','Rating']].head(10)
top10_revenue.to_csv('scripts/top10_revenue.csv', index=False)

print(top10_rated.to_string(index=False))
print()
print(top10_revenue.to_string(index=False))
