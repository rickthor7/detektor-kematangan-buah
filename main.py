import cv2
import os
import numpy as np

# =====================================================
# DETEKSI KEMATANGAN BUAH PISANG
# MENGGUNAKAN RGB DAN HSV
# =====================================================

# =====================================================
# PATH DATASET
# =====================================================
dataset_path = "dataset"

# =====================================================
# PATH OUTPUT
# =====================================================
output_path = "output"

# =====================================================
# MEMBUAT FOLDER OUTPUT JIKA BELUM ADA
# =====================================================
if not os.path.exists(output_path):
    os.makedirs(output_path)

# =====================================================
# FUNGSI RESIZE GAMBAR
# =====================================================
def resize_image(img):
    return cv2.resize(img, (400, 300))

# =====================================================
# FUNGSI DETEKSI KEMATANGAN
# =====================================================
def detect_ripeness(img):

    # =================================================
    # KONVERSI BGR KE HSV
    # =================================================
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # =================================================
    # THRESHOLD WARNA HIJAU
    # =================================================
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # =================================================
    # THRESHOLD WARNA KUNING
    # =================================================
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # =================================================
    # SEGMENTASI WARNA
    # =================================================
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # =================================================
    # MASKING OBJEK
    # =================================================
    result_green = cv2.bitwise_and(img, img, mask=mask_green)

    result_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

    # =================================================
    # HITUNG JUMLAH PIXEL
    # =================================================
    green_pixels = cv2.countNonZero(mask_green)

    yellow_pixels = cv2.countNonZero(mask_yellow)

    # =================================================
    # CETAK HASIL PIXEL
    # =================================================
    print("Green Pixels :", green_pixels)
    print("Yellow Pixels:", yellow_pixels)

    # =================================================
    # PENENTUAN KEMATANGAN
    # =================================================
    if green_pixels > yellow_pixels + 1000:
        status = "MENTAH"

    elif yellow_pixels > green_pixels + 1000:
        status = "MATANG"

    else:
        status = "SETENGAH MATANG"

    # =================================================
    # RETURN SEMUA HASIL
    # =================================================
    return (
        status,
        hsv,
        mask_green,
        mask_yellow,
        result_green,
        result_yellow
    )

# =====================================================
# HEADER PROGRAM
# =====================================================
print("========================================")
print(" DETEKSI KEMATANGAN BUAH PISANG ")
print("========================================")

# =====================================================
# CEK APAKAH DATASET ADA
# =====================================================
if not os.path.exists(dataset_path):

    print("Folder dataset tidak ditemukan!")
    exit()

# =====================================================
# MEMBACA SELURUH FOLDER DATASET
# =====================================================
for kategori in os.listdir(dataset_path):

    folder_path = os.path.join(dataset_path, kategori)

    # =================================================
    # SKIP JIKA BUKAN FOLDER
    # =================================================
    if not os.path.isdir(folder_path):
        continue

    print("\n========================================")
    print("MEMBACA FOLDER :", kategori)
    print("========================================")

    # =================================================
    # MEMBACA FILE GAMBAR
    # =================================================
    for file in os.listdir(folder_path):

        # =================================================
        # HANYA MEMBACA FILE GAMBAR
        # =================================================
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # =================================================
        # PATH GAMBAR
        # =================================================
        img_path = os.path.join(folder_path, file)

        # =================================================
        # MEMBACA GAMBAR
        # =================================================
        img = cv2.imread(img_path)

        # =================================================
        # CEK APAKAH GAMBAR BERHASIL DIBACA
        # =================================================
        if img is None:
            print("Gagal membaca gambar:", img_path)
            continue

        # =================================================
        # RESIZE GAMBAR
        # =================================================
        img = resize_image(img)

        print("\n----------------------------------------")
        print("Nama File :", file)
        print("Path      :", img_path)
        print("----------------------------------------")

        # =================================================
        # PROSES DETEKSI
        # =================================================
        (
            status,
            hsv,
            mask_green,
            mask_yellow,
            result_green,
            result_yellow

        ) = detect_ripeness(img)

        # =================================================
        # CETAK HASIL DETEKSI
        # =================================================
        print("HASIL DETEKSI :", status)

        # =================================================
        # COPY GAMBAR UNTUK OUTPUT FINAL
        # =================================================
        result_img = img.copy()

        # =================================================
        # MENAMPILKAN LABEL HASIL
        # =================================================
        cv2.putText(
            result_img,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # =================================================
        # MENAMPILKAN WINDOW HASIL
        # =================================================
        cv2.imshow("1. Original Image", img)

        cv2.imshow("2. HSV Image", hsv)

        cv2.imshow("3. Mask Green", mask_green)

        cv2.imshow("4. Mask Yellow", mask_yellow)

        cv2.imshow("5. Result Green", result_green)

        cv2.imshow("6. Result Yellow", result_yellow)

        cv2.imshow("7. Final Detection", result_img)

        # =================================================
        # MENYIMPAN OUTPUT
        # =================================================
        save_name = kategori + "_" + file

        save_path = os.path.join(output_path, save_name)

        success = cv2.imwrite(save_path, result_img)

        # =================================================
        # CEK HASIL PENYIMPANAN
        # =================================================
        if success:
            print("Output berhasil disimpan:")
            print(save_path)
        else:
            print("Gagal menyimpan output!")

        # =================================================
        # DELAY
        # =================================================
        key = cv2.waitKey(1500)

        # =================================================
        # TEKAN ESC UNTUK KELUAR
        # =================================================
        if key == 27:
            break

# =====================================================
# MENUTUP SEMUA WINDOW
# =====================================================
cv2.destroyAllWindows()

# =====================================================
# PROGRAM SELESAI
# =====================================================
print("\n========================================")
print(" PROGRAM SELESAI ")
print("========================================")