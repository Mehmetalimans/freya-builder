# Ekip arkadaşının AI aracına başlangıç metni

Freya Build the Builder v3 için private `Mehmetalimans/freya-builder` deposunda
çalışıyoruz. Ben Freya entegrasyonu, simülasyonlar ve sonuç kaydından sorumluyum;
diğer kişi görev analizi, agent üretimi ve otomatik düzeltmeyi geliştiriyor.
Önce `AGENTS.md`, `README.md`, `docs/hackathon-rules.md`,
`docs/contracts.md`, `docs/tasks.md` ve resmî `starter-v3/build-the-builder/`
paketini oku. Kendi `integration/first-live-run` dalını aç; ana dala doğrudan
push yapma. İlk görev: ücretsiz birim testlerini çalıştır, yeni takım
workspace'i olan [Mirac Birlik's Workspace](https://staging-app.freyavoice.ai/?workspaceId=8783bb12-56fc-489a-8608-590676971f6c) içinde resmî istemciyle validate/save/publish/export/readback yolunu
doğrula. UI'da yayımlanmış `Brief A - Builder Baseline` v3 zaten var; bunun
programatik doğrulama ve benchmark ölçümü olduğunu varsayma. Gerçek/eksik
sonuçları dürüstçe kaydet. Ücretli resmî simülasyondan
önce vaka başı azami Freya maliyetini ve ortak 100 USD sınırını teyit et; iki
bilgisayar arasında aynı anda test başlatma. Anahtarları sohbete, commit'e veya
loglara koyma. API/model/başarı uydurma. Değişiklikleri testli PR ile paylaş.
