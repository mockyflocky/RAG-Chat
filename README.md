# RAG-Chat
PDF Chat &amp; AI Assistant **yang Running Secara Lokal** memungkinkan pengguna mengunggah PDF untuk bertanya terkait isi dokumen atau berinteraksi langsung dengan AI tanpa PDF. PDF Chat mengekstrak informasi dari dokumen untuk jawaban akurat, cocok untuk membaca laporan atau penelitian. AI Assistant menjawab berbagai pertanyaan.

# Install Ollama 
kemudian pull model, bisa cek di library ollama sedot secukupnya sesuaikan dengan spek hardware.<br>
```ollama pull llama3.2``` atau ```ollama pull deepseek-r1```
Check model
```ollama ls```

# Install Ramuan
daftar pustaka (libraries) dan dependensi yang dibutuhkan agar proyek dapat berjalan dengan benar<br>
```pip install -r requirements.txt```

# Jalankan Streamlit
sebagai frontend yang paling ciamik, namun banyak framework alternatif lain yang bisa dipakai (FastAPI / Flask) tinggal di ganti headernya from --- import ---<br>
```streamlit run pdf_rag.py```

# Other Option
Karena berjalan di lokal ada baiknya menggunakan Virtual Environment (Venv) utk menghindari konflik dependensi **Menjaga Kebersihan rumah   Python**
