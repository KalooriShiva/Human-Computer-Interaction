import csv
import time
import random
from scholarly import scholarly

# -------------------------------
# Step 1: Define Keywords
# -------------------------------
keywords = [
    "automatic text simplification dyslexia",
    "text simplification ADHD education AI",
    "Hindi text simplification accessibility",
    "cognitive accessibility sentence simplification school curriculum",
    "multilingual text simplification education technology disabilities",
    "text-to-speech cognitive accessibility",
    "AI text simplification with TTS",
    "adaptive learning accessibility NLP",
    "Indian languages educational accessibility AI",
]

# -------------------------------
# Step 2: Function to Collect Papers
# -------------------------------
def search_papers(query, max_results=10, retries=3):
    """Search Google Scholar and return a list of papers for a query"""
    results = []
    attempt = 0

    while attempt < retries:
        try:
            search_query = scholarly.search_pubs(query)
            for i in range(max_results):
                try:
                    paper = next(search_query)
                    results.append({
                        "keyword": query,
                        "title": paper.get("bib", {}).get("title", "N/A"),
                        "authors": paper.get("bib", {}).get("author", "N/A"),
                        "year": paper.get("bib", {}).get("pub_year", "N/A"),
                        "source title": paper.get("bib", {}).get("venue", "N/A"),
                        "DOI": paper.get("bib", {}).get("doi", "N/A"),
                        "link": paper.get("pub_url", "N/A"),
                        "abstract": paper.get("bib", {}).get("abstract", "N/A"),
                        "author keywords": "N/A",
                        "index keywords": "N/A"
                    })
                except StopIteration:
                    break
            return results

        except Exception as e:
            attempt += 1
            wait_time = random.randint(5, 15)
            print(f"⚠️ Error fetching '{query}' (attempt {attempt}/{retries}): {e}")
            print(f"⏳ Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    print(f"❌ Failed to fetch results for '{query}' after {retries} retries.")
    return results

# -------------------------------
# Step 3: Run Search for All Keywords (with duplicate handling)
# -------------------------------
all_results = []
seen = set()  # store unique papers (using DOI or title)

for kw in keywords:
    print(f"\n🔎 Searching for: {kw}")
    papers = search_papers(kw, max_results=10)

    for p in papers:
        # Use DOI if available, otherwise use title as fallback
        identifier = p.get("DOI", "N/A")
        if identifier == "N/A":
            identifier = p.get("title", "").lower().strip()

        if identifier not in seen:
            seen.add(identifier)
            all_results.append(p)
        else:
            print(f"⚠️ Duplicate skipped: {p.get('title')}")

# -------------------------------
# Step 4: Save Results into CSV
# -------------------------------
output_file = "papers.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "keyword", "title", "authors", "year",
            "source title", "DOI", "link",
            "abstract", "author keywords", "index keywords"
        ]
    )
    writer.writeheader()
    writer.writerows(all_results)

print(f"\n✅ Done! {len(all_results)} unique papers saved to {output_file}")
