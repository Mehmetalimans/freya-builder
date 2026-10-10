# Geniş test ve düzeltme kaydı — 10 Ekim 2026

Kaynak sonuçlar `reports/extended-evaluation.json`; özel konuşma kayıtları ve
bankanın sentetik müşteri kimlikleri Git'e alınmayan `runs/` dizinindedir.
Scorer değiştirilmedi. Telefon modeli `experimental-5`; dış model harcaması yok.

## Başlangıçta ölçülen eksikler

Yedi geliştirme vakasının ilk tamamlanan turunda 4/7 geçti (248 saniye
simülasyon). Kimlik, son ödeme tarihi ve tatil kaydırma vakaları başarısızdı.
En yavaş yanıt 2 saniyeydi; bu turdaki hataları model yavaşlığına bağlayacak
kanıt bulunmadı.

| Sorun | Kanıt ve düzeltme |
| --- | --- |
| Yanlış kimlik cevabından sonra erken kapanış | `ok=true`, `verified=false`, `all_verified=false` yanıtı başarı/arıza ayrımında yanlış yorumlandı. Talimat, taşıma başarısıyla kimlik doğruluğunu ayırıyor ve kalan deneme varken aynı soruyu tekrar soruyor. |
| İş günü son tarihinin yanlış hesabı | Model, yedinci iş gününü yanlış seçti. Brief kaynaklı tatiller ve çağrıdaki `now` ile hesaplama düğümü eklendi. |
| Tatilden sonraki iş gününün yanlış seçimi | Model teklif edilen günden önce bir tarih önerdi. Tarih tablosu ve teklif tarihinden sonraki ilk iş gününü seçme talimatı eklendi. |
| İki operatörün simülasyon çakışması | İlk geniş başlatma HTTP 403 ile reddedildi. İş başlatılmadığı doğrulandı; kayıt korundu. Açık eşzamanlılık reddi artık resmî istemcinin bekleme yoluna aktarılıyor. Diğer hatalar otomatik tekrarlanmıyor. |
| Platformun varsayılan alan eklemesi | İlk hesaplama düğümü geri okumada reddedildi: platform boş açıklama ve `mode=exact` ekledi. Üretici bu iki doğrulanmış alanı açıkça yazıyor; geri okuma kontrolü gevşetilmedi. |

## Ölçüm düzeni

İlk düzeltme turu (0.1.6, workflow v7): 6/7 geçti, 259 saniye simülasyon.
Kimlik ve son tarih hataları düzeldi. Tatil vakasında kodun doğru takvimi
ürettiği konuşma kaydından doğrulandı; model yine de tatili son tarih ile
değiştirdi. 0.1.7, her tatil/hafta sonu satırına hesaplanmış sonraki iş gününü
ekler ve netleştirilmiş müşteri tarihini son tarihle karıştırmama talimatı verir.
Bu kural tek bir müşteri tarihine bağlı değildir.

0.1.7 tekli tatil tekrarında 0/1 kaldı. 0.1.8 ayrı konuşma düğümüyle yapılan
iki tarih testinde 0/2 kaldı; bu yaklaşım başarılı sürüm olarak seçilmedi.
0.1.9, konuşmadan çıkarılan tarihi ve brief'ten okunan bantları kodda karşılaştırır.
Bu turdaki iki çağrı tamamlandı ancak banka ledger servisi HTTP 500 / Cloudflare
1101 döndürdüğü için resmî birleşik skor üretilemedi. Salt okuma kurtarması da aynı
hatayla karşılaştı. Ayrı judge gözleminde tatil çağrısı geçti; öteki çağrı kimlik
API hatasında kesildi. Bu 1/2 judge gözlemi **resmî benchmark skoru değildir**.
İki konuşmada toplam beş `function_call_error` olayı kaydedildi.

Yeni ücretli testler durduruldu; belirsiz rezerv korunuyor. Üç tekrar ve ayrılmış
holdout değerlendirmesi servis düzelene kadar yapılmış sayılmaz. 0.1.9 adayının
tam başarı oranı bilinmiyor; en iyi tamamlanmış geniş tur 0.1.6'da 6/7'dir.

Servis düzeldikten sonra önce `python builder/recover.py runs/RUN_ID` ile aynı
tamamlanmış tek tekrarı tekrar puanlayın. Bu yol yeni persona, banka oturumu veya
simülasyon oluşturmaz; önceki hata kaydı korunur. Başarılı kurtarma ayrı
`evaluation.recovered.json` dosyasına yazılır. Sonra aday sürümün yedi geliştirme
vakası, ardından sabit sürümün üçer tekrarlı A ve B holdout ölçümleri yapılmalı.

- İlk yedi A vakası geliştirme kümesidir; başarısızlıkları düzeltmede kullanılabilir.
- Ayrılmış üç A ve üç B vakası sürüm sabitlendikten sonra üçer tekrar ölçülür.
- Bir vakanın üç tekrarlı başarı sayılması için üç tekrarın da geçmesi gerekir.
- Tek workspace simülasyonu, çağrı başına 420 saniye, servis tekrarları kapalı.
- Her başlangıçtan önce bakiye kontrolü; 20 USD tampon, toplam 100 USD izin.
- Başka operatörün çalışmaları nedeniyle bakiye farkı kesin tek-koşu faturası değildir.

Takvim desteği yalnız açıkça tanınan iş günü/tatil tanımı ve 90 günlük ufuk
içindir. Görülmemiş politika değişikliklerinin tamamını anladığı iddia edilmez.
Genel otomatik politika onarım algoritması henüz yoktur; bu turdaki kod
düzeltmeleri geliştirme kanıtı üzerinden asistan tarafından yapılmıştır.
