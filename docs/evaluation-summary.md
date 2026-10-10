# Ölçümler, başarısız denemeler ve açık işler

**Güncelleme:** Aşağıdaki 0.1.3–0.1.9 tablosu ilk raporun tarihsel kaydıdır.
Sonradan 0.1.9 salt okunur kurtarmayla 1/2 puanlandı; 0.1.10 üç tekrarda 6/7
vaka, 19/21 çağrı geçti. Sonraki adaylar ve güncel ölçümler
[canlı doğrulama kaydında](live-validation.md) ve
[`reports/live-validation.json`](../reports/live-validation.json) tutulur.
98 yerel test, son kod adayına aittir; aşağıdaki eski sayılar korunmuştur.

Bu belge 10 Ekim 2026'daki kayıtların özetidir; yeni canlı test veya güncel servis
sağlığı kontrolü değildir. İncelenen kod sürümü **0.1.9**, kod commit'i
`a05c54341c3fcf37fd0afd3d1c6d4fd498d27659`; rapor ve paket güncellemesi `e390cc4`.
0.1.9 hâlâ adaydır; final teslimi hazır sayılmaz.

## Denemeler ve ölçümler

Kaynak: [geniş test verisi](../reports/extended-evaluation.json) ve
[ilk pilot](../reports/first-live-evaluation.json). Aşağıdaki süreler
`seconds` alanındaki **değerlendirme toplam süresidir**; yalnız konuşma süresi
değildir. Tüm ölçümler public geliştirme vakalarında tek tekrarlıdır.

| Sürüm / koşu | Kapsam | Birleşik sonuç | Toplam süre (sn) | Gözlenen bakiye düşüşü (USD) |
| --- | --- | --- | ---: | ---: |
| 0.1.3 / `20261010T143548Z-dcb3f232` | İlk pilot, PUB-01 | 1/1 | 79,953 | 0,01995 |
| 0.1.4 / `20261010T150504Z-9f03bf6c` | Yedi vaka başlatma girişimi | HTTP 403; çağrı başlamadı | 3,422 | 0 |
| 0.1.4 / `20261010T150901Z-e1defbd9` | PUB-01–07 | 4/7 | 255,157 | 0,18040 |
| 0.1.6 / `20261010T151623Z-f44d3290` | PUB-01–07 | 6/7 | 349,734 | 0,20295 |
| 0.1.7 / `20261010T152338Z-7424aeff` | PUB-07 | 0/1 | 44,344 | 0,03245 |
| 0.1.8 / `20261010T152719Z-f7a30f49` | PUB-04, PUB-07 | 0/2 | 105,578 | 0,08405 |
| 0.1.9 / `20261010T153230Z-22e5b9a3` | PUB-04, PUB-07 | Çağrılar tamamlandı; ledger hatası nedeniyle skor bilinmiyor | 155,828 | 0,12175 |

Geniş kampanyada pilot hariç **19 gerçek çağrı**, bunların **17'sinde birleşik
puanlama** var. Sürümler ve vaka altkümeleri farklı olduğundan tek toplam başarı
oranı hesaplanmadı. En iyi tamamlanmış yedi vakalık tur 0.1.6 ile 6/7'dir;
bu sonuç 0.1.9'a ait değildir. Son iki çağrıdaki judge-only 1/2 gözlemi,
banka kaydıyla birleşik resmî skor yerine kullanılamaz.

Kayıtlı en son bakiye **98,83555 USD**; güncel bakiye olduğu iddia edilmez.
Tablodaki farklar başka workspace faaliyetlerini veya gecikmeli tahsilatı
içerebilir. Kesin faturalanmış tutar bütün koşularda `actual_cost_usd=null`.
100 USD'den toplam düşüşün tamamı bizim testlerimize atfedilemez. Dış model API
harcaması yoktur. Ayrıntı: [fiyat analizi](cost-analysis.md).

## Hata kaydı ve düzeltmenin kanıtı

| Hata | Yapılan değişiklik / gözlenen sonuç | Durum |
| --- | --- | --- |
| PUB-03: yanlış kimlik yanıtını teknik arıza sayıp erken kapatma | İşlem başarısı ile `verified` ayrıldı; 0.1.6 turunda bu vaka geçti. | Tek tekrar ile doğrulandı; üç tekrar bekliyor. |
| PUB-04: ürünün son ödeme tarihini yanlış hesaplama | Brief ve çağrıdaki `now` üzerinden takvim eklendi; 0.1.6 geçti, 0.1.8 yeniden başarısız oldu. | Kalıcı çözüm kanıtlanmadı; 0.1.9 ölçümü eksik. |
| PUB-07: tatil sonrasındaki iş gününü son tarihle karıştırma | 0.1.7 talimatı ve 0.1.8 konuşma düğümü başarısız kaldı. 0.1.9 ürün bazlı tarih karşılaştırması ekledi. | Son aday için yalnız olumlu judge gözlemi var; birleşik doğrulama bekliyor. |
| Eşzamanlı simülasyon reddi | Belgeli 403 eşzamanlılık hatası resmî bekleme yoluna yönlendirildi; reddedilen girişim başarı sayılmadı. | Farklı bilgisayarlar ayrıca koordine edilmeli. |
| Platform geri okuma uyuşmazlığı | `20261010T151541Z-44239f69` dağıtımı 7,531 sn sonra durdu; test başlamadı. Platformun eklediği boş açıklama ve `mode=exact` üreticide açık yazıldı. | Sonraki dağıtım geri okumayı geçti. |
| Banka ledger HTTP 500 / Cloudflare 1101 | Yeni ücretli işler durduruldu; salt okuma kurtarması da başarısız kaldı. Orijinal kayıt ve rezerv korundu. | Son kontrolde engeldi; bu belge servis sağlığını yeniden ölçmedi. |

Son adayın iki çağrısında beş araç hata olayı görüldü. Bunlar beş başarısız
vaka anlamına gelmez. Önceki turlarda gözlenen araç hata sayısının sıfır olması da
doğru iş kararı verildiğini kanıtlamaz. Teknik ayrıntılar:
[hata ve düzeltme günlüğü](extended-test-notes.md).

## Bilinen sınırlamalar ve tamamlanma koşulları

| Konu | Mevcut sınır | Tamamlanma kanıtı |
| --- | --- | --- |
| Son adayın başarısı | 0.1.9 tam geliştirme turu ölçülmedi. | Önce bekleyen turu kurtar; ardından yedi geliştirme vakasında üç tekrarı raporla. |
| Genelleme | Ayrılmış üç A ve üç B holdout vakası çalıştırılmadı. | Kodu sabitle; iki workflow'u ayrı ayrı üçer tekrar ölç. Bu sonuçlarla düzeltme yapıp aynı kümeden bağımsız başarı iddia etme. |
| Politika çıkarımı | Yalnız tanınan takvim/bant dilbilgisi ve 90 günlük ufuk destekleniyor. | Tanınmayan girdileri açıkça raporla; görülmemiş brief başarısını ölçmeden iddia etme. |
| Diyalog | Tarih çıkarımı, açıklama ve müşteri onayı hâlâ modele bağlı. | Yanlış/eksik çıkarım ve ürün bazlı kayıtları birleşik scorer ile doğrula. |
| Otomatik onarım | Genel bir otomatik onarım motoru yok; mevcut düzeltmeleri asistan yaptı. | Geliştirme geri bildirimiyle sınırlı döngü uygulanıp ölçülmeden var sayma. |
| Maliyet | Vaka başına doğrulanmış azami ücret yok; 20 USD tampon servis tarafı harcama kilidi değil. | Her yeni simülasyondan önce bakiye ve bekleyen iş kontrolünü sürdür. |
| Tekrar üretim | Kaynak paket temiz Windows ortamında doğrulandı; macOS kontrol edilmedi. | Final kod ve export/izleri sabitlendikten sonra temiz ortam kontrolünü yenile. |
| Teslim | Gizli brief sonuçları, iki final export/iz ve organizatörün son teslim adımları eksik. | Kesin commit ve resmî teslim koşullarıyla tamamla. |

[Tarihsel temiz ortam raporu](https://github.com/Mehmetalimans/freya-builder/blob/e390cc4/reports/verification.json) 39 birim testinin geçtiği
doğrulama çalışmasına, A ve A+B için tekrarlanan eşit workflow hash'lerine ve
sıfır üçüncü taraf bağımlılığına aittir. Bu kontroller canlı görev başarısı değildir.
Kod commit'inin [Linux CI çalışması](https://github.com/Mehmetalimans/freya-builder/actions/runs/38065145260)
başarılıdır. Bu belge daha sonra yapılan dokümantasyon değişikliklerinin aynı
arşiv hash'ine sahip olduğunu iddia etmez.

Sonraki 0.1.10 incelemesi ve 90 yerel test sonucu
[ayrı belgede](mirac-integration-review.md), güncel temiz ortam sonucu ise
`reports/verification.json` içindedir. Ekip raporu B vakalarının kullanıldığını
bildirdiğinden yukarıdaki altı vakalık holdout planının B kısmı artık bağımsız
genelleme ölçümü değildir; tekrarları regresyon olarak raporlanmalıdır.

## Kod incelemesi ve ekip devri

Arkadaşın `daef83b` commit'indeki altı bulgu, kaynak bağlantıları ve kabul
ölçütleriyle [kod incelemesinde](teammate-code-review.md) tutulur. Bunlar kod
incelemesi bulgularıdır; arkadaşın dalında canlı olarak yeniden üretilmiş test
sonucu değildir. Bu daldaki önlemler arkadaşın dalının düzeltilmiş veya
birleştirilmiş olduğu anlamına gelmez.

Özel ham kayıtlar `runs/` içinde yerel kalır. Bu belgelerde anahtar, müşteri
değişkenleri veya tam konuşma kaydı yayımlanmaz. Devam sırası ve sahipler:
[görevler](tasks.md). Yeni testten önce bekleyen `20261010T153230Z-22e5b9a3`
sonucu salt okunur kurtarma yoluyla ele alınmalıdır.
