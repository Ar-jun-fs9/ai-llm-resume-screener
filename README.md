<div align="center">

# 🤖 AI-Powered Resume Screener with LLM

**Smart candidate ranking and AI-powered resume summarization using TinyLlama**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green.svg)](https://flask.palletsprojects.com)
[![Local LLM](https://img.shields.io/badge/%20LLM-TinyLlama-orange.svg)](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)

_Process resumes, rank candidates by job fit, and generate AI summaries - all locally on your machine_

</div>

---

## 🚀 Features

- **📄 Resume Processing**: Upload PDF/DOCX resume files
- **📝 Job Description Analysis**: Upload job requirements in TXT format
- **🎯 AI-Powered Ranking**: Semantic similarity ranking using advanced embeddings
- **🤖 Local LLM Summarization**: AI-generated summaries with TinyLlama
- **📊 CSV Export**: Download complete ranking results
- **🔒 Privacy-First**: All processing happens locally, no data sent externally

---

## ⚠️ First Run Important Notes

**When you first run the application after cloning/downloading, you'll see these models being downloaded:**

```
Successfully loaded LLM model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
Successfully loaded Embedding model: all-MiniLM-L6-v2
```

### 📦 Model Download Information

| Model                        | Size   | Purpose                      | Cache Location  |
| ---------------------------- | ------ | ---------------------------- | --------------- |
| **TinyLlama-1.1B-Chat-v1.0** | ~1-2GB | LLM for resume summarization | `.cache` folder |
| **all-MiniLM-L6-v2**         | ~100MB | Semantic embeddings          | `.cache` folder |

**Important:**

- **Download Frequency**: Models are downloaded **only once** and cached permanently
- **First Run Time**: 5-15 minutes depending on your internet connection
- **Subsequent Runs**: Models load instantly from cache
- **Disk Space**: ~2GB total for all models

### ⚡ Performance Expectations

- **Current Summary Generation**: ~1 minute per candidate (CPU-only inference)
- **Hardware Consideration**: Optimized for laptop specs - higher-end systems may experience lag
- **Future Updates**: Will optimize to achieve sub-1-second summary generation

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- 8GB+ RAM (for TinyLlama model loading)
- ~2GB disk space for model downloads
- CPU-only (no GPU required)

### Quick Start

```bash
# 1. Clone or download the project
git clone https://github.com/Ar-jun-fs9/ai-llm-resume-screener.git
cd ai-llm-resume-screener

# 2. Install dependencies
pip install -r requirements.txt

# 3. First run (models will download automatically)
python app.py

# 4. Open your browser
# Navigate to http://localhost:5000
```

---

## 🎯 How It Works

### 1. Similarity Scoring Algorithm

The application uses **cosine similarity** to rank candidates based on semantic matching between resumes and job descriptions:

#### **Step-by-Step Process:**

1. **Text Extraction**: Resume and job description text is extracted from uploaded files
2. **Text Preprocessing**: Text is cleaned and normalized for better matching
3. **Embedding Generation**: Both texts are converted to high-dimensional vectors using `all-MiniLM-L6-v2`
4. **Similarity Calculation**: Cosine similarity is computed between resume and job embeddings
5. **Score Normalization**: Results are sorted by similarity score (highest first) and similarity score (0-1) is converted to percentage for display

#### **Color Coding:**

- 🟢 **Green (≥70%)**: Excellent match - highly qualified
- 🟡 **Yellow (40-69%)**: Good match - worth considering
- 🔴 **Red (<40%)**: Poor match - may not be suitable

### 2. AI-Powered Summarization

Using **TinyLlama-1.1B-Chat-v1.0** for local LLM analysis:

1. **Context Preparation**: Resume and job description are prepared for LLM input
2. **Prompt Engineering**: Structured prompt guides the AI to analyze candidate fit
3. **Text Generation**: TinyLlama generates detailed assessment including:
   - Key candidate skills
   - Overall role compatibility
   - Strengths and potential gaps
   - Structured evaluation

---

## 📖 Usage Guide

### Step 1: Upload Files

- **Resumes**: Select multiple PDF/DOCX files
- **Job Description**: Select one TXT file

### Step 2: Rank Candidates

- Click **"Rank Candidates"** to process all files
- View ranked results with similarity percentages

### Step 3: Generate Summaries

- Click **"Summarize"** button for any candidate
- AI generates detailed assessment using local TinyLlama model

### Step 4: Export Results

- Click **"Download Results (CSV)"** to export all rankings

---

## 🏗️ Project Structure

```
├── app.py                     # Main Flask application
├── src/
│   ├── extract_text.py        # PDF/DOCX text extraction
│   ├── preprocess.py          # Text preprocessing & cleaning
│   ├── embeddings.py          # Sentence transformer embeddings
│   ├── similarity.py          # Cosine similarity calculation
│   ├── rank_candidates.py     # Candidate ranking & CSV export
│   └── local_llm.py           # TinyLlama integration
├── templates/
│   └── index.html             # Main web interface
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── index.js           # Frontend interactions
├── output/                    # Generated CSV files
└── requirements.txt           # Python dependencies
```

---

## 🚀 Future Enhancements

- **⚡ Performance Optimization**: Target sub-1-second summary generation
- **🎯 Enhanced Models**: Integration of faster, more capable LLMs
- **📱 Mobile Interface**: Responsive design improvements
- **🔄 Batch Processing**: Multiple job descriptions simultaneously
- **📊 Analytics Dashboard**: Detailed recruitment insights
- **☁️ Cloud Integration**: Optional cloud model support

---
## 🙏 Acknowledgments

- **TinyLlama Team**: For the lightweight chat model
- **Sentence Transformers**: For semantic embedding capabilities
- **Flask Community**: For the excellent web framework
- **Hugging Face**: For model hosting and transformers library

---

**Built with**

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-black.svg?labelColor=orange)](#)


