import csv, json, re, math
from collections import Counter

# ---------- Part 1: read data and build tags ----------
def read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

movies = read("data/tmdb_5000_movies.csv")
credits = read("data/tmdb_5000_credits.csv")

credits_by_id = {c["movie_id"]: c for c in credits}

def names(text, limit=None):
    items = json.loads(text) if text else []
    result = [i["name"].replace(" ", "") for i in items]
    return result[:limit] if limit else result

def director(text):
    for person in json.loads(text):
        if person["job"] == "Director":
            return [person["name"].replace(" ", "")]
    return []

data = []
for m in movies:
    c = credits_by_id.get(m["id"])
    if not c:
        continue
    overview = (m["overview"] or "").lower().split()
    extra = (
        names(m["genres"])
        + names(m["keywords"])
        + names(c["cast"], 3)
        + director(c["crew"])
    )
    tags = overview + [w.lower() for w in extra]
    data.append({"id": m["id"], "title": m["title"], "tags": tags})

print("Movies loaded:", len(data))

# ---------- Part 2: clean tags and build TF-IDF model ----------
STOP = set("""a an the and or but in on at to of for with by from as is are was were
be been it its this that these those he she they his her their him them who which
what when where while after before into over under about up out than then so not
no can will just one two also has have had""".split())

def clean(tags):
    out = []
    for t in tags:
        t = re.sub(r"[^a-z0-9]", "", t)
        if len(t) > 1 and t not in STOP:
            out.append(t)
    return out

docs = [clean(m["tags"]) for m in data]
N = len(docs)

df = Counter()
for d in docs:
    df.update(set(d))
idf = {w: math.log(N / (1 + df[w])) + 1 for w in df}

vectors = []
for d in docs:
    tf = Counter(d)
    v = {w: c * idf[w] for w, c in tf.items()}
    norm = math.sqrt(sum(x * x for x in v.values())) or 1
    vectors.append({w: round(x / norm, 4) for w, x in v.items()})

titles = [m["title"] for m in data]

with open("model.json", "w", encoding="utf-8") as f:
    json.dump({"titles": titles, "vectors": vectors}, f)

# ---------- Part 3: recommend function ----------
def recommend(title, n=5):
    lower = [t.lower() for t in titles]
    if title.lower() not in lower:
        return []
    i = lower.index(title.lower())
    v = vectors[i]
    scores = []
    for j, other in enumerate(vectors):
        if j == i:
            continue
        score = sum(x * other.get(w, 0) for w, x in v.items())
        scores.append((score, titles[j]))
    scores.sort(reverse=True)
    return [t for _, t in scores[:n]]

# ---------- Test ----------
print("Model saved. Movies:", N)
for name in ["Avatar", "The Dark Knight Rises", "Toy Story"]:
    print(f"\nBecause you liked {name}:")
for r in recommend(name):
        print("  -", r)