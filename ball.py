import cv2
import imutils
from collections import deque
import random
import time
import numpy as np

TopMax = 10 #aynı anda görülen top sayısı
MaxSure= 60 #oyunun max süresi
Width = 1000 #pencere genişliği
MaxKuyruk= 2 #izleyici kuyruğundaki en fazla nokta sayısı
MinCap = 6 #işaretçi için alt boyut sınırı
Font = 'verdana.ttf'

def top_ekle(toplist,kare):
    while True:
        if len(toplist)>=TopMax:
            break
        y = random .randint(0,kare.shape[0])
        x = random .randint(0,kare.shape[1])
        
        toplist.append((y,x))
    return toplist


def ana():
    kamera = cv2.VideoCapture(0)
    kuyruk = deque(maxlen=MaxKuyruk)
    top = cv2.imread('sari_top.png',-1)
    topmaske = top[:,:,3]
    ters_topmaske = cv2.bitwise_not(topmaske)
    top = top[:,:,:3]
    toph,topw = top.shape[:2]
    toplist=[]
    xt=int(0)
    yt=int(0)
    puan = 0
    t0=time.time()
    kaydet_ad = None #'toptopla.mp4'
    kaydet = None
    
    while True:
        if time.time() - t0 > MaxSure:
            print("Oyun Sonu! Toplam Puanınız:", puan)
            break
        
        _, kare = kamera.read()
        kare = cv2.flip(kare, 1)  # ayna görüntüsü
        kare = imutils.resize(kare, Width)
        hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
        
        # top sayısı eksikse tamamla
        toplist = top_ekle(toplist, kare)
        
        for j in range(len(toplist)):
            try:
                (yt, xt) = toplist[j]
                parca = kare[yt:yt+toph, xt:xt+topw]
                alt_parca = cv2.bitwise_and(parca, parca, mask=ters_topmaske)
                ust_parca = cv2.bitwise_and(top, top, mask=topmaske)
                kare[yt:yt+toph, xt:xt+topw] = cv2.add(alt_parca, ust_parca)
            except:
                try:
                    print(j, len(toplist), toplist[j], toplist)
                    toplist.pop(j)
                except:
                    pass
                continue
            
            # mavi renk
            alt_renk = np.array([110, 50, 50])
            ust_renk = np.array([130, 255, 255])
            maske = cv2.inRange(hsv, alt_renk, ust_renk)
            maske = cv2.erode(maske, None, iterations=3)
            maske = cv2.dilate(maske, None, iterations=3)
            kenarlar = cv2.findContours(maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            
            merkez = None
            if len(kenarlar) > 0:
                kmax = max(kenarlar, key=cv2.contourArea)  # en büyük alana sahip sınır
                for kenar in kenarlar:
                    (x, y), ycap = cv2.minEnclosingCircle(kmax)
                    if ycap > MinCap:
                        cv2.circle(kare, (int(x), int(y)), int(ycap), (255, 255, 0), 2)
                        moments = cv2.moments(kmax)
                        merkez = (int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00']))
                        
                        for i in range(1, len(kuyruk)):
                            if kuyruk[i-1] and kuyruk[i]:
                                kal = 1 + int(np.log(MaxKuyruk / i) * 1.3)
                                cv2.line(kare, kuyruk[i-1], kuyruk[i], (255, 0, 255), kal)
                                
                                # merkez ile çakışan top varsa sil ve puan ekle
                                if merkez:
                                    for j in range(len(toplist)):
                                        try:
                                            yt, xt = toplist[j]
                                            if (merkez[1] > yt and merkez[1] < (yt+toph)) and (merkez[0] > xt and merkez[0] < (xt+topw)):
                                                del toplist[j]
                                                puan += 1
                                        except:
                                            continue

            text = f"Puan: {str(puan)} Kalan süre: {MaxSure - (time.time() - t0):.3f}"
            renk= (0, 0, 0)
            
            kare = print_utf8_text(kare,text,Font,renk)
            cv2.imshow('kare',kare)
            cv2.moveWindow('kare',10,10)

            if kaydet is None and kaydet_ad is not None:
                fourcc=cv2.VideoWriter_fourcc(*"mp4v")
                kaydet = cv2.VideoWriter(kaydet_ad,fourcc,24.0,(kare.shape[0]),True)
            if kaydet is not None:
                kaydet.write(kare)
            k =cv2.waitKey(1) & 0xFF
            if k ==27 or k == orf('q'):
                break
            #oyun sonunda puan ver uyarı
            while True:
                _,kare = kamera.read()
                kare = cv2.flip(kare,1)#ayna görüntüsü
                kare = imutils.resize(kare,Width)
                text = "Oyun Bitti ! Puanın : " +str(puan)
                renk =(0,0,0)
                kare =  print_utf8_text(kare,text,Font,renk)
                cv2.imshow('kare',kare)
                if kaydet is not None:
                    kaydet.write(kare)
                k =cv2.waitKey(1) & 0xFF
                if k ==27 or k == orf('q'):
                    break
                kamera.release()
                if kaydet:kaydet.release()
                cv2.destroyAllWindows()
            if __name__=="__main__":
                ana()
                
            
                

            

           



        
    
                                
                                
                                
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        
    
    
    
    
    
    
    
    
    
    



