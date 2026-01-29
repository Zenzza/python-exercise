# Latihan Python Exercise:

Tujuan: Mengukur keterampilan untuk pembagian tugas.  
Deadline: 30 Januari 2026.  
_Bila memerlukan waktu tambahan, mohon menghubungi PIC._

# Objektif:

1. Membuat program untuk membandingkan dua dokumen Word: Dokumen A dan Dokumen B.
2. Mencari perbedaan antara kedua dokumen berdasarkan kriteria yang diberikan.
3. Menampilkan hasil perbedaan dalam GUI.

# Peraturan:

1. Clone dan buat repository baru.
2. Gunakan bahasa pemrograman Python.
3. Boleh menggunakan AI.
4. Kerjakan semampunya. Jika ada komponen yang tidak berhasil dikerjakan, tuliskan alasannya di SUMMARY.md.
5. Tuliskan ringkasan eksekutif di SUMMARY.md yang mencakup pendekatan yang dipilih, tantangan yang dihadapi, dan solusi yang diterapkan.
6. Commit hasil akhir dan bagikan tautan repository.

# Kriteria Perbandingan:

1. **Line Spacing** - Jarak antar kalimat.
   - Contoh:
     - Dokumen A: 1.5 Spacing
     - Dokumen B: 1 Spacing
     - Perbedaan: -0.5

2. **Bullet & Numbering** - Jenis bullet seperti disc, atau penomoran seperti 1), A., termasuk sub-level seperti a), i.
   - Contoh:
     - Dokumen A: Menggunakan A)
     - Dokumen B: Menggunakan 1.
     - Perbedaan: 1 Bullet & Numbering

3. **Spacing Indentasi** - Jarak indentasi dari sisi kiri dokumen.
   - Contoh:
     - Dokumen A: 1 cm dari kiri
     - Dokumen B: 1.5 cm dari kiri
     - Perbedaan: 0.5 cm

4. **Efek Pencetakan** - Deteksi perbedaan pada kata yang memiliki efek seperti **bold**, italic, atau underline.
   - Contoh:
     - Dokumen A: wisata - **bold**
     - Dokumen B: wisata - regular
     - Perbedaan: 1 Efek

5. **Kesalahan Ketik** - Deteksi kata yang memiliki kesalahan ketik.
   - Contoh:
     - Dokumen A: memilih
     - Dokumen B: memilihi
     - Perbedaan: 1 Kata

# Interface:

- Tampilkan hasil perbandingan dalam GUI. Penilaian tidak akan didasarkan pada keindahan desain.
- Desain GUI bebas, namun hasilnya harus menyerupai tampilan pada file `interface.png`.
- Ilustrasi interface dan contoh di atas hanya menampilkan satu perbedaan. Ekspektasi Anda adalah mencantumkan semua perbedaan yang ditemukan untuk setiap kriteria.
