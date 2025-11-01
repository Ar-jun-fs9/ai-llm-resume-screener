from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


def load_local_model():
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",  # Automatically uses GPU if available, CPU otherwise
            load_in_8bit=True,  # Loads model in 8-bit integers → faster & less memory
        )
        summarizer = pipeline("text-generation", model=model, tokenizer=tokenizer)
        print(f"Successfully loaded LLM model: {model_name}")
        return summarizer
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


# Global variable to store the model
summarizer = None


def load_models_at_startup():
    """Load the LLM model at startup and print success message."""
    global summarizer
    if summarizer is None:
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name)
            summarizer = pipeline("text-generation", model=model, tokenizer=tokenizer)
            print(f"Successfully loaded LLM model: {model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            summarizer = None
    return summarizer


def get_summarizer():
    global summarizer
    if summarizer is None:
        summarizer = load_local_model()
    return summarizer


def generate_resume_summary(resume_text, job_text):
    summarizer = get_summarizer()
    if summarizer is None:
        return "Error: Unable to load the LLM model. Please ensure transformers and torch are installed."

    # Limit text length to avoid memory issues
    resume_text = resume_text[:1500] if resume_text else ""
    job_text = job_text[:1500] if job_text else ""

    prompt = f"""<|system|>
You are an HR assistant. Analyze this candidate's resume against the job description.
Summarize the candidate's suitability, key skills, and overall match.
</s>
<|user|>
Resume:
{resume_text}

Job Description:
{job_text}

Provide a short structured summary of the candidate's fit for this role.
</s>
<|assistant|>"""

    try:
        output = summarizer(
            prompt, max_new_tokens=200, do_sample=True, temperature=0.7, pad_token_id=2
        )
        generated_text = output[0]["generated_text"]

        # Extract only the assistant's response
        if "<|assistant|>" in generated_text:
            summary = generated_text.split("<|assistant|>")[-1].strip()
        else:
            # Fallback extraction method
            summary = generated_text.replace(prompt, "").strip()

        # Ensure summary ends with a fullstop
        if summary and not summary.endswith("."):
            summary += "."

        return summary if summary else "Unable to generate summary."

    except Exception as e:
        return f"Error generating summary: {str(e)}"
