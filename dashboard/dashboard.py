import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    day_df = pd.read_csv('dashboard/main_data.csv' if __import__('os').path.exists('dashboard/main_data.csv') else 'main_data.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df

@st.cache_data
def load_hour_data():
    hour_df = pd.read_csv('dashboard/hour_data.csv' if __import__('os').path.exists('dashboard/hour_data.csv') else 'hour_data.csv')
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return hour_df

day_df = load_data()
hour_df = load_hour_data()

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown("<div style='font-size:56px;text-align:center;'>🚲</div>", unsafe_allow_html=True)
st.sidebar.title("🚲 Bike Sharing")
st.sidebar.markdown("**Dashboard Analisis Data**")
st.sidebar.markdown("---")

# Filter Tahun
year_options = {'Semua Tahun': [0, 1], '2011': [0], '2012': [1]}
selected_year = st.sidebar.selectbox("📅 Pilih Tahun", list(year_options.keys()))
filtered_day = day_df[day_df['yr'].isin(year_options[selected_year])]
filtered_hour = hour_df[hour_df['yr'].isin(year_options[selected_year])]

# Filter Musim
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_options = ['Semua Musim'] + list(season_map.values())
selected_season = st.sidebar.selectbox("🌤️ Pilih Musim", season_options)
if selected_season != 'Semua Musim':
    rev_map = {v: k for k, v in season_map.items()}
    filtered_day = filtered_day[filtered_day['season'] == rev_map[selected_season]]
    filtered_hour = filtered_hour[filtered_hour['season'] == rev_map[selected_season]]

st.sidebar.markdown("---")
st.sidebar.markdown("**Tentang Dataset:**")
st.sidebar.info("Bike Sharing Dataset mencatat data peminjaman sepeda di Washington DC tahun 2011-2012.")

# ==========================================
# JUDUL UTAMA
# ==========================================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Analisis pola penggunaan layanan penyewaan sepeda berdasarkan waktu, cuaca, dan tipe pengguna.")
st.markdown("---")

# ==========================================
# METRIK UTAMA
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rentals = filtered_day['cnt'].sum()
    st.metric("Total Peminjaman", f"{total_rentals:,}", help="Total seluruh peminjaman sepeda")

with col2:
    avg_daily = filtered_day['cnt'].mean()
    st.metric("Rata-rata Harian", f"{avg_daily:.0f}", help="Rata-rata peminjaman per hari")

with col3:
    total_casual = filtered_day['casual'].sum()
    st.metric("Pengguna Kasual", f"{total_casual:,}", help="Total pengguna tidak terdaftar")

with col4:
    total_registered = filtered_day['registered'].sum()
    st.metric("Pengguna Terdaftar", f"{total_registered:,}", help="Total pengguna terdaftar")

st.markdown("---")

# ==========================================
# VISUALISASI 1: POLA PER JAM
# ==========================================
st.subheader("📊 Pertanyaan 1: Pola Peminjaman per Jam")
st.markdown("Bagaimana perbedaan pola peminjaman antara hari kerja dan akhir pekan?")

hourly_workday = filtered_hour[filtered_hour['workingday'] == 1].groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()
hourly_weekend = filtered_hour[filtered_hour['workingday'] == 0].groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()

fig1, axes = plt.subplots(1, 2, figsize=(14, 4))
fig1.patch.set_facecolor('#f8f9fa')

colors = {'casual': '#FF8C00', 'registered': '#1E90FF', 'cnt': '#2E8B57'}

ax1 = axes[0]
ax1.set_facecolor('#f8f9fa')
ax1.fill_between(hourly_workday['hr'], hourly_workday['casual'], alpha=0.4, color=colors['casual'], label='Kasual')
ax1.fill_between(hourly_workday['hr'], hourly_workday['registered'], alpha=0.4, color=colors['registered'], label='Terdaftar')
ax1.plot(hourly_workday['hr'], hourly_workday['cnt'], color=colors['cnt'], linewidth=2.5, label='Total', marker='o', markersize=4)
ax1.axvline(x=8, color='red', linestyle='--', alpha=0.7)
ax1.axvline(x=17, color='red', linestyle='--', alpha=0.7, label='Jam Puncak')
ax1.set_title('Hari Kerja', fontsize=12, fontweight='bold')
ax1.set_xlabel('Jam'); ax1.set_ylabel('Rata-rata Peminjaman')
ax1.set_xticks(range(0, 24, 2))
ax1.legend(fontsize=8); ax1.grid(True, alpha=0.3)

ax2 = axes[1]
ax2.set_facecolor('#f8f9fa')
ax2.fill_between(hourly_weekend['hr'], hourly_weekend['casual'], alpha=0.4, color=colors['casual'], label='Kasual')
ax2.fill_between(hourly_weekend['hr'], hourly_weekend['registered'], alpha=0.4, color=colors['registered'], label='Terdaftar')
ax2.plot(hourly_weekend['hr'], hourly_weekend['cnt'], color=colors['cnt'], linewidth=2.5, label='Total', marker='o', markersize=4)
ax2.axvspan(10, 16, alpha=0.1, color='green', label='Jam Ramai')
ax2.set_title('Akhir Pekan', fontsize=12, fontweight='bold')
ax2.set_xlabel('Jam'); ax2.set_ylabel('Rata-rata Peminjaman')
ax2.set_xticks(range(0, 24, 2))
ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig1)
plt.close()

col_a, col_b = st.columns(2)
with col_a:
    st.info("**Hari Kerja:** Puncak di jam 08.00 dan 17.00-18.00 (pola komuting). Pengguna terdaftar mendominasi.")
with col_b:
    st.info("**Akhir Pekan:** Pola merata jam 10.00-16.00 (pola rekreasi). Proporsi pengguna kasual lebih tinggi.")

st.markdown("---")

# ==========================================
# VISUALISASI 2: FAKTOR LINGKUNGAN
# ==========================================
st.subheader("🌤️ Pertanyaan 2: Pengaruh Faktor Lingkungan")
st.markdown("Bagaimana musim, cuaca, dan suhu memengaruhi jumlah peminjaman?")

weather_map_label = {1: 'Cerah/Sedikit Berawan', 2: 'Kabut/Berawan', 3: 'Hujan/Salju Ringan', 4: 'Hujan Lebat/Badai'}
filtered_day['season_label'] = filtered_day['season'].map(season_map)
filtered_day['weather_label'] = filtered_day['weathersit'].map(weather_map_label)
filtered_day['temp_celsius'] = filtered_day['temp'] * 41

fig2, axes2 = plt.subplots(1, 3, figsize=(15, 4))
fig2.patch.set_facecolor('#f8f9fa')

ax1 = axes2[0]
ax1.set_facecolor('#f8f9fa')
season_order = ['Spring', 'Summer', 'Fall', 'Winter']
season_avg = filtered_day.groupby('season_label')['cnt'].mean().reindex(season_order).dropna()
bars = ax1.bar(season_avg.index, season_avg.values,
               color=['#90EE90', '#FFD700', '#FF8C00', '#87CEEB'], edgecolor='white')
ax1.bar_label(bars, fmt='%.0f', padding=3, fontsize=9, fontweight='bold')
ax1.set_title('Peminjaman per Musim', fontsize=11, fontweight='bold')
ax1.set_xlabel('Musim'); ax1.set_ylabel('Rata-rata/Hari')
ax1.grid(axis='y', alpha=0.3)

ax2 = axes2[1]
ax2.set_facecolor('#f8f9fa')
weather_avg = filtered_day.groupby('weather_label')['cnt'].mean().sort_values(ascending=False)
bars2 = ax2.barh(weather_avg.index, weather_avg.values,
                  color=['#4CAF50', '#FFC107', '#F44336'][:len(weather_avg)], edgecolor='white')
ax2.bar_label(bars2, fmt='%.0f', padding=3, fontsize=9, fontweight='bold')
ax2.set_title('Peminjaman per Cuaca', fontsize=11, fontweight='bold')
ax2.set_xlabel('Rata-rata/Hari')
ax2.grid(axis='x', alpha=0.3)

ax3 = axes2[2]
ax3.set_facecolor('#f8f9fa')
ax3.scatter(filtered_day['temp_celsius'], filtered_day['cnt'],
            c=filtered_day['season'], cmap='RdYlGn', alpha=0.5, s=20, edgecolors='none')
if len(filtered_day) > 1:
    z = np.polyfit(filtered_day['temp_celsius'], filtered_day['cnt'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(filtered_day['temp_celsius'].min(), filtered_day['temp_celsius'].max(), 100)
    ax3.plot(x_line, p(x_line), 'r--', linewidth=2, label='Tren')
corr_val = filtered_day['temp_celsius'].corr(filtered_day['cnt'])
ax3.set_title('Suhu vs Peminjaman', fontsize=11, fontweight='bold')
ax3.set_xlabel('Suhu (C)'); ax3.set_ylabel('Total/Hari')
ax3.text(0.05, 0.92, f'r = {corr_val:.2f}', transform=ax3.transAxes,
         fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax3.legend(fontsize=8); ax3.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig2)
plt.close()

col_c, col_d, col_e = st.columns(3)
with col_c:
    if not filtered_day.empty:
        season_insight = filtered_day.groupby('season_label')['cnt'].mean().sort_values(ascending=False)
        if len(season_insight) >= 2:
            highest_season = season_insight.index[0]
            lowest_season = season_insight.index[-1]
            if selected_season == 'Semua Musim':
                st.success(f"**Musim:** Rata-rata peminjaman tertinggi pada {highest_season} dan terendah pada {lowest_season}.")
            else:
                st.success(f"**Musim terpilih:** {selected_season}; rata-rata {season_insight.iloc[0]:,.0f} peminjaman per hari.")
        else:
            st.success(f"**Musim terpilih:** {selected_season}; data tersedia untuk analisis.")
    else:
        st.info("Tidak ada data untuk kombinasi filter ini.")
with col_d:
    st.success("**Cuaca:** Cerah 2x lebih tinggi dari hujan ringan.")
with col_e:
    st.success(f"**Suhu:** Korelasi positif kuat (r={corr_val:.2f}) dengan peminjaman.")

st.markdown("---")

# ==========================================
# TREN BULANAN
# ==========================================
st.subheader("📈 Tren Peminjaman Bulanan")

monthly = filtered_day.groupby(['yr', 'mnth'])['cnt'].mean().reset_index()
monthly['year_label'] = monthly['yr'].map({0: '2011', 1: '2012'})

fig3, ax = plt.subplots(figsize=(12, 4))
fig3.patch.set_facecolor('#f8f9fa')
ax.set_facecolor('#f8f9fa')

month_names = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
colors_yr = {'2011': '#1E90FF', '2012': '#FF8C00'}

for yr_label, grp in monthly.groupby('year_label'):
    ax.plot(grp['mnth'], grp['cnt'], marker='o', linewidth=2.5,
            markersize=7, label=f'Tahun {yr_label}', color=colors_yr.get(yr_label, 'gray'))

ax.set_title('Tren Rata-rata Peminjaman per Bulan', fontsize=12, fontweight='bold')
ax.set_xlabel('Bulan'); ax.set_ylabel('Rata-rata Peminjaman/Hari')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig3)
plt.close()

st.markdown("---")
st.markdown("**Sumber Data:** Bike Sharing Dataset (Fanaee-T, Hadi, and Gama, Joao, 2014) | Dashboard dibuat untuk proyek akhir Dicoding")
