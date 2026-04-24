import { screen } from "@testing-library/react";

import { MacroChart } from "./MacroChart";
import { renderWithProviders } from "../test/testUtils";

test("MacroChart renders empty state", () => {
  renderWithProviders(<MacroChart data={[]} />);

  expect(screen.getByText("Veri yok")).toBeInTheDocument();
});

