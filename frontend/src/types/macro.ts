export type Series = {
  code: string;
  evds_code: string;
  name: string;
  description: string;
  source: string;
  frequency: string;
  unit: string;
  category: string;
  is_active: boolean;
  last_updated: string | null;
  last_successful_fetch: string | null;
  last_fetch_attempt: string | null;
  fetch_status: string;
  fetch_error: string | null;
};

export type ObservationPoint = {
  date: string;
  value: number;
};

export type LatestObservation = {
  series_code: string;
  date: string | null;
  value: number | null;
  source?: string | null;
};

export type SeriesListResponse = {
  count: number;
  items: Series[];
};

export type SeriesDetailResponse = Series & {
  latest: LatestObservation | null;
  observations: ObservationPoint[];
};

export type ObservationListResponse = {
  series_code: string;
  count: number;
  observations: ObservationPoint[];
};

export type IndicatorSummary = {
  series: Series;
  latest_date: string | null;
  latest_value: number | null;
  previous_value: number | null;
  change_percent: number | null;
  sparkline: ObservationPoint[];
};

export type DashboardSummaryResponse = {
  generated_at: string;
  disclaimer: string;
  indicators: IndicatorSummary[];
  metadata?: {
    source: string;
    last_updated: string | null;
    cache_status: string;
    demo_mode: boolean;
    warnings: string[];
    errors?: string[];
  };
  warnings?: string[];
};

export type CompareSeriesItem = {
  series: Series;
  observations: ObservationPoint[];
};

export type CompareResponse = {
  normalized: boolean;
  series: CompareSeriesItem[];
};
