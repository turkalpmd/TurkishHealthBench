# download_healthbench.py
from datasets import load_dataset
from tqdm import tqdm
import json

splits = ["oss_eval", "hard", "consensus"]
names = ["main_5000", "hard_1000", "consensus_3671"]

for split, name in zip(splits, names):
    print(f"→ {name} indiriliyor ve {name}.jsonl olarak kaydediliyor...")
    dataset = load_dataset("Tonic/Health-Bench-Eval-OSS-2025-07", split=split)
    
    with open(f"healthbench_{name}.jsonl", "w", encoding="utf-8") as f:
        for item in tqdm(dataset):
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✓ {name} kaydedildi → healthbench_{name}.jsonl\n")

print("Hepsi bitti! 3 tane .jsonl dosyası oluştu.")