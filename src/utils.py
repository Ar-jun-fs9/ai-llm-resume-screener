import os


def get_resume_files(resume_folder):
    files = []
    for file in os.listdir(resume_folder):
        if file.endswith(".pdf") or file.endswith(".docx"):
            files.append(os.path.join(resume_folder, file))
    return files


def read_job_description(job_desc_file):
    with open(job_desc_file, "r", encoding="utf-8") as f:
        return f.read()
