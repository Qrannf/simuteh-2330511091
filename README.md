# **SIMUTEH – Analisis Citra Daun Teh**

## **Deskripsi**

SIMUTEH merupakan proyek Computer Vision untuk melakukan analisis citra daun teh berdasarkan kondisi kesehatan dan keberadaan bercak.

## **Cara Menjalankan**

1. Buka notebook SIMUTEH menggunakan Google Colab.  
2. Hubungkan Google Drive.  
3. Pastikan dataset dan folder `src` tersedia.  
4. Jalankan seluruh sel notebook dari awal menggunakan **Runtime → Run all**.  
5. Hasil pengujian tersimpan pada folder `hasil`.

## **SEED**

SEED yang digunakan untuk pembangkitan dataset sintetis: **1091**.

## **Parameter Final Praproses**

* Resize: lebar 640 piksel.  
* Gamma: 1.0.  
* CLAHE: clip limit 2.0, tile 8×8.  
* Filter: median 3×3.  
* Penajaman: dinonaktifkan (`tajam_k = 0.0`).

## **Ringkasan Hasil P5**

Pengujian menunjukkan KB meningkat pada empat kondisi pencahayaan:

* Bayangan: 5.84 menjadi 10.18.  
* Gelap: 8.94 menjadi 15.32.  
* Kontras rendah: 3.38 menjadi 4.60.  
* Normal: 8.95 menjadi 11.56.

Pada kondisi terang, KB menurun dari 6.53 menjadi 5.79.

Pengujian 20 citra daun sehat menunjukkan simpangan baku kanal R meningkat 16.37% pada kondisi terang, sedangkan pada empat kondisi lainnya mengalami penurunan. Oleh karena itu, kondisi terang perlu mendapat perhatian pada pengujian berikutnya.


## Praktikum P5 – Deteksi Tepi

Praktikum P5 membahas penerapan deteksi tepi pada citra daun teh menggunakan beberapa metode, yaitu Sobel, Prewitt, LoG, dan Canny. Pengujian dilakukan dengan membandingkan hasil deteksi tepi terhadap mask acuan serta mengevaluasi pengaruh kondisi pencahayaan dan praproses.

Tahapan yang dilakukan:
- Perhitungan gradien Sobel dan Prewitt.
- Penerapan operator LoG dan Canny.
- Non-Maximum Suppression dan hysteresis thresholding.
- Pengujian variasi parameter deteksi tepi.
- Evaluasi menggunakan precision, recall, dan F1-score.

## Praktikum P6 – Morfologi dan Analisis Bercak

Praktikum P6 membahas segmentasi bercak daun teh menggunakan operasi morfologi, analisis komponen terhubung, pengukuran karakteristik bercak, dan klasifikasi mutu daun.

Tahapan yang dilakukan:
- Segmentasi awal daun dan bercak.
- Penerapan erosi, dilasi, opening, dan closing.
- Pengujian bentuk dan ukuran structuring element.
- Pengukuran luas, keliling, kebulatan, dan rasio aspek bercak.
- Penyaringan komponen berdasarkan karakteristik bercak.
- Evaluasi hasil klasifikasi pada 60 citra sintetis.

### Modul Analisis Bercak

Modul `src/bercak.py` menyediakan fungsi `analisis_daun()` untuk menganalisis citra daun yang telah melalui proses praproses.

Contoh penggunaan:

```python
from praproses import praproses
from bercak import analisis_daun

# Memproses citra terlebih dahulu
img_pra = praproses(img, PARAM)

# Menganalisis bercak
hasil = analisis_daun(img_pra)

print("Jumlah bercak:", hasil["jumlah_bercak"])
print("Persen bercak:", hasil["persen_bercak"], "%")
print("Kelas mutu:", hasil["kelas"])
```

Hasil analisis meliputi:
- Mask daun.
- Mask bercak.
- Jumlah komponen bercak.
- Persentase luas bercak.
- Kelas mutu daun: Sehat, Bercak Ringan, atau Bercak Berat.
- Informasi ukuran setiap komponen bercak.

### Hasil Evaluasi P6

Pengujian modul dilakukan terhadap 60 citra sintetis dengan hasil:
- Galat absolut rerata persentase bercak: 0,622.
- Korelasi persentase prediksi dan acuan: 0,909.
- Akurasi klasifikasi: 85%.
- Kondisi pencahayaan dengan akurasi tertinggi: terang (100%).
- Kondisi pencahayaan dengan akurasi terendah: kontras rendah (67%).

Hasil evaluasi masih memiliki keterbatasan karena parameter batas kelas ditentukan dengan melihat label seluruh dataset. Pengujian lanjutan menggunakan pembagian data latih, validasi, dan uji diperlukan untuk memperoleh evaluasi yang lebih objektif.
