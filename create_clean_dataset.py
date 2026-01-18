import pandas as pd
import json
import os
import glob

def clean_and_export_data():
    print("Veri temizleme ve dışa aktarma işlemi başlıyor...")
    
    # 1. Verileri Yükle
    data_dir = 'jsonldata'
    files = {
        'main': os.path.join(data_dir, 'healthbench_main_5000.jsonl'),
        'consensus': os.path.join(data_dir, 'healthbench_consensus_3671.jsonl'),
        'hard': os.path.join(data_dir, 'healthbench_hard_1000.jsonl')
    }

    dfs = []
    for label, file_path in files.items():
        if os.path.exists(file_path):
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            temp_df = pd.DataFrame(data)
            temp_df['source_dataset'] = label
            dfs.append(temp_df)
    
    if not dfs:
        print("Hata: Veri dosyaları bulunamadı.")
        return

    df = pd.concat(dfs, ignore_index=True)
    print(f"Toplam Ham Veri Sayısı: {len(df)}")

    # 2. Temizleme Fonksiyonları
    def extract_prompt(prompt_data):
        # Prompt bir liste geliyor, genellikle son kullanıcı mesajı veya tüm konuşma geçmişi önemli
        # Basitlik için tüm konuşmayı metin olarak birleştirelim veya son soruyu alalım.
        # Genellikle SFT için: User: ... Assistant: ... formatı makbuldür.
        # Burada sadece User'ın sorusunu (Instruction) alalım.
        if isinstance(prompt_data, list):
            # Genellikle son mesaj user'a aittir
            for p in reversed(prompt_data):
                if p.get('role') == 'user':
                    return p.get('content', '')
            # Bulamazsa hepsini birleştir
            return "\n".join([f"{p.get('role')}: {p.get('content')}" for p in prompt_data])
        return str(prompt_data)

    def extract_ideal_completion(data):
        if data is None:
            return None
        if isinstance(data, dict):
            val = data.get('ideal_completion')
            # Bazen ideal_completion bir liste olabilir veya boş olabilir
            if isinstance(val, list): 
                return val[0] if val else None
            if isinstance(val, str) and len(val.strip()) > 0:
                return val
        return None

    # 3. Veriyi İşle
    df['instruction'] = df['prompt'].apply(extract_prompt)
    df['output'] = df['ideal_completions_data'].apply(extract_ideal_completion)
    
    # 4. Filtreleme (Sadece ideal cevabı olanlar)
    clean_df = df.dropna(subset=['output']).copy()
    print(f"Temizlenmiş (İdeal Cevaplı) Veri Sayısı: {len(clean_df)}")
    
    # Gereksiz boşlukları temizle
    clean_df['instruction'] = clean_df['instruction'].str.strip()
    clean_df['output'] = clean_df['output'].str.strip()
    
    # Sadece gerekli sütunları seç
    # 'example_tags' listesini virgülle ayrılmış string'e çevirelim (kolay okuma için)
    clean_df['tags'] = clean_df['example_tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
    
    final_df = clean_df[['source_dataset', 'instruction', 'output', 'tags', 'rubrics']]

    # 5. Kaydetme
    output_dir = 'processed_data'
    
    # A) Tüm Temiz Veri (CSV)
    final_df.to_csv(os.path.join(output_dir, 'healthbench_clean_all.csv'), index=False)
    
    # B) Eğitim Seti (Sadece instruction ve output - SFT için hazır)
    train_df = final_df[['instruction', 'output']]
    train_df.to_csv(os.path.join(output_dir, 'train_sft.csv'), index=False)
    
    # C) JSONL Formatı (HuggingFace/OpenAI formatına daha yakın)
    # {"messages": [{"role": "user", "content": ...}, {"role": "assistant", "content": ...}]}
    
    jsonl_output_path = os.path.join(output_dir, 'train_sft.jsonl')
    with open(jsonl_output_path, 'w', encoding='utf-8') as f:
        for _, row in final_df.iterrows():
            entry = {
                "messages": [
                    {"role": "user", "content": row['instruction']},
                    {"role": "assistant", "content": row['output']}
                ],
                "source": row['source_dataset'],
                "tags": row['tags']
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"\nDosyalar '{output_dir}' klasörüne kaydedildi:")
    print(f"1. healthbench_clean_all.csv (Tüm detaylar - {len(final_df)} satır)")
    print(f"2. train_sft.csv (Sadece Soru/Cevap - {len(train_df)} satır)")
    print(f"3. train_sft.jsonl (Chat formatı - {len(final_df)} satır)")

if __name__ == "__main__":
    clean_and_export_data()
