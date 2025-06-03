<p align="center">
  <img src="URL_GAMBAR_BANNER" alt="Smart City Bengkulu" width="100%" />
</p>

# 🚦 Smart City: Sistem Prediksi & Navigasi Kemacetan Bengkulu

Proyek ini merupakan bagian dari pengembangan sistem Smart City untuk Kota Bengkulu. Sistem ini bertujuan memberikan **peringatan dini terhadap kemacetan lalu lintas** dan merekomendasikan **rute alternatif** secara visual melalui peta interaktif.

## 📌 Studi Kasus

> Kota Bengkulu ingin mengembangkan sistem navigasi cerdas berbasis AI yang dapat memprediksi dan memperingatkan kemacetan secara visual, serta memberikan rekomendasi rute alternatif kepada masyarakat secara interaktif dan informatif.

---

## 🧠 Model AI yang Digunakan: Algoritma Dijkstra + Penalti Kemacetan

🔍 **Prediksi Kemacetan**
Menggunakan dua model pembelajaran mesin untuk memprediksi tingkat kepadatan lalu lintas:

* **Random Forest Regressor**
  Cocok untuk data tabular dan statis. Memberikan prediksi cepat dan akurat terhadap kondisi jalan pada waktu tertentu.

* **LSTM (Long Short-Term Memory)**
  Digunakan untuk data deret waktu (time series) seperti volume kendaraan per jam/menit. Mampu mengenali pola jangka panjang dalam data historis lalu lintas.

🛍️ **Navigasi Rute**
Menggunakan algoritma:

* **Dijkstra**
  Efisien untuk mencari jalur terpendek dari titik awal ke tujuan.
  → Dimodifikasi dengan penalti kemacetan untuk memprioritaskan jalan yang lebih lancar.

---

## 📊 Jenis, Sumber Data, dan Preprocessing

* **Data jalan**: OpenStreetMap (diakses dengan `osmnx`)
* **Geolokasi pengguna**: Lokasi awal & tujuan dimasukkan manual lalu dikonversi menjadi koordinat dengan geopy
* **Kemacetan**: **Data dummy** yang disimulasikan berdasarkan node tertentu secara statis

### 📌 Catatan tentang data dummy:

> Kemacetan tidak diambil dari sumber real-time. Data ini **hanya simulasi** dan tidak mencerminkan kondisi aktual di Kota Bengkulu. Diperlukan integrasi API eksternal untuk mendukung prediksi kemacetan nyata.

---

## 📈 Strategi Evaluasi Model dan Performa Sistem

Untuk mengevaluasi performa sistem prediksi kemacetan lalu lintas berbasis AI yang terintegrasi dengan peta interaktif, kami melakukan **lima kali percobaan** dengan lokasi atau kondisi berbeda pada setiap percobaan (Percobaan ke-1 hingga Percobaan ke-5).

Setiap percobaan mengukur efisiensi pemuatan peta, visualisasi data kemacetan, serta performa fitur interaktif.

### 🔮 2. Strategi Evaluasi

* Mengukur **Total Execution Time (TET)** dari awal pemuatan peta hingga sistem aktif sepenuhnya.
* Menganalisis **Mean Execution Time (MET)** sebagai waktu rata-rata.
* Menghitung **Relative Performance Index (RPI)** untuk melihat efisiensi relatif antar percobaan.
* Mengamati efek penggunaan berulang terhadap performa sistem (**semakin sering AI digunakan, semakin cepat waktu eksekusi**).

### 🔢 3. Hasil Percobaan & Metrik

#### a. Total Execution Time (TET)

| Percobaan | Total Waktu Eksekusi |
| --------- | -------------------- |
|  1        | 206.18 detik         |
| 2         | 153.73 detik         |
| 3         | 156.09 detik         |
| 4         | 141.69 detik         |
| 5         | 156.44 detik         |

#### b. Mean Execution Time (MET)

$$
MET = \frac{206.18 + 153.73 + 156.09 + 141.69 + 156.44}{5} = 162.03 \text{ detik}
$$

#### c. Relative Performance Index (RPI)

$$
RPI = \left(\frac{MET - TET}{MET}\right) \times 100\%
$$

| Percobaan | RPI (%)       |
| --------- | ------------- |
| 1         | -27.26%       |
| 2         | +5.12%        |
| 3         | +3.67%        |
| 4         | +12.57%       |
| 5         | +3.45%        |

### 🔹 4. Insight dan Interpretasi

* **Percobaan ke-1** lambat karena merupakan **eksekusi pertama (cold start)**, harus mengunduh model AI, peta, dan layer data.
* Setelah Percobaan 2–5, waktu eksekusi menjadi **lebih efisien** karena sistem telah cache model dan elemen visual.
* Percobaan 4 menunjukkan hasil **terbaik**, cocok dijadikan baseline pengembangan sistem.

---

## 🚀 Pengembangan Lanjutan

* Integrasi data real-time dari sensor dan kamera lalu lintas.
* Pengiriman notifikasi peringatan kemacetan ke pengguna secara langsung.
* Pengembangan aplikasi mobile interaktif.
* Integrasi dengan sistem transportasi publik dan ridesharing.

---

## 👥 Tim Pengembang

**Ketua:**
Khaylilla Shafaraly Irnanda (G1A023079)

**Anggota:**
Aurel Moura Athanafisah  (G1A023001)
Waridhania As Syifa      (G1A023075)

---

## 📍 Daftar Lokasi yang Dapat Diakses

| No | Lokasi Populer (Patokan) |
| -- | ------------------------ |
| 1  | SD Negeri 57 Bengkulu    |
| 2  | Pantai Panjang           |
| 3  | SMPN 07 Bengkulu         |
| 4  | Pasar Panorama           |
| 5  | Pasar Minggu             |
| 6  | Universitas Bengkulu     |
| 7  | SMPIT Iqra Bengkulu      |
| 8  | Masjid Raya Baitul Izza  |

💡 *Gunakan nama lokasi persis seperti tertulis untuk hasil terbaik.*

---

## ⚙️ Alur Sistem

<img src="https://raw.githubusercontent.com/username/repo-name/main/assets/alur-sistem.png" alt="Alur Sistem Smart City" width="100%" />

---

## 🚀 Ayo mulai!

Jalankan kode, dan nikmati pengalaman navigasi yang lebih pintar untuk Kota Bengkulu.
**Menuju kota cerdas yang lebih nyaman dan efisien.**
