# TurkishHealthBench Veri Seti Analiz Raporu

**Tarih:** 17 Ocak 2026  
**Analiz Edilen Dosyalar:** `healthbench_main_5000.jsonl`, `healthbench_consensus_3671.jsonl`, `healthbench_hard_1000.jsonl`  
**Toplam Veri Sayısı:** 9,671 Örnek

---

## 1. Veri Seti Genel Bakış
Bu veri seti, Tıp ve Yapay Zeka alanında kullanılmak üzere, **lisanslı hekimler tarafından doğrulanmış**, yüksek kaliteli bir diyalog ve değerlendirme kümesidir. Veri seti, bir hasta (User) ile bir sağlık asistanı (AI) arasındaki ideal iletişimi simüle eder.

### 1.1. Kaynak Dağılımı
*   **Main Set (Ana Veri):** 5,000 örnek (%51.7) - Genel medikal senaryoları kapsar.
*   **Consensus Set (Uzlaşı):** 3,671 örnek (%38.0) - En yüksek güvenilirlik seviyesine sahiptir. Birden çok doktorun cevabın doğruluğu üzerinde tam uzlaşıya vardığı "Altın Standart" verilerdir.
*   **Hard Set (Zor):** 1,000 örnek (%10.3) - Modellerin sınırlarını zorlayan, karmaşık, çok adımlı veya gri alan (hedging gerektiren) vakaları içerir.

### 1.2. Veri Kalitesi (SFT Uygunluğu)
*   **İdeal Cevaplar:** Veri setinin **%85'i (8,231 adet)**, model eğitimi için doğrudan kullanılabilecek, doktor onaylı "Ideal Completion" (İdeal Cevap) içermektedir. Bu, veri setinin "Supervised Fine-Tuning" (SFT) için son derece elverişli olduğunu gösterir.
*   **Kalan %15:** Kalan kısımda ideal cevap metni yerine, cevabın nasıl olması gerektiğini anlatan "Rubrics" (Puanlama Kriterleri) bulunur. Bu kısım modelin değerlendirilmesi (RLHF) için kullanılabilir.

---

## 2. İçerik ve Senaryo Analizi (Simülasyonlar)
Veri seti, rastgele tıbbi sorulardan değil, iyi yapılandırılmış 5 temel simülasyon senaryosundan oluşur. Bu senaryolar, bir sağlık asistanının sahip olması gereken 5 temel yetkinliği ölçer:

| # | Senaryo (Tema) | Adet | Açıklama | Ölçülen Yetkinlik |
|---|---|---|---|---|
| **1** | **Global Health** | 2011 | Bölgesel hastalıklar, yerel tedavi imkanları ve coğrafi bağlam. | Yerel tıbbi bilgi & Kültürel adaptasyon. |
| **2** | **Hedging** | 1949 | Riskli/belirsiz durumlarda kesin konuşmaktan kaçınma ("Doktora danış" uyarısı). | Güvenlik & Haddini bilme (Risk yönetimi). |
| **3** | **Communication** | 1776 | Hasta ile empatik, açık ve profesyonel dil kullanımı. | Hasta iletişimi & Empati. |
| **4** | **Context Seeking** | 1181 | Eksik bilgiyi (belirti, ilaç geçmişi) kullanıcıdan sorma becerisi. | Anamnez (Bilgi toplama) yeteneği. |
| **5** | **Emergency Referrals** | 1001 | Acil durumları tespit edip hastayı doğru yönlendirme (Triaj). | Kriz yönetimi & Triaj. |

---

## 3. "İdeal Cevap" Standartları ve Güvenilirlik
Bu veri setindeki cevapların "İdeal" olarak kabul edilmesinin dayanağı, **Doktor Uzlaşısı (Physician Consensus)** modelidir.

*   **Kim Onayladı?:** Cevaplar, yapay zeka tarafından değil, **lisanslı tıp doktorlarından oluşan kurullar** tarafından incelenmiş ve onaylanmıştır.
*   **Nasıl Belirlendi?:** Bir cevabın ideal sayılması için 3 temel kriteri geçmesi sağlanmıştır:
    1.  **Tıbbi Doğruluk (Medical Accuracy):** Güncel tıbbi rehberlere tam uyum.
    2.  **Güvenlik (Safety):** Hastaya zarar verebilecek (örn. yanlış ilaç tavsiyesi) veya tedaviyi geciktirecek önerilerden kaçınma.
    3.  **İletişim (Communication):** Yargılayıcı olmayan, açıklayıcı ve destekleyici bir dil.

---

## 4. Kullanım Önerileri (TurkishHealthBench Projesi İçin)

### 4.1. Model Eğitimi (SFT)
*   **Kaynak:** `consensus` ve `main` setlerindeki 8,231 "İdeal Cevap"lı veriyi kullanın.
*   **Hedef:** Türkçe bir medikal asistan modeli eğitmek.
*   **İşlem:** Bu verileri Türkçeye çevirerek (Lokalizasyon yaparak) LLM'inize "Doktor gibi düşünmeyi" ve "Türkçe konuşmayı" aynı anda öğretebilirsiniz.

### 4.2. Model Değerlendirmesi (Evaluation)
*   **Kaynak:** `hard` datasındaki 1,000 örnek.
*   **Hedef:** Modelin zorlu durumlardaki performansını ölçmek.
*   **Yöntem:** Modelinizin ürettiği cevapları, veri setindeki `rubrics` (puanlama kriterleri) ile karşılaştırarak otomatik puanlama (LLM-as-a-Judge) yapabilirsiniz.

### 4.3. Kritik Başarı Faktörü: Lokalizasyon
*   `Global Health` temasındaki veriler çevrilirken Türkiye'nin sağlık sistemi ve epidemiyolojik gerçekleri (Türkiye'de sık görülen hastalıklar, ilaç isimleri, sağlık sistemi işleyişi) dikkate alınmalıdır. Doğrudan çeviri, yanıltıcı olabilir.
