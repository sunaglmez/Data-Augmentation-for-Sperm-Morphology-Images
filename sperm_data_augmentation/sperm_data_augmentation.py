#!/usr/bin/env python3
"""
Sperm Morfolojisi Görüntüleri için Veri Artırma (Data Augmentation) Scripti

Bu script, sperm morfolojisi görüntülerini çeşitli teknikler kullanarak artırır.
Medikal görüntüler için uygun veri artırma teknikleri kullanılmıştır.

Kullanım:
    python sperm_data_augmentation.py --input_dir /path/to/input/images --output_dir /path/to/output/images --target_count 1000
"""

import os
import argparse
import numpy as np
import cv2
from tqdm import tqdm
import random
import shutil
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description='Sperm morfolojisi görüntüleri için veri artırma')
    parser.add_argument('--input_dir', type=str, required=True, help='Giriş görüntülerinin bulunduğu klasör')
    parser.add_argument('--output_dir', type=str, required=True, help='Çıkış görüntülerinin kaydedileceği klasör')
    parser.add_argument('--target_count', type=int, default=1000, help='Hedeflenen toplam görüntü sayısı (varsayılan: 1000)')
    parser.add_argument('--preserve_originals', action='store_true', help='Orijinal görüntüleri çıkış klasörüne kopyala')
    return parser.parse_args()

def create_output_directory(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Çıkış klasörü oluşturuldu: {output_dir}")

def get_image_files(input_dir):
    image_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith('.bmp'):
            image_files.append(os.path.join(input_dir, file))
    return image_files

def copy_originals(image_files, output_dir):
    for img_path in image_files:
        filename = os.path.basename(img_path)
        shutil.copy(img_path, os.path.join(output_dir, filename))
    print(f"{len(image_files)} orijinal görüntü çıkış klasörüne kopyalandı.")

def rotate_image(image, angle):
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (width, height), borderMode=cv2.BORDER_REPLICATE)

def flip_image(image, flip_code):
    return cv2.flip(image, flip_code)

def adjust_brightness_contrast(image, alpha, beta):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def add_gaussian_noise(image, mean=0, sigma=5):
    row, col, ch = image.shape
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = image + gauss
    return np.clip(noisy, 0, 255).astype(np.uint8)

def crop_and_resize(image, crop_percent=0.8):
    height, width = image.shape[:2]
    crop_height = int(height * crop_percent)
    crop_width = int(width * crop_percent)
    start_x = random.randint(0, width - crop_width)
    start_y = random.randint(0, height - crop_height)
    cropped = image[start_y:start_y+crop_height, start_x:start_x+crop_width]
    return cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LINEAR)

def scale_image(image, scale_factor):
    height, width = image.shape[:2]
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)
    scaled = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(scaled, (width, height), interpolation=cv2.INTER_LINEAR)

def apply_augmentation(image, aug_type):
    if aug_type == 'rotate_small':
        angle = random.uniform(-10, 10)
        return rotate_image(image, angle)
    elif aug_type == 'flip_horizontal':
        return flip_image(image, 1)
    elif aug_type == 'flip_vertical':
        return flip_image(image, 0)
    elif aug_type == 'brightness_contrast':
        alpha = random.uniform(0.8, 1.2)
        beta = random.randint(-15, 15)
        return adjust_brightness_contrast(image, alpha, beta)
    elif aug_type == 'gaussian_noise':
        sigma = random.uniform(3, 10)
        return add_gaussian_noise(image, sigma=sigma)
    elif aug_type == 'crop_resize':
        crop_percent = random.uniform(0.8, 0.95)
        return crop_and_resize(image, crop_percent)
    elif aug_type == 'scale':
        scale_factor = random.uniform(0.8, 1.2)
        return scale_image(image, scale_factor)
    else:
        return image

def generate_augmented_images(image_files, output_dir, target_count, preserve_originals=False):
    if preserve_originals:
        copy_originals(image_files, output_dir)
        current_count = len(image_files)
    else:
        current_count = 0

    augmentation_types = [
        'rotate_small',
        'flip_horizontal',
        'flip_vertical',
        'brightness_contrast',
        'gaussian_noise',
        'crop_resize',
        'scale'
    ]

    weights = [
        0.25,  # rotate_small
        0.2,   # flip_horizontal
        0.2,   # flip_vertical
        0.15,  # brightness_contrast
        0.05,  # gaussian_noise
        0.1,   # crop_resize
        0.05   # scale
    ]

    remaining_count = target_count - current_count
    if remaining_count <= 0:
        print("Hedef görüntü sayısına ulaşıldı veya aşıldı.")
        return

    augmentations_per_image = remaining_count // len(image_files)
    extra_augmentations = remaining_count % len(image_files)

    print(f"Her bir görüntü için {augmentations_per_image} artırılmış görüntü oluşturulacak.")
    if extra_augmentations > 0:
        print(f"Ek olarak {extra_augmentations} görüntü daha oluşturulacak.")

    total_operations = remaining_count

    with tqdm(total=total_operations, desc="Veri artırma işlemi") as pbar:
        for img_path in image_files:
            image = cv2.imread(img_path)
            if image is None:
                print(f"Uyarı: {img_path} okunamadı, atlanıyor.")
                continue

            filename = os.path.basename(img_path)
            name, ext = os.path.splitext(filename)

            num_augmentations = augmentations_per_image
            if extra_augmentations > 0:
                num_augmentations += 1
                extra_augmentations -= 1

            for i in range(num_augmentations):
                aug_type = random.choices(augmentation_types, weights=weights, k=1)[0]
                augmented_image = apply_augmentation(image.copy(), aug_type)
                aug_filename = f"{name}_aug_{aug_type}_{i+1}{ext}"
                output_path = os.path.join(output_dir, aug_filename)
                cv2.imwrite(output_path, augmented_image)
                pbar.update(1)
                current_count += 1
                if current_count >= target_count:
                    break
            if current_count >= target_count:
                break

    final_count = len([f for f in os.listdir(output_dir) if f.lower().endswith('.bmp')])
    print(f"\nVeri artırma tamamlandı. Toplam {final_count} görüntü oluşturuldu.")

def main():
    args = parse_arguments()
    create_output_directory(args.output_dir)
    image_files = get_image_files(args.input_dir)
    print(f"Giriş klasöründe {len(image_files)} .bmp görüntüsü bulundu.")

    if not image_files:
        print("Hata: Giriş klasöründe .bmp görüntüsü bulunamadı.")
        return

    generate_augmented_images(
        image_files, 
        args.output_dir, 
        args.target_count, 
        args.preserve_originals
    )

if __name__ == "__main__":
    main()