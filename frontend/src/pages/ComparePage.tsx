import { GitCompare } from "lucide-react";
import { useState } from "react";

import { CompareChart } from "../components/CompareChart";
import { DateRangePicker } from "../components/DateRangePicker";
import { useCompareSeries, useSeries } from "../hooks/useMacroData";

const EXAMPLES = [
  { label: "USD/TRY vs TÜFE", codes: ["USDTRY", "CPI"] },
  { label: "Faiz vs enflasyon", codes: ["POLICY_RATE", "CPI"] },
  { label: "İşsizlik vs üretim", codes: ["UNEMPLOYMENT", "INDUSTRIAL_PRODUCTION"] },
  { label: "EUR/TRY vs USD/TRY", codes: ["EURTRY", "USDTRY"] }
];

export function ComparePage() {
  const [selectedCodes, setSelectedCodes] = useState(["USDTRY", "CPI"]);
  const [normalize, setNormalize] = useState(true);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const seriesQuery = useSeries();
  const compareQuery = useCompareSeries(selectedCodes, normalize, startDate, endDate);

  function toggleCode(code: string) {
    setSelectedCodes((current) => {
      if (current.includes(code)) {
        return current.filter((item) => item !== code);
      }
      return current.length >= 6 ? current : [...current, code];
    });
  }

  return (
    <div className="space-y-6">
      <section>
        <p className="muted-label">Karşılaştırma</p>
        <h1 className="mt-1 text-3xl font-bold text-ink">Makro serileri karşılaştır</h1>
      </section>

      <section className="grid gap-4 lg:grid-cols-[320px_minmax(0,1fr)]">
        <aside className="panel space-y-5 p-4">
          <div className="space-y-2">
            <p className="muted-label">Örnekler</p>
            <div className="grid gap-2">
              {EXAMPLES.map((example) => (
                <button
                  key={example.label}
                  type="button"
                  className="text-button justify-start"
                  onClick={() => setSelectedCodes(example.codes)}
                >
                  <GitCompare className="h-4 w-4" aria-hidden="true" />
                  {example.label}
                </button>
              ))}
            </div>
          </div>

          <label className="flex items-center gap-2 text-sm font-semibold text-slate-700">
            <input
              type="checkbox"
              checked={normalize}
              onChange={(event) => setNormalize(event.target.checked)}
            />
            Normalize et
          </label>

          <DateRangePicker
            startDate={startDate}
            endDate={endDate}
            onStartDateChange={setStartDate}
            onEndDateChange={setEndDate}
          />

          <div className="space-y-2">
            <p className="muted-label">Seriler</p>
            <div className="max-h-[420px] space-y-2 overflow-y-auto pr-1">
              {(seriesQuery.data?.items ?? []).map((item) => (
                <label
                  key={item.code}
                  className="flex cursor-pointer items-start gap-3 rounded-md border border-line bg-white p-3 text-sm"
                >
                  <input
                    type="checkbox"
                    checked={selectedCodes.includes(item.code)}
                    onChange={() => toggleCode(item.code)}
                  />
                  <span>
                    <span className="font-semibold text-ink">{item.name}</span>
                    <span className="block text-xs text-slate-500">{item.code}</span>
                  </span>
                </label>
              ))}
            </div>
          </div>
        </aside>

        <section className="panel p-4">
          <CompareChart items={compareQuery.data?.series ?? []} />
          {compareQuery.error ? (
            <p className="mt-3 text-sm text-berry">{String(compareQuery.error.message)}</p>
          ) : null}
        </section>
      </section>
    </div>
  );
}
