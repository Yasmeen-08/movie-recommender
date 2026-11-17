import json
import streamlit as st

st.set_page_config(page_title="Yasmeen's CineMatch", page_icon="🎬", layout="centered")

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top, #3a0d2e 0%, #14061f 45%, #0a0a12 100%); }
h1.title { text-align:center; font-size:42px; margin-bottom:0;
  background: linear-gradient(90deg,#ff4b6e,#ffb347);
  -webkit-background-clip:text; background-clip:text; color:transparent; }
.sub { text-align:center; color:#b9b3c9; margin-bottom:24px; }
.card { background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.12);
  border-radius:14px; padding:14px 18px; margin:10px 0; display:flex; align-items:center; gap:14px; }
.num { min-width:34px; height:34px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; font-weight:700; color:#fff;
  background:linear-gradient(135deg,#ff4b6e,#ffb347); }
.info { flex:1; }
.name { font-size:17px; font-weight:600; color:#fff; margin-bottom:8px; }
.bar { height:6px; border-radius:3px; background:rgba(255,255,255,0.15); overflow:hidden; }
.bar div { height:100%; background:linear-gradient(90deg,#ff4b6e,#ffb347); }
.pct { font-size:12px; color:#b9b3c9; margin-top:5px; }
.foot { text-align:center; color:#7d7690; font-size:13px; margin-top:40px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    with open("model.json", encoding="utf-8") as f:
        return json.load(f)


model = load_model()
titles = model["titles"]
vectors = model["vectors"]


def recommend(index, n=6):
    v = vectors[index]
    scores = []
    for j, other in enumerate(vectors):
        if j == index:
            continue
        score = sum(x * other.get(w, 0) for w, x in v.items())
        scores.append((score, titles[j]))
    scores.sort(reverse=True)
    top = scores[:n]
    best = top[0][0] or 1
    return [(t, max(1, round(s / best * 100))) for s, t in top]


st.markdown('<h1 class="title">🎬 Yasmeen\'s CineMatch</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub">Tell me a movie you love. I\'ll find your next obsession. 🍿</div>',
            unsafe_allow_html=True)

default = titles.index("Avatar") if "Avatar" in titles else 0
choice = st.selectbox("Pick or search a movie", titles, index=default)

if st.button("Recommend 🎯", use_container_width=True):
    results = recommend(titles.index(choice))
    st.subheader(f"Because you liked {choice}")
    for i, (name, match) in enumerate(results, 1):
        st.markdown(f"""
        <div class="card">
          <div class="num">{i}</div>
          <div class="info">
            <div class="name">{name}</div>
            <div class="bar"><div style="width:{match}%"></div></div>
            <div class="pct">{match}% match</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="foot">Made with ❤️ by Yasmeen Khan · TF-IDF + cosine similarity · TMDB 5000 dataset</div>',
            unsafe_allow_html=True)
