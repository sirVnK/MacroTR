import type { Series } from "../types/macro";

type Props = {
  series: Series[];
  value?: string;
  onChange: (value: string) => void;
  label?: string;
};

export function SeriesSelector({ series, value, onChange, label = "Seri" }: Props) {
  return (
    <label className="grid gap-2">
      <span className="muted-label">{label}</span>
      <select
        className="input"
        value={value ?? ""}
        onChange={(event) => onChange(event.target.value)}
      >
        {series.map((item) => (
          <option key={item.code} value={item.code}>
            {item.name} ({item.code})
          </option>
        ))}
      </select>
    </label>
  );
}

