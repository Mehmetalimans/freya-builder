# Yarışma kuralları ve belirsizlikler

10 Ekim 2026 itibarıyla [resmî etkinlik](https://events.ycombinator.com/AI-FDE-Build-the-Builder),
[Freya yarışma sayfası](https://www.freyavoice.ai/hackathon) ve
[v3 katılımcı paketi](https://www.freyavoice.ai/hackathon/build-the-builder-v3.zip)
ile doğrulandı. Ayrıntılı kaynak eşlemesi [REQUIREMENTS.md](REQUIREMENTS.md)
dosyasındadır. Genel agent API dokümanı yarışma workflow API'si için kaynak
sayılmaz; bu repoda v3 kitinin istemcisi kullanılır.

| Konu | Doğrulanmış koşul |
| --- | --- |
| Girdi | Görev brief'i/brief'leri ve o görevin banka OpenAPI belgesi. B, A'nın üzerine eklenir. Yedi araç adı sabit; şemaları değişebilir. |
| Çıktı | Freya workflow + agent; resmî istemciyle alınmış iki platform export'u ve üretim izleri. Yerel JSON tek başına teslim export'u değildir. |
| Alan | Sentetik İngilizce borç tahsilatı. Çağrıdaki `now` kullanılır; gerçek müşteri verisi yasak. |
| Modeller | Builder istediği yöntemi kullanabilir ve maliyetini ekip öder. Telefon agent'ı provider/model `experimental-5`; resmî test simülatörü/judge `google/gemini-3-flash-preview`. |
| Limitler | Brief başına iç testler dahil 30 dakika; workspace başına 200 workflow, tek eşzamanlı simülasyon; takım başına tek Freya API anahtarı. |
| Değerlendirme | 10 A + 3 B public vaka; finalde iki görülmemiş brief, her biri 30 vaka ve üç tekrar. Bir vaka tüm tekrarlarda politika, doğruluk ve banka kaydını geçmeli. |
| Teslim | Repo URL'si, kesin commit, çalıştırma komutu, iki platform export'u ve ilgili iki iz. Gizli brief'ler 11 Ekim 17:00 UTC / 20:00 İstanbul; teslim 20:00 UTC / 23:00 İstanbul öncesi. |

## Henüz doğrulanmayan veya çelişen noktalar

- Katılımcı e-postası incelendi: [kaynak ve uygulama kaydı](kickoff-mail.md).
  Miraç workspace'inin API erişimi ve dağıtımı doğrulandı; teslim formu/adımları
  e-postada henüz yok, organizatör ayrıca gönderecek.
- Bir vakanın azami Freya maliyeti, kredi kapsamı, ek CPU/RAM/token kotaları
  ve GitHub private depo erişimi organizatör kaynağıyla henüz doğrulanmadı.
- 10 Ekim'de güncel sayfanın ayrıntılı Submit bölümü birden çok üretimden birini
  seçmeye açıkça izin veriyor. Overview/v3 README'deki “bir kez” ifadesiyle fark
  sürüyor; kickoff e-postası bu ayrıntıyı ele almıyor. Her seçilen üretimin kendi
  izi ve 30 dakika sınırı korunmalı; belirsizlik organizatöre sorulabilir.
- Başka takımın test workspace'inde tarayıcıyla yayınlanan A workflow'u resmî
  otomatik dağıtım veya benchmark başarısı sayılmaz.

## Kullanıcının kararı; yarışma kuralı değil

- Toplam harcama en çok 100 USD ve yalnız Freya platformunda; ek dış model API
  harcaması yok. Bu sınır iki geliştirici için tek ortak toplamdır.
- Bakiye 100 USD olarak API ve arayüzle doğrulandı; bu simülasyon fiyatı değildir.
  Fiyat kanıtı ve belirsizlikler [maliyet kaydında](cost-analysis.md).
- İlk 7 A vakası geliştirme, kalan 3 A + 3 B public vaka yerel holdout'tur.
  Bu ayrım resmî gizli final seti değildir.
