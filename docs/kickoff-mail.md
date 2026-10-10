# Kickoff e-postası: uygulama kaydı

Kaynak: kullanıcının 10 Ekim 2026'da sohbet içinde paylaştığı Freya ekip e-postası.
Bu bir organizatör belgesi olarak değerlendirilir; kullanıcı talimatlarının veya
depo güvenlik sınırlarının yerini almaz. Anahtar, parola ve kişisel e-posta
adresleri bu kayda alınmadı.

- Takım bir veya iki kişi olabilir. Workspace başına aynı anda bir practice
  simülasyonu çalışabilir. Kullanıcı bu ölçümlerin operatörü olarak bu çalışmayı seçti.
- Builder için herhangi bir kodlama aracı kullanılabilir; üretim izi teslimle
  birlikte istenir. Bu projenin builder'ı dış model API çağrısı yapmaz.
- Freya anahtarı workspace içindeki API Keys sayfasından üretilir; kit `env.sh`
  içinde `FREYA_API_KEY` bekler. Kendi wrapper'ımız aynı süreç ortamını okur,
  `env.sh` veya `.env` dosyalarını kendiliğinden yüklemez.
- Banka takım anahtarını takım kendisi seçer: en az 16 karakter, her denemede aynı
  değer. Bu Freya anahtarı değildir. `FREYA_BANK_TEAM_KEY` yerel ortamda tutulur.
  Önceki hazırlığın yerel anahtarı `state/browser-bank-team-key` içinde korunuyor;
  dosya Git dışında. İkinci bilgisayara sohbet veya repo üzerinden paylaşılmaz.
- Başlangıç workflow'u `Freya Bank Collections Base`; kitte karşılığı
  `examples/base-agent.json`. Bize ait baseline ayrı workflow'da tutulur.
- Gizli brief'ler **11 Ekim Pazar 17:00 UTC / 20:00 İstanbul**; kapanış
  **20:00 UTC / 23:00 İstanbul**. Ayrıntılı teslim adımları ayrıca gönderilecek.
  Bu e-postada teslim formu yok; mevcut sayfadaki form ifadesi tamamlanmış sayılmaz.

## Paket eşleştirmesi

E-postanın [Drive bağlantısı](https://drive.google.com/file/d/1237DMLa-a0xWAB1GfRcqBDsJ0S1XgDWr/view)
10 Ekim'de Chrome'da “file does not exist” sonucu verdi. Drive paketinin içeriğini
gördüğümüzü iddia etmiyoruz. [Resmî yarışma sayfasının](https://www.freyavoice.ai/hackathon)
hâlâ sunduğu [v3 ZIP](https://www.freyavoice.ai/hackathon/build-the-builder-v3.zip)
yeniden indirildi: 59.892 bayt, SHA-256
`655cbe581b0b0a7fba1f62ebd7d8c806edcfcc43f4d4fd47a27dca1e2534413a`.
Depodaki değişmemiş v3 arşiviyle birebir aynı. Bu nedenle v3 temel alındı.

## Gerçek API uygulaması

10 Ekim'de anahtarın yalnız Miraç workspace'ine bağlı olduğu sunucudan doğrulandı.
Builder 0.1.3 ile `practice-a` slotu mevcut baseline workflow'una bağlandı;
validate → update → publish → export → davranış karşılaştırması tamamlandı.
Workspace: `8783bb12-56fc-489a-8608-590676971f6c`.
Workflow: `82c69318-2c6a-43d3-9661-a93ea8b9b99d`, yayımlanan sürüm **4**.
Agent: `7e5da178-7701-4c97-a394-b4c93c4dc953`.
Yerel kanıt: `runs/20261010T143548Z-dcb3f232/`, durum `deployed_verified`.
Üretim 1,625 saniye; 3 düğüm, 7 araç; telefon modeli `experimental-5`.
Henüz resmî simülasyon, davranış başarı skoru veya final teslimi yok.
