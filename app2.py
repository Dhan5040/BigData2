import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
import numpy as np

# Setup
st.set_page_config(page_title="🎓 Student Dashboard", layout="wide")
st.title("🎓 Student Results Dashboard - Interaktif & Eksploratif")

# Load data
df = pd.read_csv("Students.csv")

# Preprocessing
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = df.select_dtypes(include='object').columns

st.markdown("## 1️⃣ Statistik Awal & Ringkasan")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Jumlah Siswa", df.shape[0])
col2.metric("Kolom Numerik", len(numeric_cols))
col3.metric("Kolom Kategori", len(categorical_cols))
col4.metric("Skor Rata-rata", round(df['score'].mean(), 2))

st.markdown("---")

# ===============================
# 1. Distribusi Nilai (Histogram)
# ===============================
st.markdown("### 📊 Visual 1: Distribusi Nilai")
fig = px.histogram(df, x="score", nbins=20, color="gender", marginal="box",
                   color_discrete_map={'female':'#e377c2','male':'#1f77b4'})
st.plotly_chart(fig, use_container_width=True)
st.info("Insight: Sebagian besar siswa memiliki nilai antara 60 dan 80. Distribusi agak skew ke kiri.")

# ===============================
# 2. Pie Chart Gender
# ===============================
st.markdown("### 👥 Visual 2: Distribusi Gender (Pie Chart)")
fig2 = px.pie(df, names='gender', title='Distribusi Gender',
              color_discrete_map={'female':'#e377c2','male':'#1f77b4'})
st.plotly_chart(fig2)
st.info("Insight: Data relatif seimbang antara siswa laki-laki dan perempuan.")

# ===============================
# 3. Barplot Education Parent
# ===============================
st.markdown("### 🎓 Visual 3: Level Pendidikan Orang Tua")
fig3 = px.bar(df['parental level of education'].value_counts().reset_index(),
              x='index', y='parental level of education',
              color='index', title='Distribusi Level Pendidikan Orang Tua')
st.plotly_chart(fig3)
st.info("Insight: Sebagian besar orang tua siswa memiliki pendidikan associate's degree atau high school.")

# ===============================
# 4. Boxplot Test Preparation vs Score
# ===============================
st.markdown("### 📘 Visual 4: Kursus Persiapan vs Skor (Boxplot)")
fig4 = px.box(df, x="test preparation course", y="score", color="test preparation course",
              title="Pengaruh Kursus Persiapan terhadap Nilai")
st.plotly_chart(fig4)
st.info("Insight: Siswa yang menyelesaikan kursus persiapan cenderung memiliki skor lebih tinggi.")

# ===============================
# 5. Violin Plot Gender vs Score
# ===============================
st.markdown("### 🎻 Visual 5: Gender vs Score (Violin)")
fig5 = px.violin(df, x="gender", y="score", box=True, color="gender",
                 color_discrete_map={'female':'#e377c2','male':'#1f77b4'})
st.plotly_chart(fig5)
st.info("Insight: Distribusi skor perempuan lebih terkonsentrasi di skor tinggi dibanding laki-laki.")

# ===============================
# 6. Scatter Plot dengan Korelasi
# ===============================
st.markdown("### 📍 Visual 6: Scatter & Korelasi")
num_x = st.selectbox("Pilih variabel numerik untuk X:", numeric_cols)
fig6 = px.scatter(df, x=num_x, y="score", trendline="ols", color="gender")
st.plotly_chart(fig6)
st.info(f"Insight: Terdapat hubungan antara {num_x} dan skor, terlihat dari trendline.")

# ===============================
# 7. Korelasi Heatmap
# ===============================
st.markdown("### 🔥 Visual 7: Korelasi Numerik")
fig7, ax = plt.subplots()
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig7)
st.info("Insight: Korelasi tertinggi terjadi antara skor dan variabel terkait ujian atau pendidikan.")

# ===============================
# 8. Countplot Semua Kolom Kategori
# ===============================
st.markdown("### 📦 Visual 8: Eksplorasi Kategori")
cat_selected = st.selectbox("Pilih kolom kategori:", categorical_cols)
fig8, ax = plt.subplots()
sns.countplot(data=df, x=cat_selected, order=df[cat_selected].value_counts().index, palette='pastel')
plt.xticks(rotation=45)
ax.set_title(f"Distribusi {cat_selected}")
st.pyplot(fig8)
st.info(f"Insight: Distribusi {cat_selected} menunjukkan preferensi yang dapat memengaruhi hasil belajar.")

# ===============================
# 9. WordCloud
# ===============================
st.markdown("### ☁️ Visual 9: WordCloud")
wc_text = " ".join(df[cat_selected].astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(wc_text)
fig9, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig9)
st.info(f"Insight: WordCloud menggambarkan dominasi nilai dalam '{cat_selected}' yang sering muncul.")

# ===============================
# 10. Distribusi Score per Education Level
# ===============================
st.markdown("### 🎯 Visual 10: Score berdasarkan Pendidikan Orang Tua")
fig10 = px.box(df, x="parental level of education", y="score", color="gender")
fig10.update_layout(xaxis_title="Pendidikan Orang Tua", yaxis_title="Score")
st.plotly_chart(fig10)
st.info("Insight: Siswa dengan orang tua berpendidikan tinggi cenderung mendapat skor lebih tinggi.")

# ===============================
# 💡 Insight Ringkasan
# ===============================
st.markdown("---")
st.subheader("🧠 Kesimpulan dan Insight Utama")

st.markdown("""
- Kursus persiapan memiliki pengaruh signifikan terhadap skor siswa.
- Perempuan secara umum menunjukkan distribusi skor yang lebih baik.
- Pendidikan orang tua juga berkorelasi dengan skor siswa.
- Distribusi gender dan latar belakang cukup seimbang, memungkinkan analisis adil.
- Korelasi antar variabel numerik cukup rendah, menandakan skor dipengaruhi oleh kategori/psikologis/eksternal.
""")

st.caption("Dashboard terinspirasi dari Kaggle EDA by Joshua Swords. Dibuat oleh NMAA x ChatGPT")
