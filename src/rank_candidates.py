import pandas as pd


def rank_candidates(
    resume_names, similarity_scores, output_path="output/ranked_candidates.csv"
):
    df = pd.DataFrame(
        {"Candidate": resume_names, "Similarity Score": similarity_scores}
    )
    df = df.sort_values(by="Similarity Score", ascending=False)
    df.to_csv(output_path, index=False)
    print(f"Ranked candidates saved to {output_path}")
    return df
