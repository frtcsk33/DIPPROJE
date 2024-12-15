import cv2
import pytesseract
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'

# Tesseract'ın sistemdeki yolunu ayarlayın (Windows için gerekebilir)
# Örnek: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Görüntüyü yükle
image_path = r"C:\Users\frtcs\Desktop\book.webp"
img = cv2.imread(image_path)

# Görüntüyü gri tonlamaya dönüştür
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tesseract ile metin tespiti
custom_config = r'--oem 3 --psm 6'  # OCR motor modu ve sayfa segmentasyon modu
detection_data = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)

threshold = 0.25  # Güven skoru eşik değeri (0-1 arasında)

# Metinleri ve sınırlayıcı kutuları çiz
print("Tespit Edilen Metinler:")
for i in range(len(detection_data['text'])):
    text = detection_data['text'][i]
    conf = int(detection_data['conf'][i])  # Tesseract'tan güven skoru alır

    if text.strip() and conf > (threshold * 100):  # Metin boş değil ve güven skoru yeterliyse
        x, y, w, h = (detection_data['left'][i], detection_data['top'][i],
                      detection_data['width'][i], detection_data['height'][i])
        # Sınırlayıcı kutu çiz
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Tespit edilen metni yazdır
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # Tespit edilen metni ve güven skorunu yazdır
        print(f"Metin: {text}, Guven Skoru: {conf}")

# Görüntüyü matplotlib ile göster
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()