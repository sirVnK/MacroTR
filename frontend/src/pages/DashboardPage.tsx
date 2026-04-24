import { AlertCircle, RefreshCw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { IndicatorCard } from "../components/IndicatorCard";
import { MacroChart } from "../components/MacroChart";
import { SeriesSelector } from "../components/SeriesSelector";
import { formatDate, formatNumber } from "../lib/format";
import { useDashboardSummary } from "../hooks/useMacroData";

export function DashboardPage() {
  const { data, isLoading, error, refetch, isFetching } = useDashboardSummary();
  const [selectedCode, setSelectedCode] = useState<string>();

  const indicators = data?.indicators ?? [];
  const demoMode =
    data?.metadata?.demo_mode ??
    indicators.some((item) => item.series.fetch_status === "demo_seed");
  const selectedIndicator = useMemo(
    () => indicators.find((item) => item.series.code === selectedCode) ?? indicators[0],
    [indicators, selectedCode]
  );

  useEffect(() => {
    if (!selectedCode && indicators.length) {
      setSelectedCode(indicators[0].series.code);
    }
  }, [indicators, selectedCode]);

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (error) {
    return (
      <section className="panel p-6">
        <div className="flex items-start gap-3">
          <AlertCircle className="mt-1 h-5 w-5 text-berry" aria-hidden="true" />
          <div>
            <h1 className="text-xl font-semibold text-ink">API bağlantısı kurulamadı</h1>
            <p className="mt-2 text-sm text-slate-600">{String(error.message)}</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="muted-label">Türkiye makro göstergeleri</p>
          <h1 className="mt-1 text-3xl font-bold text-ink">MacroTR Dashboard</h1>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
            TCMB EVDS odaklı açık kaynak makro veri paneli.
          </p>
        </div>
        <button
          type="button"
          className="text-button w-fit"
          onClick={() => void refetch()}
          disabled={isFetching}
        >
          <RefreshCw className={isFetching ? "h-4 w-4 animate-spin" : "h-4 w-4"} />
          Yenile
        </button>
      </section>

      {demoMode ? (
        <section className="rounded-lg border border-amber/30 bg-amber/10 p-4 text-sm leading-6 text-slate-700">
          Demo seed modu aktif. Gerçek TCMB EVDS verisi için `.env` dosyasına
          `EVDS_API_KEY` ekleyip `/api/v1/admin/fetch-data` endpointini local/dev
          ortamında çalıştırın.
        </section>
      ) : null}

      {!indicators.length ? (
        <section className="panel p-8 text-center text-sm text-slate-500">
          Gösterilecek makro seri bulunamadı.
        </section>
      ) : null}

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {indicators.map((indicator) => (
          <IndicatorCard key={indicator.series.code} indicator={indicator} />
        ))}
      </section>

      {selectedIndicator ? (
        <section className="panel p-4">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <p className="muted-label">Seçili seri</p>
              <h2 className="mt-1 text-2xl font-bold text-ink">
                {selectedIndicator.series.name}
              </h2>
              <p className="mt-1 text-sm text-slate-600">
                Son değer: {formatNumber(selectedIndicator.latest_value, selectedIndicator.series.unit)}
                {" · "}
                {formatDate(selectedIndicator.latest_date)}
              </p>
            </div>
            <div className="w-full lg:w-80">
              <SeriesSelector
                series={indicators.map((item) => item.series)}
                value={selectedIndicator.series.code}
                onChange={setSelectedCode}
              />
            </div>
          </div>
          <div className="mt-4">
            <MacroChart
              data={selectedIndicator.sparkline}
              unit={selectedIndicator.series.unit}
              height={360}
            />
          </div>
        </section>
      ) : null}

      {data?.disclaimer ? (
        <section className="rounded-lg border border-amber/30 bg-amber/10 p-4 text-sm leading-6 text-slate-700">
          {data.disclaimer}
        </section>
      ) : null}
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div className="h-24 animate-pulse rounded-lg bg-white" />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }).map((_, index) => (
          <div key={index} className="h-64 animate-pulse rounded-lg bg-white" />
        ))}
      </div>
    </div>
  );
}
