import cv2
import numpy as np
#Gerekli kütüphaneleri ve modülleri içeri aktarırız
altRenk = (75, 100, 100)
ustRenk = (130, 255, 255)
#Hedeflediğimiz nesnenin renk aralığını belirleriz
RENK = 'MAVI'
#Tespit edilen nesnelerin adını belirleriz
kamera = cv2.VideoCapture(0)
#Kamera erişimini sağlarız
cember = True
#Nesnelerin çember olarak çizilip çizilmeyeceğini belirleriz
while True:
#Ana döngüyü başlatırız:
    if not kamera.isOpened(): break
#Kameranın açılıp açılmadığını kontrol ederiz
    _,kare = kamera.read()
#Bir sonraki kareyi yakalarız:
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
#Kareyi HSV renk uzayına dönüştürürüz
    maske = cv2.inRange(hsv,altRenk,ustRenk)
#Belirlediğimiz renk aralığına göre maske oluştururuz
    kernel = np.ones((5,5),'int')
#Morfolojik işlemler için bir çekirdek (kernel) oluştururuz
    maske = cv2.dilate(maske,kernel)
#Maskeyi genişletiriz (dilate):
    res = cv2.bitwise_and(kare,kare,mask=maske)
#Orijinal kare üzerinde maskeyi uygularız:
    konturlar = cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
#findContours fonksiyonu, görüntüdeki konturları bulur.
#maske.copy() ile maske kopyası üzerinde konturları buluruz.
#cv2.RETR_EXTERNAL parametresi, yalnızca dış konturları almayı sağlar.
#cv2.CHAIN_APPROX_SIMPLE parametresi, kontur verilerini basit bir şekilde temsil etmeyi sağlar.
#[-2] ile kontur sonuçlarını alırız.
    say = 0
    for kontur in konturlar:
        alan = cv2.contourArea(kontur)
        if alan > 600:
            say+=1
            (x,y,w,h)=cv2.boundingRect(kontur)
            cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if cember:
                (x, y), ycap = cv2.minEnclosingCircle(kontur)
                merkez = (int(x), int(y))
                ycap = int(ycap)
                img = cv2.circle(kare, merkez, ycap, (255, 0, 0), 2)
#say değişkeni, belirlenen alan sınırlamasını aşan nesnelerin sayısını tutar.
#Her kontur için döngüye gireriz.
#cv2.contourArea(kontur) ile konturun alanını hesaplarız.
#Eğer alan, 600'den büyükse:
#say değişkenini bir artırırız.
#cv2.boundingRect(kontur) ile konturun çevreleyen dikdörtgenin koordinatlarını alırız.
#cv2.rectangle ile kare üzerinde konturu çevreleyen dikdörtgeni çizeriz.
#Eğer cember True ise:
#cv2.minEnclosingCircle(kontur) ile konturun etrafını saran en küçük çemberin merkezini ve yarıçapını buluruz.
#Çemberi kare üzerinde çizeriz.
    if say > 0:
        cv2.putText(kare, f'{say} {RENK} nesne bulundu', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
#Eğer say değeri 0'dan büyükse:
#Nesne sayısını ve adını ekrana yazdırmak için cv2.putText fonksiyonunu kullanırız.
    cv2.imshow('kare', kare)
#'kare' adıyla pencere açar ve kare değişkenini gösterir.
    k = cv2.waitKey(4) & 0xFF
#Klavyeden bir tuşa basılmasını bekler ve basılan tuşun ASCII değerini k değişkenine atar.
#cv2.waitKey fonksiyonunun parametresi, bekleme süresini milisaniye cinsinden belirtir.
    if k == 27: break
#Eğer basılan tuşun ASCII değeri 27 (ESC tuşu) ise döngüden çıkar ve programı sonlandırır.
if kamera.isOpened():
    kamera.release()
#Kamera hala açıksa, kamera erişimini serbest bırakır.
cv2.destroyAllWindows()
#Tüm açık pencereleri kapatır ve belleği temizler.