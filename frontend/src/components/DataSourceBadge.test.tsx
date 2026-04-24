import { screen } from "@testing-library/react";

import { DataSourceBadge } from "./DataSourceBadge";
import { renderWithProviders } from "../test/testUtils";

test("DataSourceBadge renders source name", () => {
  renderWithProviders(<DataSourceBadge source="TCMB EVDS" lastUpdated="2026-04-24T00:00:00Z" />);

  expect(screen.getByText("TCMB EVDS")).toBeInTheDocument();
});

