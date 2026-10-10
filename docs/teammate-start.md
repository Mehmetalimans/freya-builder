# Ekip arkadaşının AI aracına başlangıç metni

Freya Build the Builder v3 için private `Mehmetalimans/freya-builder` deposunda
çalışıyoruz. Ben Freya entegrasyonu, simülasyonlar ve sonuç kaydından sorumluyum;
diğer kişi görev analizi, agent üretimi ve otomatik düzeltmeyi geliştiriyor.
Önce `AGENTS.md`, `README.md`, `docs/hackathon-rules.md`,
`docs/contracts.md`, `docs/tasks.md` ve resmî `starter-v3/build-the-builder/`
paketini oku. Kendi `integration/first-live-run` dalını aç; ana dala doğrudan
push yapma. API dağıtımı artık [Mirac Birlik's Workspace](https://staging-app.freyavoice.ai/?workspaceId=8783bb12-56fc-489a-8608-590676971f6c)
içinde doğrulandı: `Brief A - Builder Baseline` v4; workflow
`82c69318-2c6a-43d3-9661-a93ea8b9b99d`. İlk geliştirme testi PUB-01 1/1 geçti;
genel benchmark/holdout ölçülmedi. Eklediğin belgeler `docs/reference-index.md`
ile değerlendirildi; çalışma koduyla birlikte inceleme dalında korunuyor.
İlk görev: birim testlerini çalıştır, `docs/cost-analysis.md` ve
`docs/kickoff-mail.md` kayıtlarını oku; simülasyon fiyat bilgisini doğrula.
Kullanıcı şimdilik diğer bilgisayardaki asistanı tek test operatörü seçti;
eşzamanlı deneme başlatma. Gerçek/eksik sonuçları dürüstçe kaydet. Ücretli resmî simülasyondan
önce vaka başı azami Freya maliyetini ve ortak 100 USD sınırını teyit et; iki
bilgisayar arasında aynı anda test başlatma. Anahtarları sohbete, commit'e veya
loglara koyma. Banka takım anahtarı Freya anahtarından ayrı, en az 16 karakterlik
sabit takım sırrıdır; her bilgisayar aynı değeri yerel ortamda kullanmalı.
API/model/başarı uydurma. Değişiklikleri testli PR ile paylaş.
