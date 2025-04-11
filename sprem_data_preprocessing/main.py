import os
import cv2
import numpy as np
from tqdm import tqdm


def convert_nested_dataset_to_rgb(input_dir, output_dir, target_size=(224, 224)):
    """
    İç içe klasör yapısına sahip veri setindeki tüm görüntüleri (gri veya renkli) tespit edip,
    hepsini RGB formata dönüştürür ve belirtilen boyuta getirir.

    Parametreler:
    input_dir (str): Kaynak görüntülerin bulunduğu ana dizin
    output_dir (str): İşlenmiş görüntülerin kaydedileceği ana dizin
    target_size (tuple): Hedef görüntü boyutu (genişlik, yükseklik)
    """
    # Çıktı dizinini oluştur (yoksa)
    os.makedirs(output_dir, exist_ok=True)

    # Ana sınıf dizinlerini bul (01_Normal, 02_Tapered, vb.)
    class_dirs = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    for class_dir in class_dirs:
        class_path = os.path.join(input_dir, class_dir)

        # Her sınıf için çıktı dizini oluştur
        class_output_dir = os.path.join(output_dir, class_dir)
        os.makedirs(class_output_dir, exist_ok=True)

        # Alt dizinleri bul (train, test, valid)
        split_dirs = [d for d in os.listdir(class_path) if os.path.isdir(os.path.join(class_path, d))]

        for split_dir in split_dirs:
            split_path = os.path.join(class_path, split_dir)

            # Her bölme için çıktı dizini oluştur
            split_output_dir = os.path.join(class_output_dir, split_dir)
            os.makedirs(split_output_dir, exist_ok=True)

            # Bölme dizinindeki tüm .bmp dosyalarını bul (büyük/küçük harf duyarsız)
            image_files = [f for f in os.listdir(split_path) if f.lower().endswith('.bmp')]

            print(f"İşleniyor: {class_dir}/{split_dir} - {len(image_files)} görüntü")

            # Her görüntüyü işle
            for img_file in tqdm(image_files, desc=f"{class_dir}/{split_dir}"):
                # Görüntüyü oku
                img_path = os.path.join(split_path, img_file)
                img = cv2.imread(img_path)

                if img is None:
                    print(f"Uyarı: {img_path} okunamadı, atlanıyor.")
                    continue

                # Görüntünün gri tonlamalı olup olmadığını kontrol et
                if len(img.shape) == 2:
                    # Gri tonlamalı görüntüyü RGB'ye dönüştür
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                elif len(img.shape) == 3 and img.shape[2] == 1:
                    # Tek kanallı görüntüyü RGB'ye dönüştür
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                elif len(img.shape) == 3 and img.shape[2] == 3:
                    # Zaten renkli, bir şey yapma
                    pass
                else:
                    print(f"Uyarı: {img_path} beklenmeyen formatta, atlanıyor.")
                    continue

                # Görüntüyü yeniden boyutlandır (224x224)
                img_resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

                # Normalizasyon [0,1]
                img_normalized = img_resized.astype(np.float32) / 255.0

                # Normalize edilmiş görüntüyü kaydet
                # Not: Normalizasyon sonrası görüntüyü kaydederken tekrar [0,255] aralığına dönüştürüyoruz
                save_img = (img_normalized * 255).astype(np.uint8)

                output_path = os.path.join(split_output_dir, img_file)
                cv2.imwrite(output_path, save_img)

    print("Tüm görüntüler işlendi ve kaydedildi.")


# Kullanım örneği
if __name__ == "__main__":
    # Veri setinizin ana dizini
    dataset_dir = r"C:..."

    # İşlenmiş görüntülerin kaydedileceği dizin
    processed_dir = r"C:..."

    # Tüm görüntüleri 224x224 boyutuna getir ve RGB formata dönüştür
    convert_nested_dataset_to_rgb(dataset_dir, processed_dir, target_size=(224, 224))
