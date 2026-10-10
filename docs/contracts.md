# Builder ↔ Freya entegrasyonu: sözleşme v1

Bu belge **mevcut kodun** ürettiği arayüzü tanımlar; planlanan düzeltme döngüsü
henüz uygulanmış sayılmaz. Ortak dosya değişiklikleri PR incelemesi gerektirir.

## Girdi ve saf üretim

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

## Dağıtım ve doğrulama

`--deploy` için süreç ortamında `FREYA_API_KEY` ve `FREYA_WORKSPACE_ID` gerekir.
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

Üretim tarafındaki gelecekteki otomatik düzeltme yalnız **geliştirme** geri
bildirimini okuyabilir; `holdout` veya gizli vaka değerleri kod/prompt kuralına
elle eklenemez. Düzeltme arayüzü için yeni alan gerekecekse önce bu sözleşme
güncellenip iki parçanın testleri aynı PR'de geçirilir.
