# Freya fiyat analizi — 10 Ekim 2026

## Doğrulanan tutarlar

Hedef: Mirac Birlik's Workspace, `8783bb12-56fc-489a-8608-590676971f6c`.
14:34–14:37 UTC aralığında kendi workspace API'si ve Billing ekranı incelendi.

| Kalem | Gözlem | Anlamı |
| --- | --- | --- |
| Kredi | `creditsLeft=200` | Kullanılabilir kredi birimi |
| Dönüşüm | `creditUsdRate=0.5`, `billingUnit=usd` | 200 × 0,50 = **100 USD** bakiye; dakika veya vaka fiyatı değil |
| Kullanım | `totalCreditsUsed=0`, boş günlük tüketim/kategori dökümü | Sorgu anında kaydedilmiş tüketim yok |
| İşlem adedi | `totalTransactions=2` | İki çağrı/test demek değildir; işlem türleri bu yanıtta yok |
| API dağıtımı sonrası | Bakiye hâlâ 200 kredi | Bu gözlem gelecekteki dağıtımların ücretsiz olduğuna garanti değildir |
| Builder dış model maliyeti | 0 USD, 0 çağrı | Deterministik Python üretimi dış model API'si kullanmıyor |
| Simülasyon başına maliyet | **Bilinmiyor** | Henüz bir simülasyon çalıştırılmadı |

Kaynaklar: [kredi API belgesi](https://docs.freyavoice.ai/api-reference/workspace-credits/get-credits),
[kullanım API belgesi](https://docs.freyavoice.ai/api-reference/analytics/get-credits-analytics),
[workspace Billing](https://staging-app.freyavoice.ai/workspace/billing?workspaceId=8783bb12-56fc-489a-8608-590676971f6c).
Ham, anahtarsız yanıtlar yerelde `runs/mail-api-preflight/` altında tutulur.
Tarihli kullanım sorgusu HTTP 500 verdi; belgede isteğe bağlı olan tarih alanları
çıkarılınca aynı belgeli uç nokta başarılı oldu. Sunucu hata gövdesi kaydedilmedi.

## Fiyatı neden hesaplayamıyoruz?

[Resmî fiyat sayfası](https://www.freyavoice.ai/pricing) genel ürün için proje
bazlı teklif verildiğini söylüyor; hackathon metin simülasyonu için dakika,
token, vaka veya judge tarifesi yayımlamıyor. Sayfadaki “API Pricing” bağlantısı
da aynı sayfaya gidiyor. Başka sağlayıcının Google liste fiyatını Freya ücreti
olarak kullanmak doğru olmaz.

[Kickoff kaydının](https://fathom.video/share/SCFTpw9gPFqxxEqk49PbM3HFjSros35m)
görünen transkriptinde başlangıçtaki 10 USD'nin artırılacağı söyleniyor. Artırımın
kapsamı, negatif bakiye/otomatik yükleme davranışı veya vaka başına ücret burada
verilmiyor. Kayıt ayrıca gizli brief dönemindeki platform test limitinin daha
sonra açıklanacağını belirtiyor; yeni organizatör mesajı izlenmeli. Otomatik
toplantı özetindeki Cumartesi tarihi e-postayla çeliştiğinden güncel yazılı
e-posta ve yarışma sayfasındaki **Pazar 11 Ekim** takvimi esas alındı.

Resmî kit bir çağrı için 420 saniyelik süre sınırı kullanır; telefon modeli
`experimental-5`, müşteri ve judge `google/gemini-3-flash-preview` olur. Metin
simülasyonunda yedi dakika sınırı bir dolar tavanı değildir. Genel
[simülasyon şeması](https://docs.freyavoice.ai/api-reference/simulations/create-simulation)
`maxRetries` alanı da içerir; kit bu alanı göndermiyor. Olası servis tekrarlarının
ücret ve vaka sınırlarına etkisi canlı test öncesi netleştirilmeli.

## Bütçe aritmetiği — fiyat tahmini değil

Bir tamamlanmış vakanın tüm bileşenleriyle maliyeti `c` USD ise:

| Ölçüm | Planlanan vaka çalıştırması | Maliyet formülü | 100 USD'ye sığması için ortalama `c` |
| --- | ---: | ---: | ---: |
| İlk bağlantı denemesi | 1 | c | ≤100 USD |
| Geliştirme kümesi, tek tekrar | 7 | 7c | ≤14,28 USD |
| Tüm public vakalar, tek tekrar | 13 | 13c | ≤7,69 USD |
| Tüm public vakalar, üç tekrar | 39 | 39c | ≤2,56 USD |

Tablo `c` için bir tahmin vermez; ek üretim/test/başarısız tekrar maliyetlerini
kapsamadığında tam kampanya bütçesi sayılmaz. Yerel holdout ayrımı korunur;
tüm public vakalar geliştirme sırasında çalıştırılmaz. Depodaki mevcut
üç simülasyon kotası bir ilk-aşama güvenlik sınırıdır, bütün kampanya izni değildir.

## Karar ve sonraki ölçüm

İlk fiyat incelemesi sırasında kullanıcı yalnız analiz istemişti. Sonraki açık
talimatında GitHub incelemesi sonrası mevcut 100 USD krediyle test başlatmaya izin
verdi. `live_tests_enabled=false` toplu koşular için korunuyor; ayrı
`credit_pilot_authorized=true` ile tek geliştirme vakası ölçüldü. Bu yerel depo tedbiridir, organizatörün
her testten önce fiyat onayı istediği anlamına gelmez. Freya toplam 100 USD
yetkisi ve dış model harcaması yasağı değişmedi; satın alma yapılmadı.

Eksik bilgi: hackathon **chat simülasyonunda** telefon modeli, persona, judge ve
otomatik tekrarlar dahil ücret/kredi hesabı; bakiye bitince durma veya ek ücret
davranışı. Bu bilgiler organizatörden gelince doğrulanmış üst sınır kaydedilir.
Kullanıcının sonraki izniyle bir geliştirme vakası/tek tekrar için önce-sonra kredi
farkı ölçüldü. Bu gözlenen maliyettir; sonraki tüm vakalar için garanti üst sınır
olarak kullanılamaz.

İlk gerçek ölçüm için ortak operatör koordinasyonu, sabit banka takım anahtarı,
tek vaka `--only` seçimi, API sonucu ve kredi farkı birlikte kaydedilmeli. Başka
işler veya sonradan düşen ücretler varsa bakiye farkı tek çağrıya atfedilmemeli.

## İlk canlı ölçüm sonucu — 14:47–14:49 UTC

Kullanıcının açık test izni ve arkadaşının yeni testleri durdurma teyidiyle,
workspace'teki önceki iş bittikten sonra PUB-01 tek tekrar çalıştırıldı.
Resmî sonuç **1/1 PASS**, simülasyon 41 saniye, wrapper toplamı 79,953 saniye.
Kredi 199,7603 → 199,7204: gözlenen fark **0,01995 USD**. Son bakiye yaklaşık
**99,86 USD**. Önceden başka operatörün tüketimi bulunduğundan 100 USD'den
toplam düşüşün tamamı bizim testimize ait değildir.

Çağrı kaydındaki `cost` değeri 0,019933; genel API şeması birimini açıklamadığı
için bunu kesin USD faturası olarak kullanmadık. Workspace kullanım API'si
0,6113 toplam kullanılan kredi gösteriyor; toplam bakiye farkıyla aynı değil.
Bu nedenle `actual_cost_usd=null` ve gözlenen bakiye farkı ayrı tutuldu.
Bir kolay vakadaki maliyet tüm zor vakalar için azami fiyat değildir.
Rezerv henüz bırakılmadı; sınırsız/toplu test döngüsü açılmadı.
Kanıt: `reports/first-live-evaluation.json`; özel ham kanıt `runs/` altında.

## Sonraki geniş kampanya — güncel karar

Kullanıcının geniş test/düzeltme talimatı önceki tek-pilot sınırını genişletti.
İlk rezerv, tamamlanan uzak iş doğrulandıktan sonra kaydı korunarak kapatıldı.
`--monitored-credit`: toplam 100 USD Freya izni, en az 20 USD kalan kredi
tamponu, başlangıçta 20 simülasyon/84 vaka koşusu kotası ve her başlangıçta bakiye kontrolü.
Bu kullanıcı iznidir; vaka fiyatının doğrulandığı anlamına gelmez.

Son gözlenen bakiye 197,6711 kredi × 0,5 = **98,83555 USD**. İlk 100 USD'den
workspace toplam düşüşü 1,16445 USD; başka operatörün çağrıları da bulunduğundan
tamamı bu kampanyaya atfedilemez. Tur bazında gözlenen farklar
`reports/extended-evaluation.json` içindedir. `actual_cost_usd` hâlâ `null`.
Ek dış model API harcaması ve kredi satın alımı yapılmadı.

Son iki çağrıdan sonra banka test servisi HTTP 500 / Cloudflare 1101 verdi.
Yeni ücretli testler durduruldu; bu turun rezervi sonuç kurtarılana kadar tutulur.
Arkadaşın dalındaki 0,10 USD "verified" vaka fiyatı yalnız bakiyeye dayanıyor;
geçerli tarife kanıtı olmadığı için bu daldaki bütçeye alınmadı.

## 0.1.10 ve 0.1.11 canlı doğrulama kampanyası

Kullanıcının "canlı olarak uygula her şeyi test et" talimatıyla, bekleyen iki
çağrı salt okunur kurtarmayla 1/2 olarak puanlandı; eski rezerv kapatıldı.
Yeni başlangıç bakiyesi 197,4888 kredi × 0,5 = 98,7444 USD.
0.1.10'un 21 çağrılık üç tekrarı ve düzeltme adayının tüm 13 public vaka × 3
tekrarı için tarihsel koşular dahil 87 vaka koşusu gerekir. Bu nedenle yerel
vaka kotası 84'ten 96'ya çıkarıldı; 20 simülasyon, 100 USD toplam izin ve
20 USD tampon değişmedi. Aynı simülasyonda iki çağrı resmî istemcinin belgeli
özelliğidir; aynı anda birden çok simülasyon başlatma izni değildir.

0.1.10 ölçümü sırasında bakiye 100 USD'nin üstüne çıktı; bu oturum kredi satın
almadı ve artışın kaynağı doğrulanmadı. Bu aralıktaki negatif bakiye farkı
negatif test maliyeti değildir. Yeni sürüm, belgeli kullanım API'sindeki
`totalCreditsUsed` değerini de okur; eklenen kredi harcama yetkisini artırmaz.
100 USD izin içindeki 20 USD tampon korunarak, toplam gözlenen tüketim
80 USD'ye ulaştığında yeni test durur. Gözlenen tüketim geçmiş en yüksek
tüketimin, 100 USD eksi bakiyenin ve workspace toplam kullanılan kredi ×
kur değerinin en büyüğüdür; diğer operatörlerin kullanımı da ihtiyatlı biçimde
dahildir. Kullanım verisi yoksa/geçersizse veya sayaç gerilerse yeni test
engellenir. Bu kontrol sağlayıcı tarafında kesin ücret tavanı değildir;
gecikmeli faturalama belirsizliği sürer.

0.1.11 geliştirme turunda ayrıca yazıyla söylenen gün biçimi hatası yakalandı.
0.1.12 düzeltmesinin 13 public vaka × 3 ölçümüne yer bırakmak için yerel
kampanya kotası 26 simülasyon/120 vaka koşusu olarak sınırlandı (planlanan
tarihsel toplam 108 vaka koşusu). Bu, ek para izni değildir: 100 USD ve
20 USD tampon aynı kaldı; yeni kredi satın alınmadı, dış model kullanılmadı.

## 11 Ekim son public ölçüm

Kullanıcı son testleri yeniden yetkilendirdi. 0.1.11'in kesilen üç tekrarı
salt okunur kurtarıldı; bekleyen rezerv kapatıldı. Yeni kontrolde
493,9994 kredi × 0,5 = 246,9997 USD bakiye, toplam 9,1415 kredi kullanımı
görüldü. İzin hâlâ 100 USD'dir; büyük bakiye ek harcama yetkisi değildir.
Bu başlangıçtaki ihtiyatlı workspace tüketimi 4,57075 USD; kesin test faturası
değildir. 0.1.13 için 39 public çağrı planlandı; her simülasyonda bakiye ve
kümülatif kullanım kontrolü sürer. Sonraki gerçek değerler sonuç raporuna yazılır.

0.1.13'te kayıt bildirimi/ödeme kaydı belirsizliği görülünce 0.1.14 için bir
ek, sınırlı 39 çağrılık regresyon turu ayrıldı. Yerel kota 32 simülasyon/156
vaka koşusu; öngörülen tarihsel sayaç 147. 100 USD izin ve 20 USD tampon
genişlemedi. Yeni turlar tek simülasyon içinde en fazla üç çağrı kullanır.
