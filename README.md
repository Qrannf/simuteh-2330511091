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

&nbsp;