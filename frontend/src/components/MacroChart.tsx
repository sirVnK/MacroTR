import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { formatDate, formatNumber } from "../lib/format";
import type { ObservationPoint } from "../types/macro";

type Props = {
  data: ObservationPoint[];
  unit?: string;
  color?: string;
  height?: number;
  compact?: boolean;
};

export function MacroChart({
  data,
  unit,
  color = "#138a8a",
  height = 320,
  compact = false
}: Props) {
  if (!data.length) {
    return (
      <div
        className="flex items-center justify-center rounded-md border border-dashed border-line bg-mist text-sm text-slate-500"
        style={{ height }}
      >
        Veri yok
      </div>
    );
  }

  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 12, left: compact ? -24 : 0, bottom: 0 }}>
          {!compact ? <CartesianGrid stroke="#e5e7eb" vertical={false} /> : null}
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            tick={{ fontSize: 11, fill: "#64748b" }}
            tickLine={false}
            axisLine={false}
            minTickGap={compact ? 32 : 18}
          />
          <YAxis
            hide={compact}
            tick={{ fontSize: 11, fill: "#64748b" }}
            tickLine={false}
            axisLine={false}
            width={70}
            tickFormatter={(value) => formatNumber(Number(value))}
          />
          <Tooltip
            formatter={(value) => [formatNumber(Number(value), unit), "Değer"]}
            labelFormatter={(label) => formatDate(String(label))}
            contentStyle={{
              borderRadius: 8,
              border: "1px solid #d9dde4",
              boxShadow: "0 10px 24px rgba(32,33,36,0.12)"
            }}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke={color}
            strokeWidth={compact ? 2 : 2.5}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

