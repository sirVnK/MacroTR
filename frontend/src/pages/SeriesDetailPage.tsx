import { Download } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { DataSourceBadge } from "../components/DataSourceBadge";
import { DateRangePicker } from "../components/DateRangePicker";
import { MacroChart } from "../components/MacroChart";
import { SeriesSelector } from "../components/SeriesSelector";
import { formatDate, formatNumber, formatPercent, toCsv } from "../lib/format";
import { useObservations, useSeries, useSeriesDetail } from "../hooks/useMacroData";

export function SeriesDetailPage() {
  const params = useParams();
  const navigate = useNavigate();
  const code = (params.code ?? "USDTRY").toUpperCase();
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [csvWarning, setCsvWarning] = useState("");

  const seriesQuery = useSeries();
  const detailQuery = useSeriesDetail(code);
  const observationsQuery = useObservations(code, startDate, endDate);

  const detail = detailQuery.data;
  const observations =
    observationsQuery.data?.observations ?? detailQuery.data?.observations ?? [];
  const latest = observations[observations.length - 1];
  const previous = observations[observations.length - 2];
  const yearAgo = observations[Math.max(0, observations.length - 13)];

  const shortTableRows = useMemo(() => observations.slice(-12).reverse(), [observations]);

  function exportCsv() {
    if (!observations.length) {
      setCsvWarning("CSV export için uygun gözlem verisi bulunamadı.");
      return;
    }
    setCsvWarning("");
    const csv = toCsv(
      observations.map((point) => ({
        series_code: code,
        series_name: detail?.name ?? code,
        date: point.date,
        value: point.value,
        source: detail?.source ?? "TCMB EVDS",
        frequency: detail?.frequency ?? "",
        unit: detail?.unit ?? ""
      }))
    );
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `macrotr_${code.toLowerCase()}_${new Date().toISOString().slice(0, 10)}.csv`;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div>
          <p className="muted-label">{code}</p>
          <h1 className="mt-1 text-3xl font-bold text-ink">
            {detail?.name ?? "Seri detayı"}
          </h1>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
            {detail?.description ?? "Seri bilgisi yükleniyor."}
          </p>
        </div>

        <div className="panel p-4">
          <SeriesSelector
            label="Seri seç"
            series={seriesQuery.data?.items ?? []}
            value={code}
            onChange={(value) => navigate(`/series/${value}`)}
          />
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Metric label="Son değer" value={formatNumber(latest?.value, detail?.unit)} />
        <Metric
          label="Önceki veriye göre"
          value={formatPercent(percentChange(latest?.value, previous?.value))}
        />
        <Metric
          label="Yaklaşık yıllık değişim"
          value={formatPercent(percentChange(latest?.value, yearAgo?.value))}
        />
      </section>

      <section className="panel p-4">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex flex-wrap items-center gap-3">
            {detail ? (
              <DataSourceBadge source={detail.source} lastUpdated={detail.last_updated} />
            ) : null}
            <span className="text-sm text-slate-500">Son tarih: {formatDate(latest?.date)}</span>
          </div>
          <button type="button" className="text-button w-fit" onClick={exportCsv}>
            <Download className="h-4 w-4" aria-hidden="true" />
            CSV
          </button>
        </div>
        {csvWarning ? <p className="mt-3 text-sm text-berry">{csvWarning}</p> : null}

        <div className="mt-4 grid gap-4 lg:grid-cols-[260px_minmax(0,1fr)]">
          <DateRangePicker
            startDate={startDate}
            endDate={endDate}
            onStartDateChange={setStartDate}
            onEndDateChange={setEndDate}
          />
          <MacroChart data={observations} unit={detail?.unit} height={390} />
        </div>
      </section>

      <section className="rounded-lg border border-amber/30 bg-amber/10 p-4 text-sm leading-6 text-slate-700">
        Bu sayfadaki veriler eğitim ve bilgilendirme amaçlıdır; yatırım tavsiyesi,
        alım-satım önerisi veya finansal danışmanlık hizmeti sunmaz.
      </section>

      <section className="panel overflow-hidden">
        <div className="border-b border-line px-4 py-3">
          <h2 className="text-lg font-semibold text-ink">Son 12 gözlem</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-mist text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-3">Tarih</th>
                <th className="px-4 py-3">Değer</th>
              </tr>
            </thead>
            <tbody>
              {shortTableRows.map((point) => (
                <tr key={point.date} className="border-t border-line">
                  <td className="px-4 py-3">{formatDate(point.date)}</td>
                  <td className="px-4 py-3 font-semibold">
                    {formatNumber(point.value, detail?.unit)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="panel p-4">
      <p className="muted-label">{label}</p>
      <p className="mt-2 text-2xl font-bold text-ink">{value}</p>
    </div>
  );
}

function percentChange(latest?: number, previous?: number) {
  if (latest === undefined || previous === undefined || previous === 0) {
    return null;
  }
  return ((latest - previous) / previous) * 100;
}
