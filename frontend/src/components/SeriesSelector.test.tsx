import { fireEvent, screen } from "@testing-library/react";
import { vi } from "vitest";

import { SeriesSelector } from "./SeriesSelector";
import { renderWithProviders } from "../test/testUtils";
import type { Series } from "../types/macro";

const series: Series[] = [
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
    last_updated: null,
    last_successful_fetch: null,
    last_fetch_attempt: null,
    fetch_status: "not_fetched",
    fetch_error: null
  }
];

test("SeriesSelector calls onChange", () => {
  const onChange = vi.fn();
  renderWithProviders(<SeriesSelector series={series} value="USDTRY" onChange={onChange} />);

  fireEvent.change(screen.getByLabelText("Seri"), { target: { value: "USDTRY" } });

  expect(onChange).toHaveBeenCalledWith("USDTRY");
});

