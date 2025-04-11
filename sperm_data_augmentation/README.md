# Sperm Morfolojisi Görüntüleri için Veri Artırma (Data Augmentation) Aracı

Bu araç, sperm morfolojisi görüntülerini çeşitli teknikler kullanarak artırmak için tasarlanmıştır. Medikal görüntüler için özel olarak ayarlanmış veri artırma teknikleri kullanılmaktadır.

## Özellikler

- 53 görüntüyü 1000 görüntüye kadar artırabilme
- Medikal görüntüler için optimize edilmiş veri artırma teknikleri
- İlerleme çubuğu ile işlem durumunu takip etme
- Orijinal görüntüleri koruma seçeneği
- BMP formatını destekleme

## Kullanılan Veri Artırma Teknikleri

1. **Hafif Döndürme (Rotate Small)**: Görüntüyü -10° ile +10° arasında döndürür
2. **Orta Seviye Döndürme (Rotate Medium)**: Görüntüyü -30° ile +30° arasında döndürür
3. **Yatay Çevirme (Flip Horizontal)**: Görüntüyü yatay eksende çevirir
4. **Dikey Çevirme (Flip Vertical)**: Görüntüyü dikey eksende çevirir
5. **Parlaklık ve Kontrast Ayarı**: Görüntünün parlaklık ve kontrastını değiştirir
6. **Gaussian Gürültü Ekleme**: Görüntüye kontrollü miktarda gürültü ekler
7. **Kırpma ve Yeniden Boyutlandırma**: Görüntünün bir kısmını kırpar ve orijinal boyuta geri getirir
8. **Ölçeklendirme**: Görüntüyü büyütüp küçültür ve orijinal boyuta geri getirir

## Gereksinimler

- Python 3.6 veya üzeri
- OpenCV (`opencv-python`)
- tqdm (ilerleme çubuğu için)

## Kurulum

Gerekli kütüphaneleri yüklemek için:

```bash
pip install opencv-python tqdm
```

## Kullanım

Script'i aşağıdaki gibi çalıştırabilirsiniz:

```bash
python sperm_data_augmentation.py --input_dir /path/to/input/images --output_dir /path/to/output/images --target_count 1000 --preserve_originals
```

### Parametreler

- `--input_dir`: Giriş görüntülerinin bulunduğu klasör (zorunlu)
- `--output_dir`: Çıkış görüntülerinin kaydedileceği klasör (zorunlu)
- `--target_count`: Hedeflenen toplam görüntü sayısı (varsayılan: 1000)
- `--preserve_originals`: Orijinal görüntüleri çıkış klasörüne kopyala (isteğe bağlı)

## Örnek

53 görüntüyü 1000 görüntüye artırmak için:

```bash
python sperm_data_augmentation.py --input_dir /path/to/your/images --output_dir /path/to/augmented/images --target_count 1000 --preserve_originals
```

## Notlar

- Tüm görüntüler .bmp formatında olmalıdır
- Script, her bir orijinal görüntü için gerekli sayıda artırılmış görüntü oluşturur
- Medikal görüntüler için özel olarak ayarlanmış ağırlıklar kullanılmaktadır
- Artırılmış görüntüler, orijinal görüntü adı + artırma tekniği + sıra numarası şeklinde isimlendirilir
