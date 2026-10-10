# Ekip arkadaşının AI aracına başlangıç metni

Freya Build the Builder v3 için private `Mehmetalimans/freya-builder` deposunda
çalışıyoruz. Ben Freya entegrasyonu, simülasyonlar ve sonuç kaydından sorumluyum;
diğer kişi görev analizi, agent üretimi ve otomatik düzeltmeyi geliştiriyor.
Önce `AGENTS.md`, `README.md`, `docs/hackathon-rules.md`,
`docs/contracts.md`, `docs/tasks.md` ve resmî `starter-v3/build-the-builder/`
paketini oku. Güncel aday `builder/extended-evaluation` dalında; kendi görev dalını
bunun üzerinden aç, ana dala doğrudan
push yapma. API dağıtımı artık [Mirac Birlik's Workspace](https://staging-app.freyavoice.ai/?workspaceId=8783bb12-56fc-489a-8608-590676971f6c)
içinde doğrulandı; workflow `82c69318-2c6a-43d3-9661-a93ea8b9b99d`.
Geniş turda önce 4/7, 0.1.6 ile 6/7 ölçüldü. 0.1.9 adayında son iki çağrının
birleşik puanı banka test servisinin HTTP 500/1101 hatası yüzünden alınamadı;
holdout ve üç tekrar tamamlanmadı. İlk görev: birim testlerini çalıştır,
`docs/extended-test-notes.md` ve `docs/teammate-code-review.md` bulgularını incele.
Kendi `feat/agent-core-optimization` dalındaki 0,10 USD fiyat varsayımını, sabit
tarih örneklerini ve erken kapanış hook'larını geri getirmeden değişiklikleri birleştir.
Kullanıcı şimdilik diğer bilgisayardaki asistanı tek test operatörü seçti;
eşzamanlı deneme başlatma. Servis düzelince `builder/recover.py` mevcut çağrıları
yeni ücretli simülasyon açmadan kurtarabilir. Geniş test izni verilmiştir; yeni
fiyat onayı isteme, ortak 100 USD sınırı ve 20 USD tamponu uygula. İki bilgisayar
arasında aynı anda test başlatma. Anahtarları sohbete, commit'e veya
loglara koyma. Banka takım anahtarı Freya anahtarından ayrı, en az 16 karakterlik
sabit takım sırrıdır; her bilgisayar aynı değeri yerel ortamda kullanmalı.
API/model/başarı uydurma. Değişiklikleri testli PR ile paylaş.
