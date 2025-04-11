# Sperm Morfolojisi Görüntüleri için Veri Artırma (Data Augmentation)

Bu belge, sperm morfolojisi görüntülerini çeşitli teknikler kullanarak artırmak için geliştirilen Python aracının kapsamlı bir açıklamasını içermektedir. Bu araç, medikal görüntüler için özel olarak tasarlanmış veri artırma teknikleri kullanarak, sınırlı sayıdaki görüntü setini genişletmenize yardımcı olur.

## İçindekiler

1. [Genel Bakış](#genel-bakış)
2. [Özellikler](#özellikler)
3. [Gereksinimler](#gereksinimler)
4. [Kurulum](#kurulum)
5. [Kullanım](#kullanım)
6. [Veri Artırma Teknikleri](#veri-artırma-teknikleri)
7. [Parametreler](#parametreler)
8. [Bilinen Sorunlar ve Çözümleri](#bilinen-sorunlar-ve-çözümleri)
9. [Örnekler](#örnekler)
10. [Sık Sorulan Sorular](#sık-sorulan-sorular)

## Genel Bakış

Bu araç, derin öğrenme ve makine öğrenmesi modellerinin eğitimi için kullanılacak sperm morfolojisi görüntülerinin sayısını artırmak amacıyla geliştirilmiştir. Medikal görüntülerin hassas doğası göz önünde bulundurularak, morfolojik özellikleri koruyan ve aynı zamanda çeşitlilik sağlayan veri artırma teknikleri kullanılmıştır.

## Özellikler

- Sınırlı sayıdaki görüntü setini (örneğin 53 görüntü) büyük bir veri setine (örneğin 1000 görüntü) dönüştürme
- Medikal görüntüler için özel olarak ayarlanmış veri artırma teknikleri
- İlerleme çubuğu ile işlem durumunu gerçek zamanlı takip etme
- Orijinal görüntüleri koruma seçeneği
- BMP formatını destekleme
- Hata yönetimi ve raporlama
- Özelleştirilebilir hedef görüntü sayısı

## Gereksinimler

- Python 3.6 veya üzeri
- OpenCV (`opencv-python`)
- NumPy
- tqdm (ilerleme çubuğu için)

## Kurulum

### 1. Python Kurulumu

Eğer sisteminizde Python kurulu değilse, [Python'un resmi web sitesinden](https://www.python.org/downloads/) indirebilirsiniz.

### 2. Gerekli Kütüphanelerin Kurulumu

Gerekli kütüphaneleri yüklemek için terminal veya komut isteminde aşağıdaki komutu çalıştırın:

```bash
pip install opencv-python numpy tqdm
```

### 3. Script'in İndirilmesi

Script dosyasını (`sperm_data_augmentation.py`) bilgisayarınıza indirin ve istediğiniz bir klasöre yerleştirin.

## Kullanım

Script'i aşağıdaki gibi çalıştırabilirsiniz:

```bash
python sperm_data_augmentation.py --input_dir /path/to/input/images --output_dir /path/to/output/images --target_count 1000 --preserve_originals
```

### Temel Kullanım

En basit haliyle, sadece giriş ve çıkış klasörlerini belirterek script'i çalıştırabilirsiniz:

```bash
python sperm_data_augmentation.py --input_dir /path/to/input/images --output_dir /path/to/output/images
```

Bu durumda, script varsayılan olarak 1000 görüntü oluşturacak ve orijinal görüntüleri çıkış klasörüne kopyalamayacaktır.

### Parametrelerle Kullanım

Tüm parametreleri kullanarak script'i çalıştırabilirsiniz:

```bash
python sperm_data_augmentation.py --input_dir /path/to/input/images --output_dir /path/to/output/images --target_count 1500 --preserve_originals
```

Bu durumda, script 1500 görüntü oluşturacak ve orijinal görüntüleri de çıkış klasörüne kopyalayacaktır.

## Veri Artırma Teknikleri

Script, aşağıdaki veri artırma tekniklerini kullanmaktadır:

1. **Hafif Döndürme (Rotate Small)**: 
   - Görüntüyü -10° ile +10° arasında rastgele açılarla döndürür
   - Sperm hücrelerinin doğal yönelim varyasyonlarını simüle eder
   - Ağırlık: %20

2. **Orta Seviye Döndürme (Rotate Medium)**: 
   - Görüntüyü -30° ile +30° arasında rastgele açılarla döndürür
   - Daha geniş açılı yönelim varyasyonları için kullanılır
   - Ağırlık: %10

3. **Yatay Çevirme (Flip Horizontal)**: 
   - Görüntüyü yatay eksende aynalar
   - Spermlerin farklı yönlerde olabileceğini simüle eder
   - Ağırlık: %15

4. **Dikey Çevirme (Flip Vertical)**: 
   - Görüntüyü dikey eksende aynalar
   - Farklı yönelimler sağlar
   - Ağırlık: %15

5. **Parlaklık ve Kontrast Ayarı**: 
   - Görüntünün parlaklık (beta: -15 ile +15 arası) ve kontrast (alpha: 0.8 ile 1.2 arası) değerlerini değiştirir
   - Farklı ışık koşullarını ve kamera ayarlarını simüle eder
   - Ağırlık: %10

6. **Gaussian Gürültü Ekleme**: 
   - Görüntüye kontrollü miktarda (sigma: 3 ile 10 arası) rastgele gürültü ekler
   - Kamera sensör gürültüsünü ve görüntüleme artefaktlarını simüle eder
   - Ağırlık: %5 (düşük ağırlık, çünkü medikal görüntülerde dikkatli kullanılmalı)

7. **Kırpma ve Yeniden Boyutlandırma**: 
   - Görüntünün rastgele bir bölümünü (%80 ile %95 arası) kırpıp orijinal boyuta geri getirir
   - Farklı zoom seviyelerini simüle eder
   - Ağırlık: %15

8. **Ölçeklendirme**: 
   - Görüntüyü büyütüp (x0.8 ile x1.2 arası) küçültür ve orijinal boyuta geri getirir
   - Farklı büyütme faktörlerini simüle eder
   - Ağırlık: %10

## Parametreler

Script aşağıdaki komut satırı parametrelerini desteklemektedir:

| Parametre | Açıklama | Zorunlu | Varsayılan Değer |
|-----------|----------|---------|------------------|
| `--input_dir` | Giriş görüntülerinin bulunduğu klasör | Evet | - |
| `--output_dir` | Çıkış görüntülerinin kaydedileceği klasör | Evet | - |
| `--target_count` | Hedeflenen toplam görüntü sayısı | Hayır | 1000 |
| `--preserve_originals` | Orijinal görüntüleri çıkış klasörüne kopyala | Hayır | False |

## Bilinen Sorunlar ve Çözümleri

### 1. Türkçe Karakterler İçeren Dosya Yolları Sorunu

**Sorun**: OpenCV, Türkçe karakterler (ı, İ, ş, ç, ö, ü, ğ vb.) içeren dosya yollarını doğru şekilde işleyemeyebilir. Bu durumda, görüntüler okunamaz ve veri artırma işlemi tamamlanamaz.

**Hata Mesajı Örneği**:
```
WARN:0@1.072] global loadsave.cpp:268 cv::findDecoder imread_('C:\Users\kullanıcı\Desktop\4.sınıf\BİTİRME\Data set\image.BMP'): can't open/read file: check file path/integrity
```

**Çözümler**:

1. **Dosya Yollarını Değiştirme**: 
   - Klasör ve dosya isimlerinde Türkçe karakter kullanmayın
   - Örneğin: `C:\Users\kullanıcı\Desktop\4.sınıf\BİTİRME\` yerine `C:\Users\kullanici\Desktop\4.sinif\BITIRME\` kullanın

2. **Görüntüleri Kopyalama**: 
   - Tüm görüntüleri ASCII karakterler içeren basit bir klasöre kopyalayın
   - Örneğin: `C:\temp\images\` gibi bir klasör oluşturup görüntüleri buraya kopyalayın
   - Script'i bu klasör üzerinde çalıştırın

3. **Script'i Güncelleme**: 
   - Aşağıdaki değişiklikleri içeren güncellenmiş bir script kullanın:
     - Dosya yollarını Unicode olarak işleme
     - Hata yönetimini iyileştirme
     - Okunamayan dosyaları atlama ancak işleme devam etme

### 2. Bellek Yetersizliği Sorunu

**Sorun**: Çok sayıda veya yüksek çözünürlüklü görüntü işlenirken bellek yetersizliği hatası alınabilir.

**Çözümler**:

1. **Batch İşleme**: 
   - Görüntüleri daha küçük gruplar halinde işleyin
   - Örneğin: 1000 görüntü yerine, 200'er görüntülük 5 grup oluşturun

2. **Görüntü Boyutunu Küçültme**: 
   - İşlem öncesinde görüntüleri daha düşük çözünürlüğe indirin
   - İşlem sonrasında gerekirse orijinal boyuta geri getirin

## Örnekler

### Örnek 1: Temel Kullanım

```bash
python sperm_data_augmentation.py --input_dir C:\sperm_images --output_dir C:\augmented_images
```

Bu komut, `C:\sperm_images` klasöründeki görüntüleri kullanarak toplam 1000 artırılmış görüntü oluşturacak ve `C:\augmented_images` klasörüne kaydedecektir.

### Örnek 2: Özel Hedef Sayısı ile Kullanım

```bash
python sperm_data_augmentation.py --input_dir C:\sperm_images --output_dir C:\augmented_images --target_count 500
```

Bu komut, toplam 500 artırılmış görüntü oluşturacaktır.

### Örnek 3: Orijinal Görüntüleri Koruyarak Kullanım

```bash
python sperm_data_augmentation.py --input_dir C:\sperm_images --output_dir C:\augmented_images --preserve_originals
```

Bu komut, orijinal görüntüleri de çıkış klasörüne kopyalayacaktır.

## Sık Sorulan Sorular

### 1. Script neden beklediğim sayıda görüntü oluşturmuyor?

Eğer script beklediğiniz sayıda görüntü oluşturmuyorsa, aşağıdaki nedenleri kontrol edin:
- Giriş klasöründeki bazı görüntüler okunamıyor olabilir (hata mesajlarını kontrol edin)
- Dosya yollarında Türkçe karakterler olabilir
- Görüntü formatı desteklenmiyor olabilir (script sadece .bmp formatını destekler)

### 2. Veri artırma için en iyi teknikler hangileridir?

Medikal görüntüler için en iyi veri artırma teknikleri, görüntünün temel özelliklerini ve tanısal değerini koruyan tekniklerdir. Bu nedenle, hafif döndürme, çevirme ve küçük parlaklık/kontrast değişiklikleri genellikle güvenlidir. Gürültü ekleme gibi teknikler daha dikkatli kullanılmalıdır.

### 3. Artırılmış görüntüler orijinallerden nasıl ayırt edilir?

Artırılmış görüntüler, dosya adlarında `_aug_` eki ve kullanılan tekniğin adını içerir. Örneğin: `image_001_aug_rotate_small_1.BMP`.

### 4. Script'i farklı görüntü formatları için kullanabilir miyim?

Bu script özellikle .bmp formatı için tasarlanmıştır, ancak küçük değişikliklerle diğer formatları da destekleyebilir. OpenCV, jpg, png, tiff gibi birçok formatı destekler.

