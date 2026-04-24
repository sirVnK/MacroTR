import { Navigate, Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { AboutPage } from "./pages/AboutPage";
import { ComparePage } from "./pages/ComparePage";
import { DashboardPage } from "./pages/DashboardPage";
import { DataSourcesPage } from "./pages/DataSourcesPage";
import { SeriesDetailPage } from "./pages/SeriesDetailPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/series" element={<Navigate to="/series/USDTRY" replace />} />
        <Route path="/series/:code" element={<SeriesDetailPage />} />
        <Route path="/compare" element={<ComparePage />} />
        <Route path="/data-sources" element={<DataSourcesPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Layout>
  );
}

