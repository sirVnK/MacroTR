export function DataSourcesPage() {
  return (
    <div className="space-y-6">
      <section>
        <p className="muted-label">Veri kaynakları</p>
        <h1 className="mt-1 text-3xl font-bold text-ink">TCMB EVDS</h1>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="panel p-5">
          <h2 className="text-lg font-semibold text-ink">Kaynak</h2>
          <p className="mt-3 text-sm leading-7 text-slate-700">
            MVP sürümünde veri kaynağı TCMB EVDS olarak sınırlandırılmıştır. Backend,
            `EVDS_API_KEY` tanımlandığında EVDS web servisine bağlanır; anahtar yoksa
            yerel geliştirme için demo seed verisi kullanır.
          </p>
        </div>
        <div className="panel p-5">
          <h2 className="text-lg font-semibold text-ink">Güncelleme mantığı</h2>
          <p className="mt-3 text-sm leading-7 text-slate-700">
            Local/dev ortamında `/api/v1/admin/fetch-data` endpointi seri verilerini
            güncelleyebilir. Production ortamında bu endpoint kapalıdır.
          </p>
        </div>
        <div className="panel p-5 lg:col-span-2">
          <h2 className="text-lg font-semibold text-ink">API key özeti</h2>
          <p className="mt-3 text-sm leading-7 text-slate-700">
            Gerçek veri için `.env` dosyasına `EVDS_API_KEY` ekleyin ve servisleri
            yeniden başlatın. Ticari kullanım veya yeniden dağıtım öncesinde veri
            sağlayıcı koşullarını ayrıca kontrol edin.
          </p>
        </div>
      </section>

      <section className="rounded-lg border border-amber/30 bg-amber/10 p-4 text-sm leading-6 text-slate-700">
        MacroTR yalnızca eğitim ve bilgilendirme amacıyla geliştirilmiştir.
        Yatırım tavsiyesi, alım-satım önerisi veya finansal danışmanlık hizmeti sunmaz.
        Veriler halka açık veya üçüncü taraf kaynaklardan alınır ve doğruluğu garanti edilmez.
      </section>
    </div>
  );
}

