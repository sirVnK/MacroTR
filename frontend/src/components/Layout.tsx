import { BarChart3, Database, GitCompare, Info, LineChart } from "lucide-react";
import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Dashboard", icon: BarChart3 },
  { to: "/series/USDTRY", label: "Seriler", icon: LineChart },
  { to: "/compare", label: "Karşılaştır", icon: GitCompare },
  { to: "/data-sources", label: "Kaynaklar", icon: Database },
  { to: "/about", label: "Hakkında", icon: Info }
];

type Props = {
  children: ReactNode;
};

export function Layout({ children }: Props) {
  return (
    <div className="min-h-screen bg-mist">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 lg:flex-row lg:items-center lg:justify-between">
          <NavLink to="/" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-ink text-white">
              <BarChart3 className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <div className="text-xl font-bold text-ink">MacroTR</div>
              <div className="text-xs font-medium text-slate-500">TCMB EVDS makro dashboard</div>
            </div>
          </NavLink>

          <nav className="flex gap-1 overflow-x-auto">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    [
                      "inline-flex h-10 items-center gap-2 rounded-md px-3 text-sm font-semibold transition",
                      isActive
                        ? "bg-ink text-white"
                        : "text-slate-600 hover:bg-slate-100 hover:text-ink"
                    ].join(" ")
                  }
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {item.label}
                </NavLink>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>

      <footer className="border-t border-line bg-white">
        <div className="mx-auto max-w-7xl px-4 py-5 text-xs leading-5 text-slate-500">
          MacroTR yalnızca eğitim ve bilgilendirme amacıyla geliştirilmiştir.
          Yatırım tavsiyesi, alım-satım önerisi veya finansal danışmanlık hizmeti sunmaz.
          Veriler halka açık veya üçüncü taraf kaynaklardan alınır ve doğruluğu garanti edilmez.
        </div>
      </footer>
    </div>
  );
}

