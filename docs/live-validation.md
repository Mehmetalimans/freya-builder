# Canlı doğrulama — 10 Ekim 2026

**Ara verildi:** 0.1.11'in ilk iki tekrarı 6/7 ve 7/7; üçüncü tur sırasında
kullanıcı durma istedi. 0.1.12 yalnız kod/temiz ortam doğrulaması aşamasında.
[Devam kaydı](resume-checkpoint.md) ve [son uzak durum](../reports/live-pause.json).

Bu ölçümler public practice vakalarıdır, gizli final benchmark sonucu değildir.
Ham kayıtlar `runs/` altında yerel tutulur; paylaşılabilir özet
[`reports/live-validation.json`](../reports/live-validation.json) dosyasındadır.
Resmî v3 scorer değiştirilmedi. Bir vaka ancak tüm tekrarları geçtiğinde başarılıdır.

## Önceki engelin çözülmesi

0.1.9'un tamamlanmış iki çağrısı banka ledger servisi düzeldikten sonra yeni
simülasyon başlatmadan tekrar okundu: 1/2. PUB-04'te kimlik aracı hataları ve
eksik banka işlemleri, PUB-07'de başarı görüldü. Orijinal engellenmiş kayıt
korundu; kurtarma sonucu ayrı dosyada. Önceki rezerv bundan sonra kapatıldı.

## 0.1.10: uzun başlangıç ölçümü

Workflow `82c69318-2c6a-43d3-9661-a93ea8b9b99d`, yayımlanan sürüm 11;
hash `cfbdfbaed62f4cc726fbf60ccd90db89e9a09f7242d575ba8a10327bf4e1a4af`.
Yayın, export ve geri okuma doğrulandı. A geliştirme kümesindeki yedi vaka üç
kez çalıştı: **7/7, 6/7, 6/7**. Toplam 19/21 çağrı geçti; üç tekrarda da geçme
ölçütüyle **6/7 vaka**, değerlendirme süresi **1447,297 saniye**.

İki başarısızlık PUB-07'deydi: müşteri belirsiz dönem söylediğinde tam gün
sorulmadan belirli tarih önerildi. Bu konuşmadaki araçların çalışması politika
uyumunu garanti etmedi. Başarısız sonuçlar silinmedi ve farklı sürümün skoruna
katılmadı.

## 0.1.11: ölçülmekte olan düzeltme

Kesin tarih yanında müşterinin gerçek ödeme tarihi ifadesi de çıkarılır.
İfade açık bir gün içermiyorsa hesaplama sonucu kullanılmaz; netleştirme istenir.
Bu kontrol İngilizce tarih ifadeleriyle sınırlı; alıntı ve tarih çıkarımı yine
modele bağlıdır. 96 yerel test ve temiz, pip içermeyen Python 3.12.14 doğrulaması
geçti. A workflow'u v12 olarak yayımlandı ve geri okuma doğrulandı.
Canlı üç tekrar sonucu tamamlanmadan başarı iddiası yapılmaz.

Tek workspace simülasyonu korunur; yeni testlerde aynı simülasyonun içinde
en fazla iki çağrı yürür. Otomatik HTTP/başarısız çağrı tekrarı kapalıdır.
Tüm geliştirme ve kalan public ölçümler aynı sabit workflow hash'iyle raporlanır.
B vakaları ekip tarafından daha önce kullanılmıştır: bunlar bağımsız holdout
değil regresyon ölçümüdür. Kalan A vakalarının ekip kullanım geçmişi de
doğrulanmadığından ekip genelinde bağımsızlık iddia edilmez.

0.1.11 ilk tekrarında yazıyla söylenen bir gün (`six November`) geçerli tarih
olarak çıkarıldı, ancak yerel gün-ifadesi denetimi bunu tanımadı. Hesaplama
kullanılamaz fallback'ine rağmen telefon modeli son tarihin dışındaki ödemeyi
kabul etti. 0.1.12 adayı, ayla birlikte veya tek başına söylenen 1–31 sayılarının
yazılı biçimlerini de kabul eder; belirsiz süre/para ifadelerini gün saymaz.
İki yeni regresyon testiyle toplam 98 test geçti. Yeni canlı ölçüm bekleniyor;
0.1.11'in devam eden simülasyonu sırasında yayımlanmış workflow değiştirilmedi.

## Maliyet ve teslim sınırı

0.1.10 sırasında workspace'e kredi eklendi; bu oturum satın alım yapmadı.
Negatif bakiye farkı gelir veya negatif maliyet sayılmaz. Toplam izin hâlâ
100 USD Freya; kullanım sayacıyla 20 USD tampon korunur. Gerçek fatura
bilinmediğinden `actual_cost_usd=null`. [Maliyet hesabı](cost-analysis.md).

Builder modeli için ücretli dış API çağrısı yok. Görülmemiş brief başarısı,
genel otomatik onarım motoru veya final teslimi tamamlanmış sayılmaz.
İki final brief, ilgili export/iz ve organizatörün son teslim adımları beklenir.
