import { screen } from "@testing-library/react";

import { CompareChart } from "./CompareChart";
import { renderWithProviders } from "../test/testUtils";

test("CompareChart renders empty state", () => {
  renderWithProviders(<CompareChart items={[]} />);

  expect(screen.getByText("Veri yok")).toBeInTheDocument();
});

