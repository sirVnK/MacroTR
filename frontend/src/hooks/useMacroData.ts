import { useQuery } from "@tanstack/react-query";

import { macroApi } from "../api/macroApi";

export function useDashboardSummary() {
  return useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: macroApi.dashboardSummary,
    staleTime: 60_000,
    refetchInterval: 120_000
  });
}

export function useSeries(search?: string, category?: string) {
  return useQuery({
    queryKey: ["series", search ?? "", category ?? ""],
    queryFn: () => macroApi.listSeries(search, category),
    staleTime: 300_000
  });
}

export function useSeriesDetail(code?: string) {
  return useQuery({
    queryKey: ["series-detail", code],
    queryFn: () => macroApi.seriesDetail(code as string),
    enabled: Boolean(code),
    staleTime: 120_000
  });
}

export function useObservations(code?: string, startDate?: string, endDate?: string) {
  return useQuery({
    queryKey: ["observations", code, startDate ?? "", endDate ?? ""],
    queryFn: () => macroApi.observations(code as string, startDate, endDate),
    enabled: Boolean(code),
    staleTime: 120_000
  });
}

export function useCompareSeries(
  codes: string[],
  normalize: boolean,
  startDate?: string,
  endDate?: string
) {
  return useQuery({
    queryKey: ["compare", codes, normalize, startDate ?? "", endDate ?? ""],
    queryFn: () => macroApi.compare(codes, normalize, startDate, endDate),
    enabled: codes.length >= 2,
    staleTime: 120_000
  });
}

