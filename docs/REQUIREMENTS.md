# Gereksinim kaydı — 10 Ekim 2026

Kaynaklar: [resmî etkinlik](https://events.ycombinator.com/AI-FDE-Build-the-Builder),
[Freya etkinlik sayfası](https://www.freyavoice.ai/hackathon),
[resmî v3 paket](https://www.freyavoice.ai/hackathon/build-the-builder-v3.zip).
İndirilen paketin SHA-256 değeri:
`655cbe581b0b0a7fba1f62ebd7d8c806edcfcc43f4d4fd47a27dca1e2534413a`.
Paketin README, freya.py ve docs dosyaları `starter-v3/build-the-builder/` altında değiştirilmeden tutulur.

## Doğrulanan sözleşme ve kurallar

| Konu | Gereksinim | Birincil kaynak |
|---|---|---|
| Girdi | Brief dosyaları + o brief'e ait banka OpenAPI dosyası. Finalde yedi araç adı sabit, alanlar/değerler değişebilir. | v3 README; site Data/Submit |
| Çıktı | Freya workflow + ilişkili agent; `freya.export_workflow` ile platformdan alınmış JSON ve o üretime ait iz. Yerel taslak export değildir. | v3 README; site Submit |
| Alan/dil | Sentetik borç tahsilatı, İngilizce, metin simülasyonları. Tarihler çağrıdaki `now` ile hesaplanır. | site Overview/Rules |
| Builder modeli | Herhangi bir model/kodlama agent'ı; builder model ücretini ekip öder. | site Limits; v3 README |
| Telefon modeli | `freya.py:AGENT_LLM` varsayılanı: provider ve model `experimental-5`. Katılımcı değiştiremez. | v3 freya.py, README |
| Simülatör | Paket `google/gemini-3-flash-preview` kullanır. | v3 freya.py |
| Süre | Brief başına, builder'ın kendi testleri dahil en fazla 30 dakika. | site Limits |
| Kaynak | Workspace başına 200 workflow; aynı slot güncellenmeli. Aynı anda tek simülasyon; takım başına tek Freya anahtarı. | site Limits/Rules |
| Dış araçlar | Telefon agent'ı yalnızca paketin banka API'sini çağırabilir; workflow içi kod ve hook kullanılabilir. | v3 README |
| Geliştirme | 13 public vaka: 10 A, 3 B. B, A'ya eklenir; bağımsız okunmaz. | v3 README |
| Final | İki görülmemiş brief, her biri 30 vaka; her vaka 3 tekrarın tamamında geçmeli. Skor 60 vaka üzerinden. | site Evaluation |
| Başarı | Banka kaydı + politika + doğruluk birlikte geçer. Kısmi puan yok; doğru ret de başarıdır. | site Evaluation; v3 README |
| Eşitlik | Başarılı vakalardaki vaat tutarı, daha kısa toplam üretim süresi, daha erken teslim. | site Evaluation |
| Gizli brief | 11 Ekim 2026 Pazar 17:00 UTC = İstanbul 20:00. Teslim 20:00 UTC öncesi = İstanbul 23:00 öncesi. | site Submit |
| Gizli brief sonrası | Parser çökmesi gibi genel hata düzeltilebilir; yeni brief'in kural/değer/adları kaynak kod veya prompta elle eklenemez. | site Rules/README |
| Teslim | Repo URL'si, kesin commit, çalıştırma komutu, iki workflow export'u, iki üretim izi; paket e-postasındaki adrese form. | site Submit |
| İz | Başlangıç/bitiş, model adı ve her çağrının kısa amacı, workflow/agent kimlikleri, adım/araç sayıları, yapılan test ve sonuç. Anahtar içermemeli. | site Submit |
| Yeniden üretim | İlk on ekibin belirtilen commit'i yeniden çalıştırılır; izler de incelenir. | site Submit |
| Katılım | Tek kişi veya iki kişilik ekip; gerçek müşteri verisi, platform probing/load test yasak. | site Rules |

10 Ekim kickoff e-postası ayrıca incelendi: [mail uygulama kaydı](kickoff-mail.md).
Maildeki Drive bağlantısı açılamadı; resmî web sayfasındaki v3 paketi yeniden
indirildi ve yukarıdaki hash ile eşleşti. Mail gizli brief/teslim saatlerini,
takım boyutunu, tek simülasyon kuralını ve üretim izi şartını doğruluyor; teslim
adımlarının ayrıca gönderileceğini söylüyor. Kayıt transkriptinde son platform
test limitlerinin daha sonra açıklanacağı belirtiliyor.

## API seçimi

Genel [Create agent](https://docs.freyavoice.ai/api-reference/agents/create-agent)
sayfası `app.freyavoice.ai/api/v2/agents` adresini belgeliyor. Ancak yarışma istemcisi,
workflow için `https://staging-app.freyavoice.ai/api/v2/workflow` kullanıyor.
Workflow oluşturma şeması genel sitede belgelenmiyor; v3 `docs/api.md` esas alındı.
Doğrulama `POST .../workflow?dryRun=true`; güncelleme sonrası yayınlama zorunlu.
Kit bazı eski açıklamaları “not confirmed” işaretliyor; uygulama yalnızca güncel
`freya.py` içindeki workflow çağrıları kullanılıyor. Miraç workspace'inde 10 Ekim
API dağıtımı, yayınlama ve resmî export geri okuması doğrulandı: baseline v4,
`deployed_verified`. Ek kredi sorguları genel API belgelerinden doğrulanan salt
okunur uç noktaları kullanır; bunlar workflow oluşturma şeması yerine geçmez.

## Kullanıcının doğruladıkları

- Toplam üst sınır **100 USD**; son kullanıcı talimatıyla yalnızca Freya platformu
  üzerinden harcanabilir. Ek OpenAI/ChatGPT veya başka dış model API harcaması yok.
- Güncel hedef **Mirac Birlik's Workspace**, ID `8783bb12-56fc-489a-8608-590676971f6c`.
  Kullanıcı Buildo hedefini bıraktı. Anahtarın yalnız bu workspace'e eriştiği API
  ile doğrulandı; kullanıcı bu oturumdaki asistanı tek test operatörü seçti.
- Güncel bakiye **100 USD**; API 200 kredi × 0,50 USD dönüşüm ve sorgu anında
  0 toplam kullanılan kredi gösteriyor. Önceki başka workspace'in 96,20 USD
  gözlemi artık hedef hesabın durumu değildir. [Fiyat analizi](cost-analysis.md).
- Anahtarlar sohbetten istenmez veya çıktılara yazılmaz.
- `sources/` salt okunur. İnceleme sırasında boştu; başlangıç kodu veya katılımcı belgesi yoktu.

## Açık bilgiler / varsayım yapılmayan konular

- Son teslim adımları/form adresi ve kickoff'ta sonradan açıklanacağı söylenen
  gizli brief dönemi platform test kotası. E-posta ve API erişimi artık incelendi.
- Freya simülasyon kredi tarifesi, gerçekten tahsis edilmiş ücretsiz kredi ve bir vaka için doğrulanmış azami maliyet.
- Builder token, RAM/CPU veya dış model istek kotası için ek katılımcı sınırı: kamu kaynaklarında ayrıca belirtilmiyor.
- Takım adı ve ikinci geliştiricinin private depo davetini kabul durumu.
  `mbirlik24` yazma erişimi GitHub API ile doğrulandı.
  Depo: https://github.com/Mehmetalimans/freya-builder .
- Miraç workflow'u API üzerinden v4 olarak yayınlandı. İlk geliştirme vakası
  PUB-01 1/1 geçti; tüm geliştirme/holdout/genelleme başarısı henüz ölçülmedi.

Güncel sitenin ayrıntılı Submit bölümü birden çok üretim çalıştırmasından birini
seçmeye açıkça izin veriyor; Overview/README'nin final özetinde “bir kez” deniyor.
Kickoff e-postası bu ayrıntıyı çözmüyor; tutarsızlık kaynaklarıyla kaydedildi.
Bu sürüm gizli brief üzerinde otomatik tekrar veya düzeltme döngüsü yapmaz.

## Yerel tasarım tercihleri (yarışma kuralı değildir)

- Dış bağımlılıksız, deterministik ilk baseline; builder model maliyeti sıfır.
- Politika metni eksiksiz aktarılır; başlık çıkarımı anlamsal analiz sayılmaz.
- İlk 7 A vakası geliştirme; kalan 3 A ve 3 B vaka ayrılmış kontrol seti.
  Kontrol setinin script/check içerikleri geliştirmede kullanılmadı. Bunlar
  organizatörün gizli final seti değil, bizim ayırdığımız public vakalardır.
- Toplu otomatik test varsayılan kapalıdır. Kullanıcının Freya bütçesiyle arayüzden
  tek vaka / tek tekrar / 180 saniye sınırında ilk bağlantı testi hazırlanmıştır.
  Arayüz persona ve analiz seçiminde yalnız Freya YC LLM gösterir; böyle bir koşu
  resmî kitin Google simülatör/judge koşusuna eşdeğer sayılmaz.
- Farklı banka sunucusu veya karmaşık/nested araç alanı gelirse açık hata verilir;
  belgesiz bir endpoint ya da şema dönüşümü tahmin edilmez.
