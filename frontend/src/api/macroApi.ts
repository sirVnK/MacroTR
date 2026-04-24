import type {
  CompareResponse,
  DashboardSummaryResponse,
  ObservationListResponse,
  SeriesDetailResponse,
  SeriesListResponse
} from "../types/macro";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

type QueryValue = string | number | boolean | undefined | null;

function buildQuery(params: Record<string, QueryValue>) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") {
      return;
    }
    query.set(key, String(value));
  });
  const text = query.toString();
  return text ? `?${text}` : "";
}

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { Accept: "application/json" }
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail ?? `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const macroApi = {
  dashboardSummary: () => request<DashboardSummaryResponse>("/dashboard/summary"),

  listSeries: (search?: string, category?: string) =>
    request<SeriesListResponse>(
      `/series${buildQuery({
        search,
        category
      })}`
    ),

  seriesDetail: (code: string, limit = 180) =>
    request<SeriesDetailResponse>(`/series/${code}${buildQuery({ limit })}`),

  observations: (
    code: string,
    startDate?: string,
    endDate?: string,
    limit = 1000
  ) =>
    request<ObservationListResponse>(
      `/series/${code}/observations${buildQuery({
        start_date: startDate,
        end_date: endDate,
        limit
      })}`
    ),

  compare: (
    codes: string[],
    normalize: boolean,
    startDate?: string,
    endDate?: string
  ) =>
    request<CompareResponse>(
      `/compare${buildQuery({
        series: codes.join(","),
        normalize,
        start_date: startDate,
        end_date: endDate
      })}`
    )
};

