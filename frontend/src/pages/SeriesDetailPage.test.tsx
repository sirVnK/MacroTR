import { screen } from "@testing-library/react";
import { vi } from "vitest";

import { SeriesDetailPage } from "./SeriesDetailPage";
import { renderWithProviders } from "../test/testUtils";

vi.mock("../hooks/useMacroData", () => ({
  useSeries: () => ({
    data: {
      count: 1,
      items: [
        {
          code: "USDTRY",
          evds_code: "TP.DK.USD.A.YTL",
          name: "USD/TRY",
          description: "US dollar Turkish lira exchange rate.",
          source: "TCMB EVDS",
          frequency: "daily",
          unit: "TRY",
          category: "exchange_rate",
          is_active: true,
          last_updated: "2026-04-24T00:00:00Z",
          last_successful_fetch: "2026-04-24T00:00:00Z",
          last_fetch_attempt: "2026-04-24T00:00:00Z",
          fetch_status: "demo_seed",
          fetch_error: null
        }
      ]
    }
  }),
  useSeriesDetail: () => ({
    data: {
      code: "USDTRY",
      evds_code: "TP.DK.USD.A.YTL",
      name: "USD/TRY",
      description: "US dollar Turkish lira exchange rate.",
      source: "TCMB EVDS",
      frequency: "daily",
      unit: "TRY",
      category: "exchange_rate",
      is_active: true,
      last_updated: "2026-04-24T00:00:00Z",
      last_successful_fetch: "2026-04-24T00:00:00Z",
      last_fetch_attempt: "2026-04-24T00:00:00Z",
      fetch_status: "demo_seed",
      fetch_error: null,
      latest: { series_code: "USDTRY", date: "2026-04-24", value: 36.8 },
      observations: []
    }
  }),
  useObservations: () => ({
    data: {
      series_code: "USDTRY",
      count: 2,
      observations: []
    }
  })
}));

test("SeriesDetailPage renders chart controls and table", () => {
  renderWithProviders(<SeriesDetailPage />, ["/series/USDTRY"]);

  expect(screen.getByText("USD/TRY")).toBeInTheDocument();
  expect(screen.getByText("Son 12 gözlem")).toBeInTheDocument();
  expect(screen.getByText("CSV")).toBeInTheDocument();
});
