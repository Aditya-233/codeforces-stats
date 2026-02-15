from collections import Counter

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns

matplotlib.use("Agg")

# --- CONFIGURATION ---
CONTEST_COUNT = 200  # Analyzes last 200 Div. 2 contests
# ---------------------


def get_contest_data():
    print("Fetching data from Codeforces API...")

    # 1. Get all contests
    try:
        contests_url = "https://codeforces.com/api/contest.list"
        contests_data = requests.get(contests_url).json()
        if contests_data["status"] != "OK":
            print("Error fetching contests")
            return None, None
    except Exception as e:
        print(f"Connection error: {e}")
        return None, None

    # Filter for 'Div. 2' and finished contests
    all_contests = contests_data["result"]
    div2_contests = [
        c for c in all_contests if "Div. 2" in c["name"] and c["phase"] == "FINISHED"
    ]

    # Sort by ID (newest first) and take the target count
    div2_contests.sort(key=lambda x: x["id"], reverse=True)
    target_contests = div2_contests[:CONTEST_COUNT]
    target_ids = set(c["id"] for c in target_contests)

    print(f"Analyzing {len(target_contests)} recent Div. 2 contests...")

    # 2. Get all problems
    try:
        problems_url = "https://codeforces.com/api/problemset.problems"
        problems_data = requests.get(problems_url).json()
        if problems_data["status"] != "OK":
            print("Error fetching problems")
            return None, None
    except Exception as e:
        print(f"Connection error: {e}")
        return None, None

    problems = problems_data["result"]["problems"]

    rating_data = []
    tag_stats = {key: Counter() for key in ["A", "B", "C", "D", "E", "F"]}

    for p in problems:
        if p.get("contestId") in target_ids:
            if "index" in p:
                # GROUPING LOGIC: Take first character only.
                # 'C1' -> 'C', 'C2' -> 'C', 'D1' -> 'D'
                clean_index = p["index"][0]

                if clean_index in ["A", "B", "C", "D", "E", "F"]:
                    # Collect Rating Data
                    if "rating" in p:
                        rating_data.append(
                            {
                                "Contest ID": p["contestId"],
                                "Problem": clean_index,
                                "Rating": p["rating"],
                            }
                        )

                    # Collect Tag Data
                    if "tags" in p:
                        for tag in p["tags"]:
                            tag_stats[clean_index][tag] += 1

    return pd.DataFrame(rating_data), tag_stats


def plot_ratings(df):
    if df is None or df.empty:
        print("No rating data found!")
        return

    order = ["A", "B", "C", "D", "E", "F"]

    print("\n--- Rating Summary (Past 200 Div. 2 Contests) ---")
    summary = df.groupby("Problem")["Rating"].describe()[
        ["count", "mean", "50%", "min", "max"]
    ]
    summary.rename(columns={"50%": "median"}, inplace=True)
    print(summary)

    print("\nGenerating Rating Boxplot...")
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")

    sns.boxplot(
        x="Problem",
        y="Rating",
        data=df,
        order=order,
        hue="Problem",
        palette="Set2",
        showfliers=True,
        legend=False,
    )

    plt.title(
        f"Problem Rating Distribution - Past {CONTEST_COUNT} Div. 2 Contests",
        fontsize=16,
    )
    plt.ylabel("Rating", fontsize=12)
    plt.xlabel("Problem Index (C1/C2 grouped as C)", fontsize=12)
    plt.yticks(range(800, 3600, 200))

    filename = f"div2_ratings_{CONTEST_COUNT}.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print(f"Saved '{filename}'")


def plot_tags(tag_stats):
    if not tag_stats:
        print("No tag data found.")
        return

    levels = ["A", "B", "C", "D", "E", "F"]

    print("\n" + "=" * 50)
    print(f"TOP 10 TAGS PER PROBLEM (Past {CONTEST_COUNT} Div. 2)")
    print("=" * 50)

    # 1. Print Text List
    for level in levels:
        print(f"\n--- Problem {level} ---")
        top_10 = tag_stats[level].most_common(10)
        if not top_10:
            print("  (No tags found)")
        for tag, count in top_10:
            print(f"  {tag:<25} : {count}")

    # 2. Generate Plot
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(
        f"Top 5 Tags by Problem Level (Past {CONTEST_COUNT} Div. 2)", fontsize=16
    )
    axes = axes.flatten()

    for i, level in enumerate(levels):
        ax = axes[i]
        top_5 = tag_stats[level].most_common(5)

        if top_5:
            tags = [x[0] for x in top_5]
            counts = [x[1] for x in top_5]
            sns.barplot(
                x=counts, y=tags, ax=ax, palette="viridis", hue=tags, legend=False
            )
            ax.set_title(f"Problem {level}", fontsize=14)
            ax.set_xlabel("Count")
        else:
            ax.text(0.5, 0.5, "No Data", ha="center")

    plt.tight_layout(rect=(0.0, 0.03, 1.0, 0.95))
    filename = f"div2_tags_{CONTEST_COUNT}.png"
    plt.savefig(filename, dpi=300)
    print(f"\nSaved '{filename}'")


if __name__ == "__main__":
    df, tags = get_contest_data()
    plot_ratings(df)
    plot_tags(tags)
