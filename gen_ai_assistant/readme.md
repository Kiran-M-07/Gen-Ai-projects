# Biomedical Research Assistant Pipeline (GenAI-Powered)

## Objective

This project is a prototype for a biomedical data platform capable of extracting structured insights from unstructured biomedical literature using Generative AI (GenAI). The assistant processes research articles and extracts diseases, genes/proteins, biological pathways, experimental methods, and key findings.

---

## Dataset

The dataset consists of 50 biomedical research articles in `.md` format, named using their PubMed ID (e.g., `39834406.md`). Each file contains:
- Title
- PubMed ID
- Journal
- Keywords
- Abstract
- Optional additional content

---

## LLM Used

- **Model**: llama-3.1-8b-instant
- **Provider**: [Groq](https://groq.com/)
- **Framework**: [LangChain](https://python.langchain.com/docs/integrations/chat/groq/)

---

## Pipeline Steps

### 1. **Markdown Parsing**
Extract structured metadata from each `.md` file:
- `pubmed_id`, `title`, `journal`, `keywords`, `abstract`, and `full_text`.

### 2. **Filtering**
Articles are filtered by LLM:
- Prompted llama3.1 to filter articles as relevant if the articles are about cancer/immunology
- Result: `filtered_articles.json` with the selected PubMed IDs.

### 3. **Biomedical Entity & Summary Extraction**
For each filtered article:
- A structured prompt is sent to Groq’s LLM.
- Extracted fields:
  - `diseases`, `genes_proteins`, `pathways`, `methods`, `key_findings`
- Result: `extracted_insights.json`

---

## Project Structure
Please lookout for project design/app design in the files :
1. project_design.jpg
2. app_workflow.jpg
3. app_demo
4. GenAi_project_workflow.pdf


## Manual Evaluation
- Manually check the filtering of articles by LLM. 
- Manually evaluated the quality of summary generated.

## Evaluation based on text similarity
- Evaluated the summary by calculating the cosine similarity score between summary and abstract.

#### LLM Performed Well On:
Filtering relevant articles related to cancer/immunology.

Extracting general disease names (e.g., "neuroblastoma", "thyroid cancer").

Capturing experimental methods like "scRNA-seq" or "bulk RNASeq" accurately.

Generating concise summaries of scientific insights.

