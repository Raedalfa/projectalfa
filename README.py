# projectalfa
git add requirements.txt
git commit -m "Add requirements.txt with necessary packages"
git push origin main
import streamlit as st
from metapub import PubMedFetcher

fetcher = PubMedFetcher()
def fetch_papers(query):
    pmids = fetcher.pmids_for_query(query)
    papers = []
    for pmid in pmids[:10]:  # Limit to first 10 results for demonstration
        try:
            article = fetcher.article_by_pmid(pmid)
            papers.append(article)
        except Exception as e:
            st.error(f"Error fetching article with PMID {pmid}: {e}")
    return papers

st.title('Revolutionizing Systematic Reviews in Medicine')

query = st.text_input("Enter your search query:")

if st.button('Search'):
    papers = fetch_papers(query)
    if papers:
        for paper in papers:
            st.write(f"**Title:** {paper.title}")
            st.write(f"**Authors:** {', '.join(paper.authors)}")
            st.write(f"**Abstract:** {paper.abstract}")
            st.write("---")  # Add a separator line
    else:
        st.write("No papers found.")

