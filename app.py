import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System ")

st.markdown("""
This AI-powered recommender matches movies based on:
- 🎭 Genres & themes
- 🎬 Actors & directors
- 📌 Description similarity
- ❤️ Your favorite movies
""")

st.divider()

@st.cache_resource
def load_model():
    with open('models/content_recommender.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['titles'], data['X_features']

with st.spinner("Loading movie database..."):
    titles, X_features = load_model()

# dimensiunea embeddingului MiniLM
EMB_DIM = 384
emb_start = X_features.shape[1] - EMB_DIM

# matricea cu DOAR embeddingurile filmelor (ultimele 384 coloane)
X_emb = X_features[:, emb_start:]

model = SentenceTransformer("all-MiniLM-L6-v2")

st.success(f"Choose from {len(titles)} movies!")




def search_movie(keyword):
    keyword = keyword.lower()
    matches = [t for t in titles if keyword in t.lower()]
    return matches


def get_recommendations(movie_title, n=10):
    if movie_title not in titles:
        return None


    idx = titles.index(movie_title)
    movie_vec = X_features[idx].reshape(1, -1)
    scores = cosine_similarity(movie_vec, X_features).flatten()
    all_idx = np.argsort(scores)[::-1]
    rec_idx = all_idx[all_idx != idx][:n]

    rec_titles = [titles[i] for i in rec_idx]
    rec_scores = scores[rec_idx]

    return pd.DataFrame({
        "Rank": range(1, len(rec_titles) + 1),
        "Movie": rec_titles,
        "Match %": (rec_scores * 100).round(1)
    })



def build_user_query(genuri=None, actori=None, regizori=None, teme=None, filme=None):
    parts = []

    if genuri:
        parts.append("Genres: " + ", ".join(genuri))

    if actori:
        parts.append("Actors: " + ", ".join(actori))

    if regizori:
        parts.append("Directed by: " + ", ".join(regizori))

    if teme:
        parts.append("Themes: " + ", ".join(teme))

    if filme:
        parts.append("Similar to: " + ", ".join(filme))

    if not parts:
        return "Popular movies"

    return ". ".join(parts)


def recommend_by_preferences(
    genuri=None, actori=None, regizori=None, teme=None, filme=None,
    n_recommendations=10
):
    query_text = build_user_query(genuri, actori, regizori, teme, filme)
    query_vec = model.encode([query_text])
    movie_embeddings = X_emb  
    scores = cosine_similarity(query_vec, movie_embeddings)[0]
    top_idx = np.argsort(scores)[::-1][:n_recommendations]

    return pd.DataFrame({
        "Rank": range(1, n_recommendations + 1),
        "Movie": [titles[i] for i in top_idx],
        "Match %": (scores[top_idx] * 100).round(1)
    })




st.divider()
st.subheader("🎯 Get Recommendations by Similar Movie")

selected_movie = st.selectbox("Choose a movie:", titles)
num_recs = st.slider("Number of recommendations:", 5, 20, 10)

if st.button("🎬 Recommend by Movie"):
    with st.spinner("Finding similar movies..."):
        recs = get_recommendations(selected_movie, num_recs)
        if recs is not None:
            st.dataframe(recs, hide_index=True, use_container_width=True)


st.divider()
st.subheader("✨ Advanced Recommendations (Multiple Preferences)")

col1, col2 = st.columns(2)

with col1:
    pref_genres = st.text_input("Preferred genres (comma separated)", placeholder="sci-fi, drama")
    pref_actors = st.text_input("Favorite actors", placeholder="Tom Hanks, Brad Pitt")
    pref_directors = st.text_input("Preferred directors", placeholder="Christopher Nolan")

with col2:
    pref_themes = st.text_input("Themes", placeholder="future, family, revenge")
    pref_movies = st.text_input("Similar to movies", placeholder="Inception, Titanic")

if st.button("🔮 Recommend by Preferences"):
    with st.spinner("Generating preference-based recommendations..."):
        recs = recommend_by_preferences(
            genuri=[g.strip() for g in pref_genres.split(",") if g.strip()],
            actori=[a.strip() for a in pref_actors.split(",") if a.strip()],
            regizori=[d.strip() for d in pref_directors.split(",") if d.strip()],
            teme=[t.strip() for t in pref_themes.split(",") if t.strip()],
            filme=[m.strip() for m in pref_movies.split(",") if m.strip()],
            n_recommendations=num_recs
        )
        st.dataframe(recs, hide_index=True, use_container_width=True)

st.divider()
st.caption("Built with Streamlit + SentenceTransformers + Cosine Similarity")
