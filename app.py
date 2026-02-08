from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import pandas as pd
from werkzeug.utils import secure_filename
import subprocess
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src import (
    extract_text,
    preprocess,
    embeddings,
    similarity,
    rank_candidates,
    utils,
    llm,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["OUTPUTS_FOLDER"] = "output"
os.makedirs(app.config["OUTPUTS_FOLDER"], exist_ok=True)

# Load models at startup
embeddings.load_models_at_startup()

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


# Handle Chrome DevTools .well-known requests to avoid 404 errors
@app.route("/.well-known/<path:filename>")
def well_known(filename):
    return "", 204


# Global storage for resume and job texts (in production, use proper session management)
global_resume_texts = {}
global_job_text = ""


@app.route("/rank", methods=["POST"])
def rank_candidates_route():
    start_time = time.time()
    global global_resume_texts, global_job_text

    try:
        if "resumes" not in request.files or "job_description" not in request.files:
            return (
                jsonify({"error": "Please upload both resumes and job description"}),
                400,
            )

        resumes = request.files.getlist("resumes")
        job_description_file = request.files["job_description"]

        if not resumes or not job_description_file:
            return jsonify({"error": "No files selected"}), 400

        if not allowed_file(job_description_file.filename):
            return jsonify({"error": "Job description must be a TXT file"}), 400

        # Store job description text globally
        job_text_raw = job_description_file.read().decode("utf-8")
        global_job_text = job_text_raw

        # Process job description
        job_text = preprocess.clean_text(job_text_raw)
        job_emb = embeddings.get_embedding(job_text)

        resume_texts = []
        resume_names = []
        global_resume_texts = {}  # Reset and store raw resume texts

        # Process resumes efficiently
        for file in resumes:
            if file and allowed_file(file.filename):
                resume_names.append(file.filename)
                try:
                    # Store raw text for summarization
                    raw_text = extract_text.extract_text(file)
                    global_resume_texts[file.filename] = raw_text

                    if raw_text.strip():  # Only process non-empty texts
                        text = preprocess.clean_text(raw_text)
                        resume_texts.append(text)
                    else:
                        resume_texts.append("")  # Empty text for failed extractions
                except Exception as e:
                    print(f"Error processing {file.filename}: {e}")
                    global_resume_texts[file.filename] = (
                        f"Error extracting text: {str(e)}"
                    )
                    resume_texts.append("")  # Empty text for failed extractions

        if not resume_texts:
            return jsonify({"error": "No valid resume files found"}), 400

        # Generate embeddings and calculate similarities efficiently
        resume_embeddings = []
        for text in resume_texts:
            if text.strip():  # Only generate embeddings for non-empty texts
                try:
                    emb = embeddings.get_embedding(text)
                    resume_embeddings.append(emb)
                except Exception as e:
                    print(f"Error generating embedding: {e}")
                    resume_embeddings.append(None)
            else:
                resume_embeddings.append(None)

        # Calculate scores, handling failed extractions
        scores = []
        valid_candidates = []
        for i, (emb, name) in enumerate(zip(resume_embeddings, resume_names)):
            if emb is not None:
                try:
                    score = similarity.calculate_similarity(emb, job_emb)
                    scores.append(score)
                    valid_candidates.append(name)
                except Exception as e:
                    print(f"Error calculating similarity for {name}: {e}")
                    scores.append(0.0)  # Default low score for failed calculations
                    valid_candidates.append(name)
            else:
                scores.append(0.0)  # Default low score for failed extractions
                valid_candidates.append(name)

        if not valid_candidates:
            return jsonify({"error": "Failed to process any resume files"}), 400

        # Save results
        output_path = os.path.join(
            app.config["OUTPUTS_FOLDER"], "ranked_candidates.csv"
        )
        df = rank_candidates.rank_candidates(valid_candidates, scores, output_path)
        results = df.to_dict("records")

        # Add terminal message for processing time
        end_time = time.time()
        processing_time = end_time - start_time
        print(
            f"Processed {len(valid_candidates)} candidates in {processing_time:.2f} seconds"
        )

        return jsonify(
            {
                "success": True,
                "results": results,
                "message": f"Successfully ranked {len(valid_candidates)} candidates",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download")
def download_results():
    try:
        output_path = os.path.join(
            app.config["OUTPUTS_FOLDER"], "ranked_candidates.csv"
        )
        if os.path.exists(output_path):
            return send_file(
                output_path, as_attachment=True, download_name="ranked_candidates.csv"
            )
        else:
            return jsonify({"error": "Results file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_summary", methods=["POST"])
def generate_summary():
    start_time = time.time()
    try:
        candidate_name = request.form.get("candidate_name")

        if not candidate_name:
            return jsonify({"error": "Missing candidate name"}), 400

        # Get stored resume and job texts
        resume_text = global_resume_texts.get(candidate_name, "")
        job_text = global_job_text

        if not resume_text:
            return (
                jsonify(
                    {"error": f"Resume text not found for candidate: {candidate_name}"}
                ),
                400,
            )

        if not job_text:
            return (
                jsonify(
                    {
                        "error": "Job description not found. Please re-upload the job description."
                    }
                ),
                400,
            )

        # Generate summary using Google Gemini
        summary = llm.generate_summary(resume_text, job_text, "Data Analyst")

        # Add terminal message for processing time
        end_time = time.time()
        processing_time = end_time - start_time
        print(
            f"Generated summary for {candidate_name} in {processing_time:.2f} seconds"
        )

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
