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
