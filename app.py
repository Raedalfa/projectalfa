
from metapub import PubMedFetcher
import streamlit as st

fetcher = PubMedFetcher()

def fetch_papers(query):
    pmids = fetcher.pmids_for_query(query)
    papers = []
    for pmid in pmids[:10]:  # Limit to first 10 results for demonstration
        try:
            article = fetcher.article_by_pmid(pmid)
            papers.append({
                "title": article.title,
                "authors": ', '.join(article.authors),
                "abstract": article.abstract
            })
        except Exception as e:
            st.error(f"Error fetching article with PMID {pmid}: {e}")
    return papers, len(pmids)  # Return both the papers and the total count

st.title('Revolutionizing Systematic Reviews in Medicine')

query = st.text_input("Enter your search query:")

if st.button('Search'):
    papers, total_results = fetch_papers(query)
    st.write(f"Total results: {total_results}")
    if papers:
        for paper in papers:
            st.write(f"**Title:** {paper['title']}")
            st.write(f"**Authors:** {paper['authors']}")
            st.write(f"**Abstract:** {paper['abstract']}")
            st.write("---")  # Add a separator line
    else:
        st.write("No papers found.")

