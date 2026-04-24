import { Database } from "lucide-react";

import { formatDate } from "../lib/format";

type Props = {
  source: string;
  lastUpdated?: string | null;
};

export function DataSourceBadge({ source, lastUpdated }: Props) {
  return (
    <div className="inline-flex min-h-8 items-center gap-2 rounded-md border border-line bg-mist px-2.5 text-xs font-semibold text-slate-700">
      <Database className="h-3.5 w-3.5 text-teal" aria-hidden="true" />
      <span>{source}</span>
      {lastUpdated ? <span className="text-slate-500">{formatDate(lastUpdated)}</span> : null}
    </div>
  );
}

