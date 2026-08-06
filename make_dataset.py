import pandas as pd
import random

random.seed(42)

positive = [
    "Terima kasih banyak atas bantuan awak",
    "Saya sangat hargai usaha awak hari ini",
    "Kerja awak memang kemas dan jelas",
    "Bagus, awak banyak membantu kumpulan",
    "Saya suka cara awak selesaikan tugasan ini",
    "Terima kasih sebab beri kerjasama yang baik",
    "Saya hargai komitmen awak dalam kerja ini",
    "Kerja ini nampak sangat teratur",
    "Terima kasih kerana update awal",
    "Awak buat bahagian ini dengan sangat baik",
]

neutral = [
    "Baik saya akan semak nanti",
    "Saya akan update selepas siap",
    "Kita bincang semula kemudian",
    "Saya akan tengok dahulu",
    "Boleh maklumkan bila sudah siap",
    "Saya tunggu kemas kini daripada awak",
    "Kita ikut perancangan yang telah dibuat",
    "Saya akan hubungi awak kemudian",
    "Noted, saya faham",
    "Baik, saya akan buat bahagian saya",
]

passive = [
    "Terima kasih sebab tak reply langsung",
    "Baguslah semua orang dah siap kerja tinggal awak je",
    "Tak apa saya buat sendiri je macam biasa",
    "Wah hebat sampai semua orang kena tunggu awak",
    "Akhirnya muncul juga selepas semua dah selesai",
    "Saya dah follow up banyak kali mungkin awak terlepas pandang",
    "Saya dah hantar dari semalam tapi mungkin awak belum sempat tengok",
    "Tak apa lah saya dah biasa handle semua sendiri",
    "Saya ingatkan kita buat sama-sama rupanya saya seorang je",
    "Terima kasih ya update last minute macam ni",
]

subjects = [
    "tugasan ini", "bahagian awak", "kerja kumpulan ini", "laporan ini",
    "slaid pembentangan", "dokumen itu", "fail itu", "projek ini",
    "perbincangan tadi", "mesej saya", "kemas kini itu"
]

time_words = [
    "hari ini", "semalam", "tadi", "dari pagi", "dari semalam",
    "sebelum kelas", "sebelum mesyuarat", "sebelum pembentangan"
]

positive_templates = [
    "Terima kasih kerana bantu siapkan {subject} {time}",
    "Saya sangat hargai usaha awak dalam {subject}",
    "Bagus kerja awak untuk {subject}, memang membantu",
    "Saya suka cara awak uruskan {subject}",
    "Terima kasih sebab beri respon yang jelas tentang {subject}",
    "Kerjasama awak dalam {subject} sangat dihargai",
]

neutral_templates = [
    "Saya akan semak {subject} {time}",
    "Boleh update saya tentang {subject} bila ada masa",
    "Kita bincang semula tentang {subject} kemudian",
    "Saya tunggu maklum balas tentang {subject}",
    "Kalau ada perubahan pada {subject}, beritahu saya",
    "Saya akan hantar {subject} selepas siap",
]

passive_templates = [
    "Baguslah, {subject} masih belum siap walaupun semua orang dah tunggu",
    "Tak apa, saya boleh buat {subject} sendiri macam biasa",
    "Terima kasih sebab baru update tentang {subject} {time}",
    "Saya dah follow up tentang {subject} banyak kali, mungkin awak terlepas pandang",
    "Wah hebat, semua orang dah buat kecuali {subject}",
    "Saya ingatkan {subject} kita buat sama-sama, rupanya saya sorang je",
    "Tak apa lah, mungkin saya je yang terlalu risau tentang {subject}",
    "Akhirnya ada juga respon tentang {subject}",
    "Saya dah tunggu {subject} dari tadi, tapi tak apa",
    "Menarik juga bila {subject} diberitahu last minute",
]

def make_sentence(template):
    return template.format(
        subject=random.choice(subjects),
        time=random.choice(time_words)
    )

rows = []

for s in positive:
    rows.append({"text": s, "label": "positive"})

for s in neutral:
    rows.append({"text": s, "label": "neutral"})

for s in passive:
    rows.append({"text": s, "label": "passive aggressive"})

for _ in range(300):
    rows.append({"text": make_sentence(random.choice(positive_templates)), "label": "positive"})
    rows.append({"text": make_sentence(random.choice(neutral_templates)), "label": "neutral"})
    rows.append({"text": make_sentence(random.choice(passive_templates)), "label": "passive aggressive"})

hard_passive = [
    "Saya dah buat bahagian saya, tinggal awak je sekarang",
    "Tak apa kalau tak sempat, saya memang dah biasa cover semua",
    "Mungkin mesej saya tenggelam sebab saya dah tanya banyak kali",
    "Saya bukan nak paksa, cuma semua orang dah tunggu bahagian awak",
    "Bagus juga cara kita plan, tapi akhirnya saya juga yang buat",
    "Saya dah remind beberapa kali, mungkin awak terlalu sibuk",
    "Tak apa, saya faham kerja saya memang kena buat lebih",
    "Terima kasih sebab inform selepas semuanya jadi kelam kabut",
    "Saya ingatkan kita satu kumpulan, bukan saya seorang sahaja",
    "Hebatlah, bahagian awak paling simple pun belum siap",
    "Saya tak kisah pun, cuma pelik kenapa benda ni selalu jadi",
    "Tak mengapa, saya akan betulkan balik walaupun bukan salah saya",
    "Saya tunggu update awak sampai malam, tapi tak apa",
    "Mungkin saya je yang ambil serius tugasan ini",
    "Baguslah, akhirnya kita tahu juga status kerja awak",
]

hard_neutral = [
    "Saya dah follow up, boleh maklumkan status terkini",
    "Saya tunggu update daripada awak apabila ada masa",
    "Boleh beritahu jika awak perlukan bantuan",
    "Kalau belum siap, kita boleh susun semula pembahagian kerja",
    "Saya cuma ingin semak perkembangan tugasan ini",
    "Boleh kongsi status bahagian awak sebelum malam ini",
    "Saya akan bantu kalau ada bahagian yang susah",
    "Kita boleh bincang semula supaya kerja lebih teratur",
    "Saya ingin pastikan semua bahagian siap sebelum hantar",
    "Boleh maklumkan jika ada sebarang masalah",
]

for s in hard_passive:
    rows.append({"text": s, "label": "passive aggressive"})

for s in hard_neutral:
    rows.append({"text": s, "label": "neutral"})

df = pd.DataFrame(rows)

df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip().str.lower()

df = df.drop_duplicates(subset=["text", "label"])

min_count = df["label"].value_counts().min()

balanced = (
    df.groupby("label", group_keys=False)
    .apply(lambda x: x.sample(min_count, random_state=42))
    .sample(frac=1, random_state=42)
    .reset_index(drop=True)
)

balanced.to_csv("data/passive_dataset.csv", index=False, encoding="utf-8-sig")

print("Dataset created successfully!")
print("Total rows:", len(balanced))
print(balanced["label"].value_counts())
print("Saved as data/passive_dataset.csv")