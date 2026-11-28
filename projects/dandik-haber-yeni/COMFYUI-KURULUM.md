# ComfyUI kurulumu (Windows, RTX 5060 8 GB)

Bu metni, kendi bilgisayarında çalışan bir Claude Code oturumuna (Claude masaüstü uygulaması, yerel oturum,
`comfy` klasöründe) olduğu gibi yapıştır.

---

Benim için bu klasöre ComfyUI kur ve kısa AI video üretimine hazırla. Bilgisayar: Windows, NVIDIA RTX 5060 8 GB
(Blackwell, CUDA 12.8 ve üstünü isteyen bir kart). Amaç: Instagram Reels için 5 ile 10 saniyelik, 9:16, çizgi film
tarzı (Pixar benzeri 3D) karakter klipleri; ses ElevenLabs'ten ayrı gelecek.

Adımlar:

1. Önce kontrol et ve bana söyle: `nvidia-smi` (sürücü ve CUDA sürümü), boş disk alanı (en az 40 GB lazım),
   yüklü Python ve Git. Sürücü eskiyse güncellememi söyle, kendin kurma.
2. ComfyUI'nin resmi Windows portable sürümünü (NVIDIA, RTX 50 serisini destekleyen PyTorch cu128 ve üstü olan)
   resmi GitHub sürümlerinden indirip bu klasöre aç. Hangi paketi seçtiğini ve neden seçtiğini söyle.
3. ComfyUI-Manager'ı ve GGUF modelleri yükleyen `ComfyUI-GGUF` özel düğümünü kur.
4. 8 GB'a sığan modelleri indir, her birinin adını ve boyutunu indirmeden önce bana listele:
   - **Wan 2.2 TI2V 5B** (metinden ve görselden video), 8 GB'a sığan sıkıştırılmış (fp8 ya da GGUF Q4/Q5) sürümü,
     VAE'si ve metin kodlayıcısı (umt5, fp8 ya da GGUF).
   - Karakter görselleri için 8 GB'ta çalışan bir görsel modeli (SDXL tabanlı, örneğin Juggernaut XL, ya da
     Flux'ın GGUF sürümü).
   Dosya adlarını ve klasörlerini tahmin etme: ComfyUI'nin resmi dokümanındaki (docs.comfy.org) Wan 2.2 sayfasına
   ve modellerin Hugging Face sayfalarına bak.
5. ComfyUI'yi `--lowvram` ile başlat, resmi Wan 2.2 5B şablon iş akışını aç ve 9:16, 480p, 3 saniyelik bir deneme
   üret: "a chunky cartoon Istanbul seagull with grumpy eyebrows standing on a red simit cart, Pixar-like 3D".
   Ne kadar sürdüğünü ve VRAM kullanımını bana söyle.
6. Bitince bana şunları ver: ComfyUI'yi nasıl açacağım (tek komut ya da .bat), deneme videosunun yolu, kurulan
   modellerin listesi ve takıldığın her şey.

Kurallar: Sistem ayarlarını, sürücüyü ya da bu klasörün dışındaki bir şeyi değiştirmeden önce bana sor. Bir şey
çalışmazsa uydurma çözüm üretme, hatayı olduğu gibi göster.
