type Props = {
  startDate?: string;
  endDate?: string;
  onStartDateChange: (value: string) => void;
  onEndDateChange: (value: string) => void;
};

export function DateRangePicker({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange
}: Props) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <label className="grid gap-2">
        <span className="muted-label">Başlangıç</span>
        <input
          className="input"
          type="date"
          value={startDate ?? ""}
          onChange={(event) => onStartDateChange(event.target.value)}
        />
      </label>
      <label className="grid gap-2">
        <span className="muted-label">Bitiş</span>
        <input
          className="input"
          type="date"
          value={endDate ?? ""}
          onChange={(event) => onEndDateChange(event.target.value)}
        />
      </label>
    </div>
  );
}

