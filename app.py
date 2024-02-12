
from Bio import Entrez
import streamlit as st

# Always provide your email when using NCBI's E-utilities
Entrez.email = "your_email@example.com"

def fetch_papers_and_count(query):
    # Fetch the total count of results
    handle_count = Entrez.esearch(db="pubmed", term=query, rettype="count")
    record_count = Entrez.read(handle_count)
    handle_count.close()
    total_count = int(record_count["Count"])
    
    # Fetch details for the first 10 articles
    handle_articles = Entrez.esearch(db="pubmed", term=query, retmax=10)
    record_articles = Entrez.read(handle_articles)
    handle_articles.close()
    pmids = record_articles['IdList']
    
    papers = []
    for pmid in pmids:
        handle_article = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
        articles = Entrez.read(handle_article)
        for article in articles['PubmedArticle']:
            try:
                title = article['MedlineCitation']['Article']['ArticleTitle']
                authors_list = article['MedlineCitation']['Article']['AuthorList']
                authors = ', '.join([author['LastName'] for author in authors_list if 'LastName' in author])
                abstract = article['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
                papers.append({'title': title, 'authors': authors, 'abstract': abstract})
            except Exception as e:
                st.error(f"Error processing article with PMID {pmid}: {e}")
        handle_article.close()
    
    return papers, total_count

st.title('Revolutionizing Systematic Reviews in Medicine')

query = st.text_input("Enter your search query:")

if st.button('Search'):
    papers, total_results = fetch_papers_and_count(query)
    if papers:
        st.write(f"Total results: {total_results}. Here are 10 of the articles:")
        for paper in papers:
            st.write(f"**Title:** {paper['title']}")
            st.write(f"**Authors:** {paper['authors']}")
            st.write(f"**Abstract:** {paper['abstract']}")
            st.write("---")  # Add a separator line
    else:
        st.write("No papers found.")

