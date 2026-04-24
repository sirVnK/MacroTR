import { screen } from "@testing-library/react";
import { vi } from "vitest";

import { DashboardPage } from "./DashboardPage";
import { renderWithProviders } from "../test/testUtils";

vi.mock("../hooks/useMacroData", () => ({
  useDashboardSummary: () => ({
    data: {
      generated_at: "2026-04-24T00:00:00Z",
      disclaimer: "Bu proje yatırım tavsiyesi sunmaz.",
      indicators: [
        {
          series: {
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
          },
          latest_date: "2026-04-24",
          latest_value: 36.8,
          previous_value: 36.4,
          change_percent: 1.1,
          sparkline: []
        }
      ]
    },
    isLoading: false,
    error: null,
    refetch: vi.fn(),
    isFetching: false
  })
}));

test("DashboardPage renders summary", () => {
  renderWithProviders(<DashboardPage />);

  expect(screen.getByText("MacroTR Dashboard")).toBeInTheDocument();
  expect(screen.getAllByText("USD/TRY").length).toBeGreaterThan(0);
});

