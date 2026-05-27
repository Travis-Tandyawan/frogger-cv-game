import cv2
import mediapipe as mp
import pygame
import sys
import os

# ============================================================
# FUNGSI KHUSUS UNTUK BACA ASET DI DALAM FILE .EXE
# ============================================================
def resource_path(relative_path):
    """ Dapatkan path absolut ke resource, berfungsi untuk dev dan untuk PyInstaller """
    try:
        # PyInstaller membuat folder temporary dan menyimpannya di _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ============================================================
# 1. PERSIAPAN GAME (PYGAME)
# ============================================================
pygame.init()
lebar_layar, tinggi_layar = 800, 600
layar = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption("Frogger CV - Final Version")
clock = pygame.time.Clock()

# Koordinat Awal (Kelipatan 40)
posisi_awal_x = 400
posisi_awal_y = 540
kodok_x = posisi_awal_x
kodok_y = posisi_awal_y
ukuran_kodok = 40
jarak_lompat = 40

# --- MEMUAT ASET KATAK (SPRITE SHEET) ---
lokasi_sheet_kodok = resource_path(os.path.join("assets", "frogs_sheet.png"))
sheet_kodok = pygame.image.load(lokasi_sheet_kodok).convert_alpha()
lebar_kodok_potong = sheet_kodok.get_width() // 6
gambar_kodok = pygame.transform.scale(
    sheet_kodok.subsurface(pygame.Rect(0, 0, lebar_kodok_potong, sheet_kodok.get_height())), 
    (ukuran_kodok, ukuran_kodok)
)

# --- MEMUAT ASET MOBIL (SPRITE SHEET) ---
lokasi_sheet_mobil = resource_path(os.path.join("assets", "cars_sheet.png"))
sheet_mobil = pygame.image.load(lokasi_sheet_mobil).convert_alpha()
lebar_mobil_potong = sheet_mobil.get_width() // 2
h_mobil_potong = sheet_mobil.get_height() // 2
lebar_mobil = 80
tinggi_mobil = 40
gambar_mobil = pygame.transform.scale(
    sheet_mobil.subsurface(pygame.Rect(0, 0, lebar_mobil_potong, h_mobil_potong)), 
    (lebar_mobil, tinggi_mobil)
)

# --- JALUR RINTANGAN ---
daftar_mobil = [
    {"x": 0, "y": 500, "speed": 4},     
    {"x": 400, "y": 460, "speed": -5},  
    {"x": 200, "y": 420, "speed": 5},   
    {"x": 600, "y": 380, "speed": -4}   
]

daftar_kayu = [
    {"x": 100, "y": 300, "speed": 3, "w": 160},  
    {"x": 500, "y": 260, "speed": -4, "w": 160}, 
    {"x": 200, "y": 220, "speed": 3, "w": 200},  
    {"x": 600, "y": 180, "speed": -3, "w": 160}  
]

# ============================================================
# 2. PERSIAPAN KAMERA & COMPUTER VISION
# ============================================================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

anchor_x, anchor_y = None, None
is_neutral = True
waktu_hilang = 0
batas_hilang = 15

print("Game siap! Silakan angkat tangan Anda ke kamera.")

# ============================================================
# 3. LOOPING UTAMA GAME
# ============================================================
while True:
    # --- A. MEMBACA KAMERA & DETEKSI TANGAN ---
    success, frame = cap.read()
    if not success: break
        
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    command = "DIAM"
    
    if results.multi_hand_landmarks:
        waktu_hilang = 0 
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            pergelangan = hand_landmarks.landmark[0]
            h, w, _ = frame.shape
            cx, cy = int(pergelangan.x * w), int(pergelangan.y * h)
            
            # Set kalibrasi titik awal
            if anchor_x is None or anchor_y is None:
                anchor_x, anchor_y = cx, cy
                
            # Gambar titik jangkar (merah) dan posisi saat ini (hijau)
            cv2.circle(frame, (anchor_x, anchor_y), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), 8, (0, 255, 0), cv2.FILLED)
            
            jarak_x = cx - anchor_x
            jarak_y = cy - anchor_y
            
            # Logika translasi gerakan
            if is_neutral:
                if jarak_y < -40:
                    command = "MAJU"
                    kodok_y -= jarak_lompat
                    is_neutral = False
                elif jarak_y > 40:
                    command = "MUNDUR"
                    kodok_y += jarak_lompat
                    is_neutral = False
                elif jarak_x > 40:
                    command = "KANAN"
                    kodok_x += jarak_lompat
                    is_neutral = False
                elif jarak_x < -40:
                    command = "KIRI"
                    kodok_x -= jarak_lompat
                    is_neutral = False
            else:
                if abs(jarak_x) < 20 and abs(jarak_y) < 20:
                    is_neutral = True
    else:
        # Buffer jika tangan hilang sejenak
        waktu_hilang += 1
        if waktu_hilang > batas_hilang:
            anchor_x, anchor_y = None, None
            is_neutral = True

    # --- B. TOMBOL KELUAR WINDOW GAME ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    # --- C. UPDATE POSISI OBJEK ---
    kodok_x = max(0, min(lebar_layar - ukuran_kodok, kodok_x))
    kodok_y = max(0, min(tinggi_layar - ukuran_kodok, kodok_y))

    for mobil in daftar_mobil:
        mobil["x"] += mobil["speed"]
        if mobil["speed"] > 0 and mobil["x"] > lebar_layar: mobil["x"] = -lebar_mobil
        elif mobil["speed"] < 0 and mobil["x"] < -lebar_mobil: mobil["x"] = lebar_layar

    for kayu in daftar_kayu:
        kayu["x"] += kayu["speed"]
        if kayu["speed"] > 0 and kayu["x"] > lebar_layar: kayu["x"] = -kayu["w"]
        elif kayu["speed"] < 0 and kayu["x"] < -kayu["w"]: kayu["x"] = lebar_layar

    # --- D. DETEKSI TABRAKAN (COLLISION) ---
    kotak_kodok = pygame.Rect(kodok_x, kodok_y, ukuran_kodok, ukuran_kodok)

    # 1. Ketabrak Mobil
    for mobil in daftar_mobil:
        kotak_mobil = pygame.Rect(mobil["x"], mobil["y"], lebar_mobil, tinggi_mobil)
        if kotak_kodok.colliderect(kotak_mobil):
            kodok_x, kodok_y = posisi_awal_x, posisi_awal_y

    # 2. Jatuh ke Sungai
    if 180 <= kodok_y <= 300:
        nempel_kayu = False
        for kayu in daftar_kayu:
            kotak_kayu = pygame.Rect(kayu["x"], kayu["y"], kayu["w"], 40)
            if kotak_kodok.colliderect(kotak_kayu):
                nempel_kayu = True
                kodok_x += kayu["speed"] 
                break
        if not nempel_kayu:
            kodok_x, kodok_y = posisi_awal_x, posisi_awal_y
            
    # 3. Masuk Garis Finish
    if kodok_y <= 140:
        print("SELAMAT! ANDA MENANG!")
        kodok_x, kodok_y = posisi_awal_x, posisi_awal_y

    # --- E. MENGGAMBAR (RENDER) LAYAR GAME ---
    layar.fill((50, 50, 50)) 
    pygame.draw.rect(layar, (200, 200, 0), (0, 0, lebar_layar, 140))       # Finish
    pygame.draw.rect(layar, (0, 100, 255), (0, 180, lebar_layar, 160))     # Sungai
    pygame.draw.rect(layar, (100, 100, 100), (0, 340, lebar_layar, 40))    # Trotoar Tengah
    pygame.draw.rect(layar, (100, 100, 100), (0, 540, lebar_layar, 60))    # Trotoar Bawah
    
    for kayu in daftar_kayu:
        pygame.draw.rect(layar, (139, 69, 19), (kayu["x"], kayu["y"], kayu["w"], 40))

    for mobil in daftar_mobil:
        if mobil["speed"] < 0:
            mobil_flip = pygame.transform.flip(gambar_mobil, True, False)
            layar.blit(mobil_flip, (mobil["x"], mobil["y"]))
        else:
            layar.blit(gambar_mobil, (mobil["x"], mobil["y"]))
            
    layar.blit(gambar_kodok, (kodok_x, kodok_y))
    
    pygame.display.update()
    clock.tick(30)

    # --- F. MENAMPILKAN WINDOW KAMERA ---
    cv2.putText(frame, f"PERINTAH: {command}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Kamera Deteksi CV", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resources saat keluar
cap.release()
cv2.destroyAllWindows()
pygame.quit()