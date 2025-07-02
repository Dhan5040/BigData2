import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import numpy as np

st.set_page_config(page_title="🧠 AI Tools in Education", layout="wide")
st.title("🎓 Dashboard: Penggunaan AI Tools oleh Mahasiswa")

# Load data
df = pd.read_csv("Students.csv")
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Sidebar filter controls
st.sidebar.header("🔍 Filter Data")

# Filter jurusan (Stream)
stream_options = df['Stream'].unique()
selected_streams = st.sidebar.multiselect("Pilih Jurusan (Stream)", options=stream_options, default=stream_options)

# Filter tahun studi
year_options = df['Year_of_Study'].unique()
selected_years = st.sidebar.multiselect("Pilih Tahun Studi", options=year_options, default=year_options)

# Filter AI tools favorit
ai_tools_options = df['Preferred_AI_Tool'].unique()
selected_tools = st.sidebar.multiselect("Pilih AI Tools Favorit", options=ai_tools_options, default=ai_tools_options)

# Filter data berdasarkan input user
filtered_df = df[
    (df['Stream'].isin(selected_streams)) &
    (df['Year_of_Study'].isin(selected_years)) &
    (df['Preferred_AI_Tool'].isin(selected_tools))
]

# Overview
st.subheader("📋 Ringkasan Data (Filtered)")
col1, col2 = st.columns(2)
with col1:
    st.metric("Jumlah Mahasiswa", filtered_df.shape[0])
with col2:
    st.metric("Jumlah AI Tools Berbeda", filtered_df["Preferred_AI_Tool"].nunique())

st.dataframe(filtered_df.head(10))

st.markdown("---")

# ========== 1. Distribusi Jurusan ==========
st.subheader("🎓 1. Distribusi Stream / Jurusan")
fig1 = px.histogram(filtered_df, x='Stream', color='Year_of_Study', barmode='group')
st.plotly_chart(fig1)
st.info("Insight: Jurusan terbanyak didominasi oleh tahun kedua dan ketiga.")

# ========== 2. Preferred AI Tool ==========
st.subheader("🤖 2. AI Tool Favorit Mahasiswa")
fig2 = px.pie(filtered_df, names='Preferred_AI_Tool', title="Preferred AI Tool", hole=0.4)
st.plotly_chart(fig2)
st.info("Insight: Terlihat bahwa ChatGPT mendominasi sebagai AI tool yang paling banyak digunakan.")

# ========== 3. WordCloud Use Cases ==========
st.subheader("📚 3. WordCloud: Use Case AI")
text = " ".join(filtered_df["Use_Cases"].dropna().astype(str))
if text.strip():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig3, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig3)
else:
    st.warning("Tidak ada data Use Cases yang tersedia untuk filter ini.")
st.info("Insight: Use cases yang umum termasuk coding, summarizing, writing dan research.")

# ========== 4. Daily Usage Hours ==========
st.subheader("⏱️ 4. Penggunaan AI Tools Harian")
fig4 = px.histogram(filtered_df, x="Daily_Usage_Hours", nbins=10, color="Year_of_Study")
st.plotly_chart(fig4)
st.info("Insight: Mayoritas mahasiswa menggunakan AI tools antara 1–3 jam per hari.")

# ========== 5. Trust vs Impact ==========
st.subheader("📈 5. Trust in AI Tools vs Impact on Grades")
fig5 = px.box(filtered_df, x="Impact_on_Grades", y="Trust_in_AI_Tools", color="Impact_on_Grades")
st.plotly_chart(fig5)
st.info("Insight: Mahasiswa yang merasakan dampak positif pada nilai cenderung memiliki tingkat kepercayaan lebih tinggi terhadap AI tools.")

# ========== 6. Apakah Diperbolehkan oleh Dosen? ==========
st.subheader("👨‍🏫 6. Apakah Dosen Membolehkan AI Tools?")
fig6 = px.histogram(filtered_df, x="Do_Professors_Allow_Use", color="Stream", barmode="group")
st.plotly_chart(fig6)
st.info("Insight: Beberapa jurusan memiliki toleransi dosen yang lebih tinggi terhadap penggunaan AI.")

# ========== 7. Kesediaan Membayar ==========
st.subheader("💸 7. Kesediaan Membayar Akses AI Tools")
fig7 = px.pie(filtered_df, names="Willing_to_Pay_for_Access", title="Willingness to Pay")
st.plotly_chart(fig7)
st.info("Insight: Sebagian besar mahasiswa masih ragu untuk membayar akses ke AI tools.")

# ========== 8. Tingkat Kesadaran AI ==========
st.subheader("🧠 8. Tingkat Kesadaran AI")
fig8 = px.histogram(filtered_df, x="Awareness_Level", color="Year_of_Study", barmode="group")
st.plotly_chart(fig8)
st.info("Insight: Mahasiswa tahun akhir memiliki tingkat kesadaran AI yang relatif tinggi.")

# ========== 9. Perangkat yang Digunakan ==========
st.subheader("💻 9. Perangkat yang Digunakan")
fig9 = px.pie(filtered_df, names="Device_Used", title="Device Digunakan untuk Akses AI")
st.plotly_chart(fig9)
st.info("Insight: Mayoritas mahasiswa menggunakan laptop, namun ponsel juga umum.")

# ========== 10. Akses Internet ==========
st.subheader("🌐 10. Akses Internet vs Daily Usage")
fig10 = px.box(filtered_df, x="Internet_Access", y="Daily_Usage_Hours", color="Internet_Access")
st.plotly_chart(fig10)
st.info("Insight: Akses internet sangat memengaruhi durasi penggunaan harian AI tools.")

# ========== Ringkasan ==========
st.markdown("---")
st.subheader("📌 Insight Umum")
st.markdown("""
- 💡 Mahasiswa menggunakan AI paling sering untuk coding dan writing.
- 💡 ChatGPT adalah tool paling populer, namun Gemini dan Claude mulai muncul.
- 💡 Tingkat kepercayaan terhadap AI berkorelasi dengan dampak positif terhadap nilai.
- 💡 Sebagian besar masih ragu untuk membayar akses premium.
- 💡 Penggunaan tinggi terutama pada jurusan teknologi dan tahun akhir.
""")
