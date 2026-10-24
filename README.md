# Bike Sharing Data Analysis Dashboard

Dashboard interaktif untuk menganalisis pola peminjaman sepeda menggunakan dataset Bike Sharing (2011-2012).

## Pertanyaan Bisnis yang Dijawab

1. Bagaimana pola penggunaan sepeda per jam dalam sehari berdasarkan tipe pengguna (kasual vs terdaftar) pada hari kerja dan akhir pekan selama periode 2011-2012?
2. Faktor lingkungan apa (musim, kondisi cuaca, suhu) yang paling signifikan memengaruhi jumlah total peminjaman sepeda harian selama periode 2011-2012?

## Setup Environment

```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

```bash
cd submission
streamlit run dashboard/dashboard.py
```

Atau jika menjalankan dari dalam folder `submission`:
```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di browser pada alamat: `http://localhost:8501`

## Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv       # Data harian untuk dashboard
│   ├── hour_data.csv       # Data per jam untuk dashboard
│   └── dashboard.py        # Script Streamlit
├── data/
│   ├── day.csv             # Dataset harian original
│   └── hour.csv            # Dataset per jam original
├── notebook.ipynb          # Notebook analisis lengkap
├── README.md               # Dokumentasi ini
├── requirements.txt        # Daftar library
└── url.txt                 # URL deployment (jika dideploy)
```

## Sumber Dataset

Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg.
