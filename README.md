# Freya builder 0.1.1 — ilk baseline

Resmî Build the Builder **v3** paketi üzerine kurulu, bağımlılıksız Python builder.
Bu bir **yerel olarak doğrulanmış başlangıç sürümüdür**. Freya hesabında henüz
çalıştırılmadı; ölçülmüş yarışma skoru ve final teslime hazır olma iddiası yoktur.

## Hızlı çalıştırma

Doğrulanan ortam: **CPython 3.12.14**. Dış Python paketi gerektirmez.
Klasörün kökünde, Python komutunuz `python` ise:

```console
python -m unittest discover -s tests -v
python builder/build.py starter-v3/build-the-builder/briefs/brief-a.md starter-v3/build-the-builder/tools/openapi.json --slot practice-a
python builder/build.py starter-v3/build-the-builder/briefs/brief-a.md starter-v3/build-the-builder/tools/openapi.json --extra-brief starter-v3/build-the-builder/briefs/brief-b.md --slot practice-b
```

Varsayılan çalışma çevrimdışıdır ve sıfır API isteği yapar. `runs/<run-id>/` altında:

- `workflow.local.json`: üretilen yerel workflow taslağı; platform export'u değildir.
- `analysis.json`: kaynak özetleri, hash'ler, araç sözleşmesi ve sınırlamalar.
- `trace.jsonl`: başlangıç/bitiş, kararlar, doğrulama ve model/test kaydı.
- `result.json`: durum, süre, maliyet ve ölçülmüşse başarı. Ölçülmeyen alanlar `null` olur.

## Hesap erişimi geldikten sonra

`FREYA_API_KEY`, `FREYA_WORKSPACE_ID` ve en az 16 karakterlik sabit
`FREYA_BANK_TEAM_KEY` değerlerini yalnızca çalıştırılacak sürecin yerel ortamına
ayarlayın. Anahtarları komut satırı argümanlarına, sohbete veya repoya koymayın.
Builder `.env` dosyasını otomatik okumaz. Hesap seçimi açık workspace ID gerektirir.
Anahtarları ekrana yazdıran komutlar kullanılmamalıdır.
Üretim kaydı workspace ID'sini saklar; farklı workspace kimliğiyle değerlendirme
bütçe ayırmadan durur. Workspace bilgisi olmayan eski üretim kayıtları da reddedilir.
Bu yerel eşleşme kontrolü, API anahtarının sunucudaki yetkisini doğrulamanın yerine geçmez.

```console
python builder/build.py starter-v3/build-the-builder/briefs/brief-a.md starter-v3/build-the-builder/tools/openapi.json --slot practice-a --deploy
```

Bu işlem resmî istemciyle sunucu doğrulaması, aynı slotta oluşturma/güncelleme,
yayınlama, geri okuma ve `workflow.export.json` oluşturma yapar. İlk oluşturma
sonrasında da yarışma modelini ayarlayıp yayınlar. API hatalarında ham yanıt veya
anahtar kaydedilmez; başarılı olup olmadığı belirsiz yazma işlemi otomatik tekrarlanmaz.
Beklenmeyen platform normalizasyonu geri okuma kontrolünü durdurabilir; bu
kontrolün gerçek Freya yanıtıyla sınanması henüz bekliyor.

## İzinli değerlendirme ve bütçe

Kullanıcının toplam bütçesi **100 USD**. `budget.json` bu sınırı kaydeder.
Freya tarifesi/kredisi doğrulanmadan `live_tests_enabled` açılmaz. Önce bir vaka
çalıştırmasının **doğrulanmış en yüksek USD maliyeti** ve dayanağı kaydedilmelidir;
bu tahmin veya ortalama ücret değildir. Ücretsiz kredi ise kapsamı teyit edilmeli.
Mevcut builder dış modele çağrı yapmaz. Sonradan kullanılan dış model maliyeti
`state/budget-ledger.json` içindeki `other_spend_usd` hesabına da dahil edilmelidir.
Yerel rezerv defteri servis tarafında bir harcama kilidi değildir; güvenilir fiyat
üst sınırı olmadan 100 USD'yi garanti edemez, bu yüzden çalışmayı reddeder.

Hesap ve fiyat doğrulandıktan sonra tek komutla üretim ve geliştirme testi:

```console
python builder/build.py starter-v3/build-the-builder/briefs/brief-a.md starter-v3/build-the-builder/tools/openapi.json --slot practice-a --deploy --test-brief A --split dev --reps 1
```

Bu yol, üretim ve testin toplamına 30 dakika uygular. Resmî scorer değiştirilmeden
bir çalışma kopyasında çalıştırılır. Her tekrar ayrı simülasyondur; yerel kilit
aynı workspace'te üst üste çalışmayı engeller. Başka bilgisayardaki işi kilitlemez;
platformun tek simülasyon kuralı ayrıca geçerlidir.

Mevcut doğrulanmış üretimin ayrı değerlendirmesi:

```console
python builder/evaluate.py runs/RUN_ID --brief A --split dev --reps 1
```

Geliştirme skoru: ilk 7 A vakası. Kod sabitlendikten sonra `--split holdout` ile
kalan 3 A, A+B'den üretilen workflow için kalan 3 B ayrı ölçülür. `--reps 3`, her
vakanın üç çalıştırmanın tamamında geçmesini gerektirir. `--style` public
konuşma varyasyonlarını destekler. Bu public ayrım gerçek gizli benchmark değildir.

`evaluation.json` sonucu; `evaluation.log` resmî çıktı; `evaluation.telemetry.json`
gözlemlenebilen araç sonuçlarını saklar. Harcanan gerçek tutar servis kanıtı yoksa
`null`, ayrılan üst sınır ayrı alandadır. Zaman aşımı başarısız/incomplete sayılır;
uzaktaki simülasyonun iptal edildiği iddia edilmez. Rezerv otomatik iade edilmez.
Tekrar denemeden önce uzaktaki işi ve defteri kontrol edin. Otomatik davranışsal
düzeltme döngüsü ilk gerçek başarısızlıklar ve kalan bütçe görülene kadar eklenmedi.

## Sınırlar ve sıradaki işler

Baseline tüm brief'i telefon modeline verir ve API alan/enum'larını girdiden üretir.
Kimlik yanıtında belgeli `all_verified` varsa deterministik araç kapısı kurar;
yoksa bu kısıtın diyalog modeline bırakıldığını açıkça kaydeder. Kimlik, hesap ve
kapanış adımları vardır. İş günü/istisna hesabı hâlâ telefon modeline bağlıdır.
Gizli brief'e ait sayı, tatil, banka adı, sonuç kodu veya kimlik sorusu kodda sabit değildir.
Sadece skaler POST JSON gövdeleri desteklenir; desteklenmeyen şema açık hata verir.

Hesap geldiğinde: doğrulama/yayınlama kontrolü → 7 geliştirme vakası ilk ölçüm →
gerekirse genel politika derleyici/tarih kodu iyileştirmesi → sabit sürümün ayrılan
6 public vakada tekrarlı ölçümü → final commit ve iki export/iz dosyası.
Gerçek skoru görmeden bu baseline'ın güçlü olduğu varsayılmamalıdır.

## Tekrar üretim ve teslim

```console
python scripts/release.py
```

Sürüm arşivi ve her dosyanın SHA-256 manifesti `dist/` içine yazılır. Arşivde
çalışma sırları, hesap durumu, gerçek çalıştırma kayıtları ve sanal ortam yoktur.
Bu arşivi temiz bir klasörde açıp:

```console
python -m venv --without-pip .venv
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe builder/build.py starter-v3/build-the-builder/briefs/brief-a.md starter-v3/build-the-builder/tools/openapi.json
```

Linux/macOS'ta sanal ortam Python yolu `.venv/bin/python` olur. Bu platformlar
henüz denenmedi; Windows temiz sanal ortam kontrolü raporda belirtilir.

Finalde dosya hash'i tek başına yeterli değildir: organizatör GitHub repo URL'si
ve kesin commit ister. Gizli brief'lerden otomatik üretilmiş **iki platform export'u**
ve bunlara bağlı **iki iz** aynı commit'te yer almalıdır. `submission.template.json`
yalnızca eksik alanları gösteren taslaktır; gönderilmemiştir.
Kurallar, doğrulanmamış bilgiler ve İstanbul saatleri: [gereksinim kaydı](docs/REQUIREMENTS.md).
