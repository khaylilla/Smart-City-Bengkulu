![Bengkulu](https://github.com/user-attachments/assets/9f4ff114-2258-45ac-b06c-c45c6ee69a63)


# 🚦 Smart City: Sistem Prediksi & Navigasi Kemacetan Bengkulu

Proyek ini merupakan bagian dari pengembangan sistem Smart City untuk Kota Bengkulu. Sistem ini bertujuan memberikan **peringatan dini terhadap kemacetan lalu lintas** dan merekomendasikan **rute alternatif** secara visual melalui peta interaktif.

## 📌 Studi Kasus

> Kota Bengkulu ingin mengembangkan sistem navigasi cerdas berbasis AI yang dapat memprediksi dan memperingatkan kemacetan secara visual, serta memberikan rekomendasi rute alternatif kepada masyarakat secara interaktif dan informatif.

---

## 📍 Daftar Lokasi yang Dapat Diakses

| No | Lokasi (Patokan)        | Lokasi (Patokan)                    |
| -- | ----------------------- | ----------------------------------- |
| 1  | Pasar Panorama          | Musium Provinsi Bengkulu            |
| 2  | Pasar Minggu            | Mercure                             |
| 3  | SMPN 07 Bengkulu        | Rumah Sakit Tiara Sella             |
| 4  | Xtra Hotel              | Taman Budaya                        |
| 5  | Toko Roti Surya         | Universitas Dehasen                 |
| 6  | Universitas Bengkulu    | SMA Negeri 5                        |
| 7  | SMPIT Iqra              | Gedung Pemuda dan Olah Raga         |
| 8  | Masjid Raya Baitul Izza | Bencoolen Mall                      |
| 9  | Masjid Al-Hidayah       | Kantor Pos Padang Jati              |
| 10 | Pantai Panjang Bengkulu | Radio Republik Indonesia, Bengkulu  |


💡 *Gunakan nama lokasi persis seperti tertulis untuk hasil terbaik.*

---

## 🧠 Model AI yang Digunakan: 

🔍 **Prediksi Kemacetan**
    Menggunakan **Decision Tree Classifier** dari pustaka scikit-learn untuk memprediksi apakah suatu ruas jalan rawan mengalami kemacetan atau tidak.

📌 Alasan Memilih Model Decision Tree:

   1. **Mudah Dipahami**:
      Decision Tree gampang dimengerti dan dijelaskan, cocok untuk percobaan awal dalam 
      sistem prediksi lalu lintas.

   2. **Cepat dan Ringan**:
      Proses pelatihannya cepat, cocok untuk data jalan di satu kota yang tidak terlalu 
      besar.

   3. **Tanpa Perlu Normalisasi**:
      Bisa langsung digunakan dengan angka seperti panjang jalan, tanpa harus diubah dulu.

   4. **Hasil Jelas (Macet atau Tidak)**:
       Model ini bisa memberi hasil sederhana: jalan macet (1) atau tidak macet (0), 
       misalnya jika panjang jalan lebih dari 200 meter.

   5. **Cocok untuk Peta Jalan**:
       Decision Tree bisa diterapkan langsung ke jaringan jalan yang dibuat dengan OSMnx  
       dan NetworkX.

🛍️ **Navigasi Rute**
Menggunakan algoritma:

* **Dijkstra**
  Efisien untuk mencari jalur terpendek dari titik awal ke tujuan.

  → Dimodifikasi dengan penalti kemacetan untuk memprioritaskan jalan yang lebih lancar.

---

## 📊 Jenis dan Sumber Data

### 1. Data Jaringan Jalan

* **Sumber**: OpenStreetMap (diakses melalui pustaka [OSMnx](https://github.com/gboeing/osmnx))
* **Jenis**: Data graf jaringan jalan (berisi simpul dan ruas jalan)
* **Fitur yang digunakan**: Panjang ruas jalan (`length`) dari setiap edge

### 2. Label Kemacetan (Simulasi)

* **Jenis**: Klasifikasi biner (1 = macet, 0 = tidak macet)
* **Sumber**: Ditentukan secara sederhana dari panjang jalan, contoh:

  ```python
  is_congested = 1 if length > 200 else 0
  ```

---

## 🔍 Metode Pengumpulan Data

* Menggunakan `osmnx.graph_from_place("Bengkulu, Indonesia", network_type='drive')` untuk mengambil graf jalan kota Bengkulu.
* Mengekstrak fitur panjang (`length`) dari setiap ruas jalan.
* Menentukan label kemacetan (`is_congested`) berdasarkan logika sederhana.

---

## 🧹 Praproses Data

* Menyaring edge yang memiliki atribut `length`.
* Menyusun dataset fitur (`X`) dan label (`y`).
* Membagi dataset menjadi data latih dan data uji menggunakan `train_test_split()` dari Scikit-learn.
* Melatih model Decision Tree untuk memprediksi status kemacetan berdasarkan panjang jalan.

---

### 📋 Contoh Dataset

| Panjang Jalan (meter) | Label Kemacetan |
| --------------------- | --------------- |
| 120.4                 | 0 (tidak macet) |
| 354.7                 | 1 (macet)       |
| 89.2                  | 0 (tidak macet) |

---

## 🔄 Desain Alur Kerja Sistem

Sistem prediksi kemacetan lalu lintas ini terdiri dari beberapa tahapan utama:

1. **Pengambilan Data Jalan**

     Sistem mengambil data jaringan jalan kota Bengkulu menggunakan pustaka **OSMnx**, yang 
   memetakan graf jaringan jalan (nodes dan edges).

3. **Ekstraksi dan Praproses Data**

     Dari graf tersebut, sistem mengekstrak atribut penting seperti panjang setiap ruas 
   jalan. Ruas jalan tanpa data panjang akan diabaikan. Kemudian dibuat dataset fitur (`X`) 
   dan label (`y`), di mana label kemacetan ditentukan berdasarkan threshold sederhana.

5. **Pelatihan Model (Training)**

     Model **Decision Tree Classifier** digunakan karena sifatnya yang sederhana dan cepat.
   Dataset dibagi menjadi data latih dan data uji, lalu model dilatih untuk memprediksi 
   apakah sebuah ruas jalan macet atau tidak berdasarkan panjangnya.

7. **Evaluasi dan Visualisasi**

     Model dievaluasi menggunakan metrik akurasi, lalu hasil prediksi divisualisasikan di 
   peta menggunakan `OSMnx`, dengan warna berbeda untuk jalan yang macet dan tidak.

---

## 📊 Strategi Evaluasi Model dan Performa Sistem

Untuk menilai performa sistem prediksi kemacetan lalu lintas berbasis AI, dilakukan **10 kali pengujian** dalam berbagai kondisi. Fokus evaluasi adalah efisiensi sistem secara keseluruhan dalam memproses data graf jalan, memuat model prediksi, serta merender visualisasi peta interaktif.

## Dokumentasi Gambar Percobaan

| ![Percobaan ke-1](https://github.com/user-attachments/assets/b86d1bf5-af5c-426e-9afe-0070515df1d2) |![Percobaan ke-2](https://github.com/user-attachments/assets/6b66b9e6-a584-4506-9c0c-9561369f71c8) | ![Percobaan ke-3](https://github.com/user-attachments/assets/d0aa0780-fdc2-43c8-a5c5-d56c03dd076b) | ![Percobaan ke-4](https://github.com/user-attachments/assets/addeb447-92fa-4692-ac3d-610a4d3844b6)|
|---|---|---|---|

| ![Percobaan ke-5](https://github.com/user-attachments/assets/2fff183f-5400-4452-8620-a10d53ff91cc) | ![Percobaan ke-6](https://github.com/user-attachments/assets/fec9a7bf-4ec3-422b-8eba-d38575684fc9) | ![Percobaan ke-7](https://github.com/user-attachments/assets/9cb309b0-88cc-4ae5-9935-32c275b2a424) | ![Percobaan ke-8](https://github.com/user-attachments/assets/a64effda-e723-4470-9fe2-d1f5e6163fbb) |
|---|---|---|---|

| ![Percobaan ke-9](https://github.com/user-attachments/assets/59e7bb81-0fa2-4443-8fa1-e2326f0817a9) | ![Percobaan ke-10](https://github.com/user-attachments/assets/1b695143-008c-42a9-84c6-b58bd3df22da) |
|---|---|

---

### 🎯 1. Strategi Evaluasi

Evaluasi dilakukan dengan pendekatan sebagai berikut:

* **Total Execution Time (TET)**
  Mengukur total waktu dari awal proses pemuatan peta dan data graf hingga sistem siap digunakan.

* **Mean Execution Time (MET)**
  Rata-rata waktu eksekusi dari seluruh percobaan untuk mengukur konsistensi performa sistem.

* **Relative Performance Index (RPI)**
  Metrik efisiensi relatif dari tiap percobaan dibandingkan waktu rata-rata:

  $$
  RPI = \left(\frac{MET - TET}{MET}\right) \times 100
  $$

* **Pengaruh Reuse Data (Cache Effect)**
  Mengamati apakah penggunaan berulang membuat sistem menjadi lebih cepat (karena model, layer, atau data sudah tersimpan di memori/cache).

---

### ⏱️ 2. Hasil Evaluasi

#### a. Waktu Eksekusi per Percobaan

| Percobaan | Waktu Eksekusi (detik) |
| --------- | ---------------------- |
| 1         | 217.22                 |
| 2         | 195.05                 |
| 3         | 181.78                 |
| 4         | 173.01                 |
| 5         | 205.81                 |
| 6         | 217.95                 |
| 7         | 208.48                 |
| 8         | 207.77                 |
| 9         | 197.58                 |
| 10        | 194.60                 |

Waktu Tercepat: 173.01 detik

Waktu Terlama: 217.95 detik

#### b. Mean Execution Time (MET)

$$
MET = \frac{217.22 + 195.05 + 181.78 + 173.01 + 205.81 + 217.95 + 208.48 + 207.77 + 197.58 + 194.60}{10} = \mathbf{199.525 \ detik}
$$

#### c. Relative Performance Index (RPI)

| Percobaan | RPI (%) |
| --------- | ------- |
| 1         | -8.85%  |
| 2         | +2.25%  |
| 3         | +8.88%  |
| 4         | +13.28% |
| 5         | -3.15%  |
| 6         | -9.22%  |
| 7         | -4.48%  |
| 8         | -4.12%  |
| 9         | +1.00%  |
| 10        | +2.47%  |

---

### 💡 3. Insight dan Interpretasi

| Aspek Evaluasi              | Penjelasan                                                                                                                                                                                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🧊 Cold Start Effect        | - Terjadi pada Percobaan ke-1 dan ke-6. <br> - Sistem membutuhkan waktu lebih lama karena harus memuat model, data graf, dan peta dari awal.                                                                                                          |
| ⚡ Performa Terbaik          | - Percobaan ke-4 memiliki waktu tercepat (173.01 detik). <br> - Menunjukkan sistem dalam kondisi optimal dengan cache aktif.                                                                                                                          |
| 📉 Fluktuasi Performa       | - Terjadi antar percobaan karena faktor eksternal: <br>   • Beban sistem lokal (CPU/RAM) <br>   • Latensi jaringan (akses peta online) <br>   • Kompleksitas graf (jumlah node/edge bervariasi)                                                       |
| ⏱️ Efisiensi Sistem         | - Rata-rata waktu eksekusi (**MET = 199.72 detik**) masih tergolong efisien untuk skala prototipe. <br> - Cocok untuk sistem prediksi non-realtime seperti batch hourly.                                                                              |
| 👥 Dampak ke Pengguna Akhir | - Waktu < 200 detik masih nyaman untuk pengguna seperti petugas dinas atau dashboard pemantauan. <br> - Untuk real-time (< 60 detik), dibutuhkan optimisasi lanjutan: <br>   • Model ringan <br>   • Cache dinamis <br>   • Server-side preprocessing |

---

## 🚀 Pengembangan Lanjutan

| No. | Fitur Pengembangan                          | Deskripsi                                                                                                 | Manfaat Bagi Masyarakat                                         |
| --- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 1   | **Integrasi Data Lalu Lintas Waktu Nyata**  | Menghubungkan sistem dengan API lalu lintas (misal Google Maps, Waze, atau Dishub).                       | Informasi kemacetan lebih akurat dan terkini.                   |
| 2   | **Pembuatan Aplikasi Mobile (Android/iOS)** | Pengembangan versi mobile menggunakan React Native lengkap dengan navigasi suara.                         | Dapat digunakan saat berkendara atau di lapangan.               |
| 3   | **Prediksi Kemacetan Berdasarkan Waktu**    | Menggunakan data historis untuk memprediksi kemacetan berdasarkan jam sibuk, hari libur, dan event lokal. | Rekomendasi rute lebih tepat waktu dan kontekstual.             |
| 4   | **Navigasi Multimodal**                     | Memberikan opsi kombinasi transportasi: jalan kaki, motor, mobil, angkot.                                 | Lebih fleksibel dan sesuai kebutuhan pengguna.                  |
| 5   | **Analisis Infrastruktur Jalan**            | Menyimpan dan menganalisis histori kemacetan, menampilkan area rawan secara visual.                       | Membantu perencanaan kota dan pengambilan keputusan pemerintah. |
| 6   | **Pelaporan Kemacetan oleh Pengguna**       | Menyediakan fitur laporan crowdsourcing langsung dari pengguna mengenai kondisi jalan.                    | Data kemacetan menjadi lebih cepat dan bersumber dari lapangan. |
| 7   | **Rute Berbasis Tujuan Khusus**             | Menyediakan rute tercepat ke tempat penting seperti RS, SPBU, sekolah, dan wisata.                        | Akses cepat dan aman untuk keperluan darurat atau publik.       |

---

## 👥 Tim Pengembang

**Ketua:**
Khaylilla Shafaraly Irnanda (G1A023079)

**Anggota:**
* Aurel Moura Athanafisah  (G1A023001)
* Waridhania As Syifa      (G1A023075)

---

## 🚀 Ayo mulai!

Jalankan kode, dan nikmati pengalaman navigasi yang lebih pintar untuk Kota Bengkulu.
**Menuju kota cerdas yang lebih nyaman dan efisien.**
