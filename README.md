# 📊 Codeforces Div. 2 Contest Analyzer

A small Python project that analyzes recent **Codeforces Div. 2 contests** and visualizes:

- 📈 Problem rating distributions (A → F)
- 🏷️ Most common problem tags per difficulty level

It pulls live data directly from the Codeforces API and generates clean visual summaries to help you understand difficulty trends and topic frequency.

---

## ✨ What this project does

This script:

- Fetches contest data from the Codeforces API
- Filters the most recent **Div. 2 contests**
- Groups problems by index (A, B, C, D, E, F)
- Merges variants like `C1`, `C2` → `C`
- Analyzes problem ratings
- Counts tag frequency per problem level
- Generates plots automatically

Perfect if you want to understand:

- How hard each problem level usually is
- Which topics appear most often
- Trends across recent contests

---

## 🧠 How it works (quick overview)

1. Fetch contest list
2. Select last **N Div. 2 contests** (default: 200)
3. Fetch full problemset
4. Extract ratings + tags
5. Build statistics using pandas
6. Generate visualizations using matplotlib + seaborn

---

## 📦 Requirements

Install dependencies:

```bash
pip install pandas matplotlib seaborn requests
```

Python 3.8+ recommended.

---

## ▶️ Usage

Just run:

```bash
python main.py
```

(The filename can be anything — just run the script.)

The script will:

- Fetch data from Codeforces
- Print rating summaries in the terminal
- Generate plots in the project folder

---

## ⚙️ Configuration

Inside the script:

```python
CONTEST_COUNT = 200
```

Change this value to analyze more or fewer contests.

Example:

```python
CONTEST_COUNT = 100
```

---

## 📊 Output

### 1️⃣ Rating Distribution

Creates:

```
div2_ratings_200.png
```

A boxplot showing rating ranges for problems A–F across recent contests.

---

### 2️⃣ Tag Analysis

Creates:

```
div2_tags_200.png
```

Shows the most common tags for each problem level.

Also prints a **Top 10 tags list** in the terminal.

---

## 📝 Example Insights You Can Get

- Typical rating jump from B → C → D problems
- Most common C/D problem topics
- How consistent difficulty levels are across contests

---

## ⚠️ Notes

- Uses live Codeforces API data — internet connection required.
- First run may take a few seconds due to API requests.
- Plots are saved using a non-GUI backend (`Agg`), so it works on servers and WSL too.

---

## 🚀 Ideas for future improvements

- User rating progression analysis
- Interactive dashboards (Plotly)
- Per-tag difficulty trends
- Contest comparison over time

---

## 🙌 Why this exists

Built as a small data exploration tool for competitive programmers curious about how Codeforces problems evolve over time.

If you find it useful, feel free to fork and experiment.

Happy coding 🚀
