# Summary

## Notes

Keterangan File :

1. `main.py` adalah file utama atau entry point dari program ini.
2. `gui.py` adalah file GUI untuk mengeluarkan output dari `comparator.py` GUI yang digunakan adalah CustomTkinter.
3. `comparator.py` adalah file logic atau engine dari program ini.
4. `requirements.txt` adalah file daftar dependensi yang dibutuhkan agar program berjalan dengan baik.

## Tech Stack

Tech stack yang digunakan dalam program ini meliputi:

1. **Python 3**: Bahasa pemrograman utama. Versi yang dipakai adalah Python 3.12.0
2. **CustomTkinter**: Modern GUI library berbasis python yang digunakan untuk memberikan tampilan Windows 11 style. Pemilihan CustomTkinter ini agar GUI mirip dengan GUI Windows 11 dan terlihat modern.
3. **python-docx**: Library pihak ketiga untuk membaca, memparsing, dan mengekstrak data (teks, formatting, properti) dari file Microsoft Word (.docx). Alasan pemilihannya karena python-docx dapat membaca properti atau metadata sedangkan pilihan lain seperti textract dan pypandoc tidak dapat membaca itu.
4. **difflib**: Library standar Python yang digunakan untuk logika perbandingan teks sequence-to-sequence (Fokus pada kesalahan tulisan atau adanya perubahan data). Alasan pemilihan karena membutuhkan fuzzy logic untuk fitur deteksi typo, selain itu library ini sudah ada langsung di python dan juga ringan.
5. **re**: Library standar Regex (Regular Expression) untuk pencocokan pola teks jika diperlukan (misalnya deteksi format bullet manual) dan merapikan kata-kata yang tidak cocok untuk data input.
6. **os**: Library standar untuk interaksi sistem operasi. Alasannya karena agar dapat mengakses file di dalam komputer dan juga untuk path handling agar bias di gunakan di OS Linux dan Mac.

## Challenges

1. **Bagian Bullet dan Numbering** : Format di word pada bagian bullet dan numbering lumayan susah untuk didetect secara langsung pakai program karena Bullet dan Numbering itu ghost text kalau pakai automatic numbering. Walaupun cuma ada tag numPr di text tsb tapi itu hanya nunjukin urutan ke berapa bukan tipe apa yang digunakan
2. **Kesalahan Ketik**: Membedakan typo dan kata yang benar namun mirip seperti Ramah dan Rumah. Program mengeluarkan output typo tapi sebenarny cuma beda arti. Namun jika dokumen A adalah dokumen yang benar dan Dokumen B adalah input peserta maka hal ini tidak menjadi masalah. Kembali ke sistem yang diinginkan
3. **Line Spacing**: Jika peserta tidak mengatur spacing secara manual (ttp pakai bawaan sistem) program mengeluarkan output None. Hal ini membuat program error. contohnya kalau dokumen A itu outputnya 1.15 sedangkan dokumen B outputnya None (dalam hal ini mengeluarkan output "") akan error di difflib. Karena difflib ketat dengan tipe datanya (satu int satu lagi string).

## Solusi

1. Menggunakan pendekatan heuristik dengan memeriksa nama style (misal "List Paragraph") dan keberadaan tag numbering (numPr) tapi ini bukan solusi yang bisa untuk segala jenis list. Tapi kalau untuk ini cukup baik
2. Menggunakan difflib.SequenceMatcher untuk mendeteksi kata-kata yang beda dan menghitung jumlah perbedaanya.
3. Tinggal mengasumsikan None sebagai single spacing (1.0).

## Blockers

1. **python-docx :** Hanya bisa mengambil format .docx . Tidak bisa mengambil format jadul seperti .doc, .dotx, .txt, dsb.
2. **Bullet dan Numbering** : Sesuai dengan solusi no 1. Masih terdapat bias data yang diberikan oleh program namun untuk program ini hanya bisa untuk mendeteksi jenisnya bukan ke tipenya seperti 1. atau a). Masih belum menemukan solusi yang tepat.
3. **Spacing Indentasi** : Program ini belum dapat mengecek spacing yang menjorok ke dalam dan keluar hanya bisa mengscan secara general dari margin dan kalimat awal. Sudah beberapa cara di lakukan namun belum ketemu solusi yang tepat.
