import { ArrowRight, TrendingDown, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";

import { formatNumber, formatPercent } from "../lib/format";
import type { IndicatorSummary } from "../types/macro";
import { DataSourceBadge } from "./DataSourceBadge";
import { MacroChart } from "./MacroChart";

type Props = {
  indicator: IndicatorSummary;
};

export function IndicatorCard({ indicator }: Props) {
  const isPositive = (indicator.change_percent ?? 0) >= 0;
  const TrendIcon = isPositive ? TrendingUp : TrendingDown;

  return (
    <article className="panel flex min-h-[250px] flex-col p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="muted-label">{indicator.series.code}</p>
          <h3 className="mt-1 truncate text-lg font-semibold text-ink">
            {indicator.series.name}
          </h3>
        </div>
        <Link
          to={`/series/${indicator.series.code}`}
          className="icon-button shrink-0"
          title="Seri detayı"
          aria-label={`${indicator.series.name} detayına git`}
        >
          <ArrowRight className="h-4 w-4" aria-hidden="true" />
        </Link>
      </div>

      <div className="mt-4 flex items-end justify-between gap-3">
        <div>
          <div className="text-2xl font-bold text-ink">
            {formatNumber(indicator.latest_value, indicator.series.unit)}
          </div>
          <div className="mt-1 flex items-center gap-1 text-sm text-slate-600">
            <TrendIcon
              className={isPositive ? "h-4 w-4 text-teal" : "h-4 w-4 text-berry"}
              aria-hidden="true"
            />
            {formatPercent(indicator.change_percent)}
          </div>
        </div>
        <DataSourceBadge
          source={indicator.series.source}
          lastUpdated={indicator.series.last_updated}
        />
      </div>

      <div className="mt-4 grow">
        <MacroChart
          data={indicator.sparkline}
          unit={indicator.series.unit}
          height={110}
          compact
        />
      </div>
    </article>
  );
}

