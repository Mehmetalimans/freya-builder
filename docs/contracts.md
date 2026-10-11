# Final klasör sözleşmesi (0.2.0)

`python builder/build.py CASE_FOLDER MOCK_URL` belge envanteri → kaynaklı gereksinimler → otomatik workflow üretimi → doğrulama → Freya yayın/export/geri okuma yapar. Ön koşul aynı vaka hash'i için başarılı uzaktan mock sözleşme kontrolüdür. Bankaya özgü fixture verileri `bank-mock/` içindedir; genel builder bunları sabit cevap olarak kullanmaz.

Girdiler: değiştirilmeyen belgeler, HTTPS mock adresi, yerel ortamda Freya yetkisi. Çıktılar: `input-manifest.json`, `builder-source-hashes.json`, `analysis.json`, `workflow.local.json`, `workflow.export.json`, `codex.session.jsonl`, `codex.events.jsonl`, `trace.jsonl`, `result.json`. Yayınlanmış başarı yalnız `deployed_verified`; üretim-only `offline_validated`.

`unresolved_conflicts` üretimi engeller. Belgelenmiş güvenli geri dönüşle ele alınabilen eksik yetenekler `limitations` içinde açıkça belirtilir. Tarih ve müşteri kimliği çağrı girdisinden, hesap bilgisi yalnız servisten gelir. Tek seferlik değişikliklerde kör tekrar yasaktır.

## Tarihsel brief/OpenAPI sözleşmesi

# Builder ↔ Freya entegrasyonu: sözleşme v1

Bu belge **mevcut kodun** ürettiği arayüzü tanımlar; planlanan düzeltme döngüsü
henüz uygulanmış sayılmaz. Ortak dosya değişiklikleri PR incelemesi gerektirir.

0.1.10 entegrasyon düzeltmesi: post-process hook'ları yalnız gerçek boolean
başarı/doğrulama alanlarını yorumlar, banka verisini değiştirmeden açıklama ekler.
Hook soru sırası, deneme sayısı, SMS vaadi, kapanış enum'u veya yeni retry bütçesi
belirlemez; bu kararlar verilen politikadadır. Desteklenmeyen null şema kısıtları
sessizce silinmez, açık hata verir. Bağlantı kurulmadan önceki hatalar için belgeli
`connect_retries=2`, tool-level HTTP tekrarı için `maxRetries=0` kullanılır.
0.1.10 canlı yayın/geri okuması doğrulandı. Yedi geliştirme vakasının üç
tekrarında 19/21 çağrı geçti; tüm tekrarları geçme hesabıyla 6/7 vaka başarılı.

Sonraki 0.1.11 adayı, tarih çıkarımına `payment_offer_quote` ekler. Hesaplama
node'u bu ifadenin açık bir gün içermesini arar ve kullanımdan sonra temizler;
eksik/belirsiz ifadede tarih uydurmak yerine netleştirme ister. Bu, İngilizce
gün ifadeleri için sınırlı bir kontroldür; alıntının ve ISO tarihin çıkarımı
hâlâ modele bağlıdır. Desteklenmeyen ifadeler ek netleştirme gerektirebilir.
0.1.12 bu denetime yazıyla söylenen 1–31 gün biçimlerini de ekler.

## Girdi ve saf üretim

Konuşma dili İngilizce, resmî test taşıması metindir (`mode=chat`).
`compile_workflow` genel talimatında İngilizce konuşmayı belirtir; bu,
Freya yönetim arayüzünün dilinden bağımsızdır. TTS/STT yapılandırması mevcut
metin benchmark sözleşmesinin parçası değildir; sesli başarı ayrıca ölçülür.

`builder.core.compile_workflow(briefs, document)` alır:

- `briefs`: sıralı `(dosya_adı, UTF-8 metin)` çiftleri; A+B halinde A önce.
- `document`: görev için verilen OpenAPI JSON nesnesi. Derleyici desteklenmeyen
  host, araç veya şemada `ContractError` verir; rota tahmin etmez.

Fonksiyon ağ isteği yapmaz ve `(workflow, analysis)` döndürür. `workflow` Freya
kitinin workflow gövdesidir; `analysis` karar/sınır açıklamasıdır. Aynı girdi
aynı kanonik workflow baytlarını üretir. `workflow_sha256 = SHA256(canonical(workflow))`;
`canonical` sıralı anahtarlı, boşluksuz UTF-8 JSON'dur.

CLI: `python builder/build.py BRIEF OPENAPI [--extra-brief BRIEF] [--slot stable]`.
Varsayılanı çevrimdışı; `--deploy` entegrasyon katmanını açar. Her koşu
`runs/<run_id>/` altında `workflow.local.json`, `analysis.json`, `trace.jsonl`
ve `result.json` yazar. `workflow.local.json` platform export'u değildir.

`builder/calendar.py`, brief'teki açık "Monday to Friday ... holidays: ISO tarihleri"
tanımını tanıdığında `calendar_setup` kod düğümü üretir. Tatiller girdiden gelir;
çağrıdaki `now` üzerinden bugünden sonraki iş günlerini ve bu/gelecek haftayı
hesaplar. Müşteri veya test cevabı gömülmez. Tanınmayan tanımda takvim varsayılmaz,
`analysis.calendar` bunu belirtir ve tam politika metni korunur. Ufuk 90 gündür;
bu özellik genel bir doğal dil politika derleyicisi değildir. Üretilen kod ve
geçişler de platform geri okuma kontrolüne dahildir.
Tanınan `days_late` / N'inci iş günü bant tablosu varsa, konuşmadan çıkarılan
ödeme tarihi `date_offer` kod düğümünde ürün bazında karşılaştırılır. Ham banka
sonucu değiştirilmez. Ayrı `date_reply` adımı hesaplanan seçenekleri açıklar;
konuşmadan tarih çıkarımı hâlâ model davranışıdır ve canlı ölçüm gerektirir.

## Dağıtım ve doğrulama

`--deploy` için süreç ortamında `FREYA_API_KEY` ve `FREYA_WORKSPACE_ID` gerekir.
İstemci önce `GET /api/v2/workspaces` ile anahtarın tek ve doğru workspace'e
bağlı olduğunu doğrular; belirsiz eşleşmede yazma yapılmaz.
`builder.build.deploy_workflow` resmî v3 istemcisiyle validate → aynı `slot`ta
save/update → publish → export → readback kontrolü yapar. Başarıda
`workflow.export.json` ile `result.json` içine `workspace_id`, `workflow_id`,
`agent_id`, `platform_version` yazılır. Sadece `status=deployed_verified`
resmî test girdisi olabilir. Hatalı/yarım yazma otomatik tekrar edilmez.

`result.json` ortak alanları: `builder_version`, `run_id`, `started_at`,
`ended_at`, `seconds`, `status`, `mode`, `workflow_sha256`, `nodes`, `tools`,
`builder_model_calls`, `builder_model_cost_usd`, `platform_cost_usd`,
`benchmark_success`, `tests`. `status` çevrimdışında `offline_validated`,
dağıtımda `deployed_verified`, hata halinde `failed` olur. `benchmark_success`
yalnız doğrulanmış resmî test tamamlanınca sayı olur; aksi halde `null`.
Canlı platform gerçek ücreti kanıtlanmıyorsa `platform_cost_usd=null` kalır.
İz, `event`, `at_utc`, `elapsed_seconds` içerir; anahtar ve ham sunucu yanıtı yoktur.

## Test geri bildirimi

`python builder/evaluate.py RUN_DIR --brief A|B --split dev|holdout --reps 1|3`
yalnız aynı workspace'te doğrulanmış dağıtımı ve yerel bütçe politikasını kabul
eder. `FREYA_BANK_TEAM_KEY` de yerel ortamda gereklidir. Çıktı
`evaluation.json` içinde `status`, `brief`, `split`, `reps`, `seconds`,
`workspace_id`, `case_ids`, `reserved_upper_bound_usd`, `actual_cost_usd`,
`benchmark_success` ve ölçüm tamamlanırsa `passed`, `total`, `results` olur.
`status=measured` dışındaki kayıtlar başarı değildir. Timeout uzaktaki işin
bitmesini kanıtlamaz; rezerv iade edilmez. Ham scorer/log/telemetry
`runs/` altında yerel kalır.

İsteğe bağlı `--only ID[,ID]`, seçilen brief/split içinden bir altküme seçer.
Tek vakalık ilk ölçüm böyle yapılır. Boş, tekrar eden veya split dışı kimlikler
bütçe ayırmadan reddedilir. Wrapper ve resmî scorer aynı kimlik listesini kullanır.

`--credit-pilot` yalnız açık kullanıcı izni (`credit_pilot_authorized`) ile bir
geliştirme vakası/tek tekrar kabul eder. Kalan bütçenin tümü yerel olarak ayrılır;
`authorization_reserved_usd` izin rezervidir, fiyat tavanı değildir.
`reserved_upper_bound_usd=null` kalır. `credits_before`, `credits_after` ve
`observed_balance_delta_usd` anlık faturalama kanıtıdır; gecikmeli/başka işlerin
ücretlerinden dolayı `actual_cost_usd` bunlarla otomatik doldurulmaz.
Rezerv ikinci denemeyi engeller ve otomatik serbest bırakılmaz.

10 Ekim'deki geniş test izni için `--monitored-credit` eklendi. Her simülasyon
öncesinde kredi kontrol edilir; bakiye 20 USD veya altındaysa yeni test başlamaz.
Kümülatif workspace tüketimi de okunur; eklenen kredi izin sınırını büyütmez.
Gözlenen toplam tüketim 80 USD'ye ulaştığında yeni test engellenir.
Geçersiz/eksik kullanım verisi ve gerileyen sayaç yeniden uzlaştırma gerektirir.
Bir simülasyonda en fazla yedi vaka, kampanyada `budget.json` kotaları uygulanır.
Bu tampon hizmet sağlayıcının fiyat garantisi değildir. Yarım kalan koşunun
`monitored_pending_run` rezervi uzaktaki durum incelenene kadar yeni testi engeller.
Tamamlanan ve scorer çıktısı doğrulanan koşu rezervi kapatır; başarısız vakalar da
geçerli ölçüm olabilir. `actual_cost_usd` fatura olmadığı sürece `null` kalır.
Tekrarların her birinin simülasyon kimliği `simulation-history.json` içinde korunur.
Belgelenmiş eşzamanlı simülasyon reddi, resmî istemcinin sınırlı süre içinde
beklemesine aktarılır; belirsiz ağ hataları veya diğer HTTP hataları tekrarlanmaz.

Her simülasyon isteği belgeli `maxRetries=0` kullanır. Eski koşular tek çağrıyla
yürütüldü; 0.1.11 kampanyası `simulation_max_concurrent_calls=2` ile aynı
simülasyonda iki çağrıya izin verir. Workspace'te tek simülasyon kontrolü sürer;
kitin modeli, persona metni, scorer'ı ve 420 saniye çağrı sınırı korunur. Başlatma
yanıtı hemen `remote-simulation.json` dosyasına kaydedilir; tamamlanmamış uzak
işin sonucu benchmark olarak yayımlanmaz. Yeni işten önce sunucu çalışan
simülasyon kontrolü yapılır; yarış durumunda sunucunun tek simülasyon kuralı da geçerlidir.

`builder/recover.py RUN_DIR`, tamamlanmış fakat puanlanamamış tek tekrarlı
bir simülasyonu veya `evaluation.user-paused.json` kaydı bulunan, tam üç
uzak simülasyonu tamamlanmış A geliştirme koşusunu yeniden okumak içindir.
Üç tekrar yolu başka brief/split için genel kurtarma desteği iddia etmez.
Eski persona/çağrı/banka oturumlarını
eşleştirir, aynı resmî `run_once` ve scorer ile bankanın mevcut ledger'ını okur.
Freya ve banka yazma istekleri engellenir. Orijinal `evaluation.json` korunur;
doğrulanan sonuç `evaluation.recovered.json` olur. Banka hâlâ bozuksa rezerv
kapanmaz. Kurtarma süresi yeni bir simülasyon süresi olarak raporlanmaz.

Üretim tarafındaki gelecekteki otomatik düzeltme yalnız **geliştirme** geri
bildirimini okuyabilir; `holdout` veya gizli vaka değerleri kod/prompt kuralına
elle eklenemez. Düzeltme arayüzü için yeni alan gerekecekse önce bu sözleşme
güncellenip iki parçanın testleri aynı PR'de geçirilir.

Ekip raporuna göre B public vakaları kullanılmıştır. `--split holdout` dosya
seçimi tarihsel ayrımı korur; ekip genelinde veri bağımsızlığını garanti etmez.
B tekrarları regresyon olarak raporlanmalı; genelleme için kullanılmamış veri
geçmişi ayrıca doğrulanmalıdır.

0.1.15 kimlik sözleşmesi: doğrulama endpoint'i all_verified veya identity_complete
alanını boolean olarak bildirmelidir. Yerel sayaç banka doğrulaması yerine
geçmez; tamamlanma alanı olmayan şema fail closed reddedilir. C/D/E sentetik
şemaları yalnız derleme uyumluluğu içindir; resmî API özellikleri sayılmaz.
