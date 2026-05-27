# 🐸 Frogger CV - Gesture Controlled Arcade Game

Sebuah reka ulang (remake) dari game arcade klasik "Frogger", di mana pemain mengendalikan karakter menggunakan **pergerakan tangan secara real-time (Computer Vision)**, bukan menggunakan keyboard atau controller.

Proyek ini dibangun menggunakan Python dan mengimplementasikan *Natural User Interface* (NUI) dengan membaca landmark tangan manusia.

## 🚀 Fitur Utama
* **Real-time Hand Tracking**: Mendeteksi dan melacak pergerakan pergelangan tangan menggunakan kecerdasan buatan.
* **Dynamic Grid Movement**: Pemetaan gerakan (Maju, Mundur, Kiri, Kanan) yang sejajar dan presisi ke sistem petak (grid) game 2D.
* **Anti-Jitter Mechanism**: Algoritma toleransi (*buffer*) untuk menjaga stabilitas kontrol saat tangan sesaat keluar dari *frame* kamera.
* **Sprite Sheet Subsurface**: Ekstraksi grafis otomatis menggunakan pemotongan matriks (pengganti pemotongan gambar manual).

## 🛠️ Teknologi yang Digunakan
* **Python 3.x**
* **OpenCV**: Untuk penangkapan *frame* dari webcam dan manipulasi gambar matriks.
* **MediaPipe**: Model *Machine Learning* ringan dari Google untuk pelacakan titik *landmark* tangan.
* **Pygame**: *Engine* utama untuk render grafis 2D, deteksi kolisi (tabrakan), dan logika *game loop*.

## 📥 Cara Instalasi dan Bermain (Untuk Developer)
1. *Clone* repositori ini:
   ```bash
   git clone [https://github.com/Travis-Tandyawan/frogger-cv-game.git](https://github.com/Travis-Tandyawan/frogger-cv-game.git)
2. Buat Virtual Environment (opsional tapi direkomendasikan) dan instal dependensi:
   Bash
pip install opencv-python mediapipe==0.10.14 pygame
3. Bash
python main.py

🎮 Kontrol (Gerakan Tangan)
1. Angkat tangan ke depan kamera hingga lingkaran merah (patokan) muncul.
2. Geser tangan Ke Atas melewati patokan -> Melompat Maju.
3. Geser tangan Ke Bawah melewati patokan -> Mundur.
4. Geser tangan Ke Kiri / Kanan melewati patokan -> Geser Kiri / Kanan.
5. Kembali ke tengah untuk melakukan lompatan berikutnya.

