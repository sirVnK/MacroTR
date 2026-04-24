import { screen } from "@testing-library/react";

import { IndicatorCard } from "./IndicatorCard";
import { renderWithProviders } from "../test/testUtils";
import type { IndicatorSummary, Series } from "../types/macro";

const series: Series = {
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
};

const indicator: IndicatorSummary = {
  series,
  latest_date: "2026-04-24",
  latest_value: 36.8,
  previous_value: 36.4,
  change_percent: 1.1,
  sparkline: []
};

test("IndicatorCard renders latest value and source", () => {
  renderWithProviders(<IndicatorCard indicator={indicator} />);

  expect(screen.getByText("USD/TRY")).toBeInTheDocument();
  expect(screen.getByText("TCMB EVDS")).toBeInTheDocument();
  expect(screen.getByLabelText("USD/TRY detayına git")).toBeInTheDocument();
});
