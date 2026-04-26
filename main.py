import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg"
resp = urllib.request.urlopen(url)
img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.imshow(img_rgb)
plt.title("Obraz")
plt.axis("off")
plt.show()

# Histogram
hist = cv2.calcHist([gray], [0], None, [256], [0,256])
plt.plot(hist)
plt.title("Histogram")
plt.show()

# Analiza jakości
mean = np.mean(gray)        # jasność
std = np.std(gray)          # kontrast
dark_pixels = np.sum(gray < 50) / gray.size
bright_pixels = np.sum(gray > 200) / gray.size

print("Średnia jasność:", round(mean,2))
print("Kontrast (std):", round(std,2))
print("Ciemne piksele:", round(dark_pixels,2))
print("Jasne piksele:", round(bright_pixels,2))

# Ocena

score = 0

# Jasność
if 80 < mean < 180:
    score += 1
else:
    print("Problem z jasnością")

# Kontrast
if std > 50:
    score += 1
else:
    print("Niski kontrast")

# Prześwietlenie / niedoświetlenie
if dark_pixels < 0.5 and bright_pixels < 0.5:
    score += 1
else:
    print("Dużo skrajnych pikseli")

print("\nOcena jakości:", score, "/ 3")

if score == 3:
    print("Dobra jakość")
elif score == 2:
    print("Średnia jakość")
else:
    print("Słaba jakość")

# Automatyczna poprawa

better = gray.copy()

# Poprawianie kontrastu
if std < 50:
    better = cv2.equalizeHist(better)

# Rozjaśnianie
if mean < 80:
    better = cv2.convertScaleAbs(better, alpha=1.2, beta=30)

# Przyciemnianie
if mean > 180:
    better = cv2.convertScaleAbs(better, alpha=0.8, beta=-30)

# Wynik
plt.imshow(better, cmap='gray')
plt.title("Poprawione zdjęcie")
plt.axis("off")
plt.show()
