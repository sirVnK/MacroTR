import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { formatDate, formatNumber } from "../lib/format";
import type { CompareSeriesItem } from "../types/macro";

const COLORS = ["#138a8a", "#b26b00", "#4f5bd5", "#b4234c", "#567568", "#6d5f8d"];

type Props = {
  items: CompareSeriesItem[];
  height?: number;
};

export function CompareChart({ items, height = 380 }: Props) {
  const rows = mergeSeries(items);

  if (!rows.length) {
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
        <LineChart data={rows} margin={{ top: 10, right: 16, left: 0, bottom: 0 }}>
          <CartesianGrid stroke="#e5e7eb" vertical={false} />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            tick={{ fontSize: 11, fill: "#64748b" }}
            tickLine={false}
            axisLine={false}
            minTickGap={18}
          />
          <YAxis
            tick={{ fontSize: 11, fill: "#64748b" }}
            tickLine={false}
            axisLine={false}
            width={68}
            tickFormatter={(value) => formatNumber(Number(value))}
          />
          <Tooltip
            formatter={(value, key) => [formatNumber(Number(value)), key]}
            labelFormatter={(label) => formatDate(String(label))}
            contentStyle={{
              borderRadius: 8,
              border: "1px solid #d9dde4",
              boxShadow: "0 10px 24px rgba(32,33,36,0.12)"
            }}
          />
          <Legend />
          {items.map((item, index) => (
            <Line
              key={item.series.code}
              type="monotone"
              dataKey={item.series.code}
              stroke={COLORS[index % COLORS.length]}
              strokeWidth={2.4}
              dot={false}
              connectNulls
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function mergeSeries(items: CompareSeriesItem[]) {
  const map = new Map<string, Record<string, string | number | null>>();
  items.forEach((item) => {
    item.observations.forEach((point) => {
      const row = map.get(point.date) ?? { date: point.date };
      row[item.series.code] = point.value;
      map.set(point.date, row);
    });
  });
  return Array.from(map.values()).sort((left, right) =>
    String(left.date).localeCompare(String(right.date))
  );
}

