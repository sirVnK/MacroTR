export function AboutPage() {
  return (
    <div className="space-y-6">
      <section>
        <p className="muted-label">Açık kaynak</p>
        <h1 className="mt-1 text-3xl font-bold text-ink">MacroTR hakkında</h1>
      </section>

      <section className="panel max-w-4xl space-y-4 p-5 text-sm leading-7 text-slate-700">
        <p>
          MacroTR, Türkiye makro ekonomik verilerini TCMB EVDS odağında sade,
          hızlı ve geliştirici dostu bir dashboard üzerinde sunan açık kaynak bir projedir.
        </p>
        <p>
          Proje eğitim, veri görselleştirme, ekonomik okuryazarlık, açık kaynak katkı
          ve portföy amacıyla geliştirilir.
        </p>
        <p>
          Ekonomi ve veri meraklıları, öğrenciler, geliştiriciler ve açık kaynak
          contributorları tarafından kullanılabilir.
        </p>
        <p className="rounded-lg border border-amber/30 bg-amber/10 p-4">
          MacroTR yalnızca eğitim ve bilgilendirme amacıyla geliştirilmiştir.
          Yatırım tavsiyesi, alım-satım önerisi veya finansal danışmanlık hizmeti sunmaz.
          Veriler halka açık veya üçüncü taraf kaynaklardan alınır ve doğruluğu garanti edilmez.
        </p>
      </section>
    </div>
  );
}

