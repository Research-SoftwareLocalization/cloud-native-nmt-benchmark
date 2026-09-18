import csv
import torch
from comet import download_model, load_from_checkpoint

print("=== Step 1: Loading COMET Model ===")
model_path = download_model("Unbabel/wmt20-comet-da")
model = load_from_checkpoint(model_path)

print("=== Step 2: Loading Evaluation Corpus ===")
with open("data/source/en.txt", "r", encoding="utf-8") as f:
    src = f.read().splitlines()
with open("data/baseline_google_translate/hi.txt", "r", encoding="utf-8") as f:
    ref = f.read().splitlines()
with open("data/indictrans2/hi.txt", "r", encoding="utf-8") as f:
    hyp = f.read().splitlines()

data = [{"src": s, "mt": h, "ref": r} for s, r, h in zip(src, ref, hyp)]

print(f"=== Step 3: Computing COMET Scores for {len(src)} strings ===")
use_gpu = 1 if torch.cuda.is_available() else 0
model_output = model.predict(data, batch_size=32, gpus=use_gpu)

print("=== Step 4: Filtering & Exporting Verified Disagreements ===")
output_file = "verified_metric_disagreements.csv"
saved_count = 0

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Line_Number", "Source_EN", "Google_Ref_HI", "IndicTrans2_Hyp_HI", "COMET_Score"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for i, score in enumerate(model_output.scores):
        word_count = len(src[i].split())
        if 1 <= word_count <= 3 and score >= 0.85:
            ref_words = set(ref[i].split())
            hyp_words = set(hyp[i].split())
            
            if len(ref_words.intersection(hyp_words)) == 0 and len(ref_words) > 0:
                writer.writerow({
                    "Line_Number": i + 1,
                    "Source_EN": src[i],
                    "Google_Ref_HI": ref[i],
                    "IndicTrans2_Hyp_HI": hyp[i],
                    "COMET_Score": f"{score:.4f}"
                })
                saved_count += 1

print(f"Saved {saved_count} verified examples to '{output_file}'.")
