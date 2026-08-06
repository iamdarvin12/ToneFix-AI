import joblib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from datetime import datetime

model = joblib.load("model/tone_model.pkl")
embedder = joblib.load("model/embedder.pkl")

st.set_page_config(
    page_title="ToneFix AI",
    page_icon="💬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 45%, #dbeafe 100%);
    color: #0f172a;
}

html, body, p, span, div, label {
    color: #0f172a !important;
}

h1, h2, h3, h4 {
    color: #0f172a !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #e0f2fe);
    border-right: 1px solid #bfdbfe;
}

[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

.hero {
    background: linear-gradient(135deg, #2563eb, #0ea5e9);
    padding: 32px;
    border-radius: 28px;
    box-shadow: 0px 12px 35px rgba(37,99,235,0.25);
    margin-bottom: 25px;
}

.hero h1, .hero h2, .hero h3, .hero p {
    color: white !important;
}

.card {
    background: rgba(255,255,255,0.96);
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #bfdbfe;
    box-shadow: 0px 8px 25px rgba(15,23,42,0.08);
    margin-bottom: 18px;
}

.result-passive {
    background: #fee2e2;
    padding: 22px;
    border-radius: 22px;
    border-left: 8px solid #ef4444;
}

.result-positive {
    background: #dcfce7;
    padding: 22px;
    border-radius: 22px;
    border-left: 8px solid #22c55e;
}

.result-neutral {
    background: #fef9c3;
    padding: 22px;
    border-radius: 22px;
    border-left: 8px solid #eab308;
}

.rewrite {
    background: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #bfdbfe;
    box-shadow: 0px 6px 18px rgba(37,99,235,0.10);
    margin-bottom: 14px;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    box-shadow: 0px 5px 18px rgba(15,23,42,0.07);
}

[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 900 !important;
}

textarea {
    background: white !important;
    color: #0f172a !important;
    border-radius: 18px !important;
    border: 1px solid #93c5fd !important;
}

label {
    font-weight: 800 !important;
    color: #1e293b !important;
    font-size: 15px !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 14px !important;
    border: 2px solid #3b82f6 !important;
    font-weight: 700 !important;
    box-shadow: 0px 4px 12px rgba(59,130,246,0.18);
}

div[data-baseweb="select"] span {
    color: #0f172a !important;
}

ul[role="listbox"] {
    background-color: #ffffff !important;
    border-radius: 14px !important;
}

li[role="option"] {
    color: #0f172a !important;
    background-color: #ffffff !important;
    font-weight: 600 !important;
}

li[role="option"]:hover {
    background-color: #3b82f6 !important;
    color: white !important;
}

li[aria-selected="true"] {
    background-color: #2563eb !important;
    color: white !important;
}

.stButton button {
    background: linear-gradient(135deg, #2563eb, #0ea5e9);
    color: white !important;
    font-weight: 800;
    border-radius: 14px;
    padding: 0.7rem 1.4rem;
    border: none;
    box-shadow: 0px 6px 18px rgba(37,99,235,0.25);
}

.stDownloadButton button {
    background: #0f172a !important;
    color: white !important;
    border-radius: 14px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []


def rule_score(text):
    t = text.lower()

    patterns = {
        "late_reply": ["tak reply", "tak balas", "tak jawab", "baru reply", "tak respon"],
        "delay": ["lambat", "tunggu", "dari tadi", "dari pagi", "dari semalam", "lewat"],
        "workload": ["buat sendiri", "sorang", "sorang je", "handle semua", "cover semua"],
        "comparison": ["semua orang", "tinggal awak", "kecuali awak", "orang lain dah"],
        "sarcasm": ["baguslah", "hebatlah", "wah", "akhirnya", "menarik juga"],
        "soft_attack": ["mungkin awak sibuk", "terlepas pandang", "tak apa lah", "takpelah", "ikut awak", "terpulang"],
        "last_minute": ["last minute", "baru bagitahu", "baru update", "baru nak inform"]
    }

    score = 0
    matched = []

    for category, words in patterns.items():
        for word in words:
            if word in t:
                score += 12
                matched.append(word)

    if "terima kasih" in t and ("tak" in t or "lambat" in t or "last minute" in t):
        score += 25
        matched.append("terima kasih + aduan")

    if "saya dah" in t and ("follow up" in t or "tunggu" in t or "hantar" in t):
        score += 25
        matched.append("saya dah + kekecewaan")

    if "semua orang" in t and ("awak" in t or "tinggal" in t or "kecuali" in t):
        score += 25
        matched.append("perbandingan sosial")

    return min(score, 100), list(dict.fromkeys(matched))


def detect_tone(text):
    vec = embedder.encode([text])
    probs = model.predict_proba(vec)[0]
    classes = model.classes_
    result = dict(zip(classes, probs))

    ml_positive = result.get("positive", 0) * 100
    ml_neutral = result.get("neutral", 0) * 100
    ml_passive = result.get("passive aggressive", 0) * 100

    rules, matched = rule_score(text)

    passive = (ml_passive * 0.70) + (rules * 0.30)
    positive = ml_positive
    neutral = ml_neutral

    if rules >= 45:
        passive = max(passive, 65)

    total = positive + neutral + passive

    if total > 0:
        positive = (positive / total) * 100
        neutral = (neutral / total) * 100
        passive = (passive / total) * 100

    scores = {
        "Positif": positive,
        "Neutral": neutral,
        "Pasif Agresif": passive
    }

    final = max(scores, key=scores.get)
    confidence = max(scores.values())

    return final, positive, neutral, passive, confidence, rules, matched


def issue_type(text):
    t = text.lower()

    if any(x in t for x in ["reply", "balas", "jawab", "respon"]):
        return "Masalah balasan mesej"

    if any(x in t for x in ["tunggu", "lambat", "lewat", "dari tadi", "dari pagi"]):
        return "Masalah kelewatan"

    if any(x in t for x in ["buat sendiri", "sorang", "handle semua", "cover semua"]):
        return "Masalah pembahagian kerja"

    if any(x in t for x in ["semua orang", "tinggal awak", "kecuali awak"]):
        return "Masalah kerjasama kumpulan"

    if any(x in t for x in ["follow up", "terlepas pandang", "saya dah hantar"]):
        return "Masalah susulan komunikasi"

    if any(x in t for x in ["last minute", "baru update", "baru bagitahu"]):
        return "Masalah makluman lewat"

    return "Isu komunikasi umum"


def smart_rewrite(text, label):
    issue = issue_type(text)

    if label == "Pasif Agresif":
        if issue == "Masalah balasan mesej":
            return {
                "sebab": "Mesej ini menunjukkan kekecewaan kerana mesej tidak dibalas atau lambat mendapat maklum balas.",
                "sopan": "Boleh balas mesej saya apabila ada masa? Saya cuma mahu pastikan perkara ini tidak terlepas.",
                "profesional": "Saya ingin membuat susulan berkenaan mesej sebelum ini. Mohon maklum balas apabila berkesempatan.",
                "mesra": "Hi, bila free nanti boleh reply mesej saya ya 😊"
            }

        if issue == "Masalah kelewatan":
            return {
                "sebab": "Mesej ini menunjukkan ketidakpuasan terhadap kelewatan atau masa menunggu yang lama.",
                "sopan": "Boleh beri sedikit kemas kini apabila ada masa supaya saya tahu perkembangan semasa?",
                "profesional": "Saya ingin mendapatkan perkembangan terkini berkaitan perkara ini bagi memastikan perancangan berjalan lancar.",
                "mesra": "Hi, boleh update sikit ya? Senang kita sambung kerja sama-sama 😊"
            }

        if issue == "Masalah pembahagian kerja":
            return {
                "sebab": "Mesej ini menunjukkan rasa terbeban kerana kerja seolah-olah dilakukan seorang diri.",
                "sopan": "Kalau awak sibuk, boleh beritahu saya supaya kita boleh susun pembahagian kerja dengan lebih baik.",
                "profesional": "Saya mencadangkan kita menyelaraskan semula pembahagian tugasan supaya kerja dapat disiapkan secara seimbang.",
                "mesra": "Kalau tak sempat, bagitahu je ya. Kita boleh bahagi kerja sama-sama 😊"
            }

        if issue == "Masalah kerjasama kumpulan":
            return {
                "sebab": "Mesej ini memberi tekanan secara tidak langsung dengan membandingkan penerima dengan orang lain.",
                "sopan": "Boleh semak bahagian awak apabila ada masa supaya kerja kumpulan dapat berjalan lancar?",
                "profesional": "Mohon kemas kini status bahagian tugasan agar keseluruhan kerja kumpulan dapat diselaraskan dengan baik.",
                "mesra": "Hi, boleh update bahagian awak sikit? Senang kita semua teruskan kerja 😊"
            }

        if issue == "Masalah susulan komunikasi":
            return {
                "sebab": "Mesej ini menunjukkan susulan yang membawa rasa kecewa kerana perkara tersebut mungkin belum diberi perhatian.",
                "sopan": "Saya ingin membuat susulan semula. Boleh semak mesej saya apabila ada masa?",
                "profesional": "Saya ingin membuat susulan berkenaan perkara ini dan memohon maklum balas apabila berkesempatan.",
                "mesra": "Hi, saya follow up semula ya. Bila free nanti boleh tengok mesej saya 😊"
            }

        if issue == "Masalah makluman lewat":
            return {
                "sebab": "Mesej ini menunjukkan rasa tidak puas hati kerana maklumat diberikan terlalu lewat.",
                "sopan": "Boleh maklumkan perkara seperti ini lebih awal selepas ini supaya kita dapat bersedia dengan baik?",
                "profesional": "Saya berharap makluman dapat diberikan lebih awal pada masa akan datang bagi memudahkan perancangan.",
                "mesra": "Next time kalau boleh bagitahu awal sikit ya, senang kita plan sama-sama 😊"
            }

        return {
            "sebab": "Mesej ini mempunyai unsur sindiran atau kekecewaan secara tidak langsung.",
            "sopan": "Boleh semak perkara ini apabila ada masa?",
            "profesional": "Saya ingin mendapatkan kemas kini mengenai perkara ini.",
            "mesra": "Hi, boleh update sikit tentang perkara ini 😊"
        }

    if label == "Positif":
        return {
            "sebab": "Mesej ini menunjukkan nada yang baik, sopan dan menghargai penerima.",
            "sopan": "Mesej ini sudah sesuai digunakan.",
            "profesional": "Mesej ini sudah jelas dan profesional.",
            "mesra": "Mesej ini sudah mesra dan positif 👍"
        }

    return {
        "sebab": "Mesej ini bersifat neutral dan tidak menunjukkan emosi yang terlalu kuat.",
        "sopan": "Mesej ini boleh digunakan seperti biasa.",
        "profesional": "Mesej ini sudah sesuai untuk komunikasi formal.",
        "mesra": "Mesej ini okay dan tidak berbunyi kasar 😊"
    }


def communication_score(label, passive):
    if label == "Positif":
        return 92
    if label == "Neutral":
        return 74
    return max(20, int(100 - passive))


st.sidebar.markdown("## 💬 ToneFix AI")
st.sidebar.write("Sistem pengesan nada mesej dan pembaikan komunikasi.")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "🏠 Laman Utama",
        "💬 Pemeriksa Nada",
        "📊 Papan Pemuka",
        "📚 Sejarah Analisis",
        "ℹ️ Tentang Sistem"
    ]
)

if menu == "🏠 Laman Utama":
    st.markdown("""
    <div class="hero">
        <h1>💬 ToneFix AI</h1>
        <h3>Sistem Pengesan Nada Pasif-Agresif dan Penulis Semula Mesej Positif</h3>
        <p>Membantu pengguna mengenal pasti nada mesej dan memperbaiki komunikasi secara lebih sopan, profesional dan mesra.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h3>🎯 Pengesanan Nada</h3>
        <p>Menggabungkan model pembelajaran mesin dan peraturan bahasa untuk mengesan nada mesej.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <h3>🧠 Penjelasan</h3>
        <p>Memberi sebab kenapa sesuatu mesej diklasifikasikan sebagai positif, neutral atau pasif-agresif.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        <h3>✨ Penambahbaikan</h3>
        <p>Mencadangkan ayat yang lebih sopan, profesional dan mesra berdasarkan isu komunikasi.</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "💬 Pemeriksa Nada":
    st.markdown("""
    <div class="hero">
        <h1>💬 Pemeriksa Nada Mesej</h1>
        <p>Masukkan mesej anda dan sistem akan menganalisis nada serta mencadangkan versi yang lebih baik.</p>
    </div>
    """, unsafe_allow_html=True)

    context = st.selectbox(
        "Pilih konteks mesej:",
        ["Umum", "Tugasan kumpulan", "Kawan", "Tempat kerja", "Hubungan", "Media sosial"]
    )

    text = st.text_area(
        "Masukkan mesej:",
        height=150,
        placeholder="Contoh: Saya bukan nak paksa, tapi semua orang tengah tunggu bahagian awak."
    )

    if st.button("🔍 Analisis Nada"):
        if text.strip() == "":
            st.warning("Sila masukkan mesej terlebih dahulu.")
        else:
            final, positive, neutral, passive, confidence, rule_value, matched = detect_tone(text)
            rewrite = smart_rewrite(text, final)
            score = communication_score(final, passive)
            issue = issue_type(text)

            st.markdown("## 📊 Keputusan Analisis")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Positif", f"{positive:.1f}%")
            col2.metric("Neutral", f"{neutral:.1f}%")
            col3.metric("Pasif Agresif", f"{passive:.1f}%")
            col4.metric("Keyakinan", f"{confidence:.1f}%")

            if final == "Pasif Agresif":
                st.markdown("""
                <div class="result-passive">
                <h3>😏 Nada Dikesan: Pasif Agresif</h3>
                <p>Mesej ini mungkin mengandungi sindiran, kekecewaan atau tekanan emosi secara tidak langsung.</p>
                </div>
                """, unsafe_allow_html=True)
            elif final == "Positif":
                st.markdown("""
                <div class="result-positive">
                <h3>😊 Nada Dikesan: Positif</h3>
                <p>Mesej ini kedengaran baik, sopan dan menghargai penerima.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-neutral">
                <h3>😐 Nada Dikesan: Neutral</h3>
                <p>Mesej ini bersifat biasa dan tidak menunjukkan emosi yang terlalu kuat.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 🔍 Jenis Isu")
            st.info(issue)

            st.markdown("### 🧩 Petunjuk Bahasa Dikesan")
            if matched:
                st.write(", ".join(matched))
            else:
                st.write("Tiada petunjuk bahasa khusus yang kuat dikesan.")

            st.markdown("### 📈 Graf Analisis")
            chart_data = pd.DataFrame({
                "Nada": ["Positif", "Neutral", "Pasif Agresif"],
                "Peratus": [positive, neutral, passive]
            })

            fig, ax = plt.subplots()
            ax.bar(chart_data["Nada"], chart_data["Peratus"])
            ax.set_ylabel("Peratus (%)")
            ax.set_ylim(0, 100)
            st.pyplot(fig)

            st.markdown("### 📊 Skor Komunikasi")
            st.progress(score / 100)
            st.write(f"Skor komunikasi: **{score}/100**")

            st.markdown("### 🧠 Sebab Pengesanan")
            st.write(rewrite["sebab"])

            st.markdown("### ✨ Cadangan Ayat Lebih Baik")

            st.markdown(f"""
            <div class="rewrite">
            <h4>🌱 Versi Sopan</h4>
            <p>{rewrite["sopan"]}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="rewrite">
            <h4>💼 Versi Profesional</h4>
            <p>{rewrite["profesional"]}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="rewrite">
            <h4>😊 Versi Mesra</h4>
            <p>{rewrite["mesra"]}</p>
            </div>
            """, unsafe_allow_html=True)

            before, after = st.columns(2)
            with before:
                st.error(f"❌ Mesej Asal:\n\n{text}")
            with after:
                st.success(f"✅ Cadangan Terbaik:\n\n{rewrite['mesra']}")

            st.session_state.history.append({
                "masa": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mesej": text,
                "konteks": context,
                "nada": final,
                "positif": round(positive, 2),
                "neutral": round(neutral, 2),
                "pasif_agresif": round(passive, 2),
                "keyakinan": round(confidence, 2),
                "skor": score,
                "isu": issue,
                "petunjuk": ", ".join(matched) if matched else "-"
            })

elif menu == "📊 Papan Pemuka":
    st.markdown("""
    <div class="hero">
        <h1>📊 Papan Pemuka Analisis</h1>
        <p>Ringkasan analisis mesej yang telah diuji dalam sistem.</p>
    </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.history) == 0:
        st.info("Belum ada data. Sila analisis mesej dahulu.")
    else:
        df = pd.DataFrame(st.session_state.history)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Jumlah Mesej", len(df))
        c2.metric("Positif", len(df[df["nada"] == "Positif"]))
        c3.metric("Neutral", len(df[df["nada"] == "Neutral"]))
        c4.metric("Pasif Agresif", len(df[df["nada"] == "Pasif Agresif"]))

        st.markdown("### Taburan Nada")
        counts = df["nada"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts, labels=counts.index, autopct="%1.1f%%")
        ax.axis("equal")
        st.pyplot(fig)

        st.markdown("### Skor Komunikasi Mengikut Analisis")
        st.line_chart(df["skor"])

elif menu == "📚 Sejarah Analisis":
    st.markdown("""
    <div class="hero">
        <h1>📚 Sejarah Analisis</h1>
        <p>Rekod mesej yang telah dianalisis dalam sesi ini.</p>
    </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.history) == 0:
        st.info("Belum ada sejarah analisis.")
    else:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Muat Turun CSV",
            csv,
            "sejarah_tonefix_ai.csv",
            "text/csv"
        )

        if st.button("🗑 Padam Sejarah"):
            st.session_state.history = []
            st.rerun()

elif menu == "ℹ️ Tentang Sistem":
    st.markdown("""
    <div class="hero">
        <h1>ℹ️ Tentang ToneFix AI</h1>
        <p>Sistem sokongan komunikasi untuk mengesan dan memperbaiki nada mesej.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Nama Sistem</h3>
    <p><b>ToneFix AI: Sistem Pengesan Nada Pasif-Agresif dan Penulis Semula Mesej Positif</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Objektif Sistem</h3>
    <p>
    Sistem ini dibangunkan untuk membantu pengguna mengenal pasti nada mesej,
    memahami sebab sesuatu mesej boleh dianggap pasif-agresif, dan memperbaiki mesej
    kepada versi yang lebih sopan, profesional dan mesra.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Teknologi Digunakan</h3>
    <p>
    Sistem ini menggunakan model pembelajaran mesin, penyulaman ayat,
    enjin peraturan bahasa, Python dan Streamlit.
    </p>
    </div>
    """, unsafe_allow_html=True)