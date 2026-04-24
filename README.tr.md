# MacroTR

TCMB EVDS, FastAPI, React, PostgreSQL ve Redis ile geliştirilmiş açık kaynak Türkiye makro ekonomik veri dashboardu.

> MacroTR yalnızca eğitim ve bilgilendirme amacıyla geliştirilmiştir. Yatırım tavsiyesi, alım-satım önerisi veya finansal danışmanlık hizmeti sunmaz. Veriler halka açık veya üçüncü taraf kaynaklardan alınır ve doğruluğu garanti edilmez.

[English README](README.md)

## Ekran Görüntüleri

![MacroTR Dashboard](docs/assets/dashboard.png)

![Seri Detayı](docs/assets/series-detail.png)

![Karşılaştırma](docs/assets/compare-page.png)

## Özellikler

- TCMB EVDS odaklı makro veri paneli
- FastAPI backend ve dokümante `/api/v1` endpointleri
- React, Vite, TypeScript, Tailwind CSS ve Recharts frontend
- PostgreSQL seri ve gözlem deposu
- Redis uyumlu cache servisi
- `EVDS_API_KEY` yoksa demo seed modu
- `EVDS_API_KEY` varsa gerçek EVDS veri çekme
- Tarih filtresi ve CSV export içeren seri detay sayfaları
- Normalize/ham değer karşılaştırma sayfası
- Backend ve frontend testleri
- Docker Compose ile tek komut kurulum

## Hızlı Başlangıç

```bash
cp .env.example .env
docker compose up --build -d
```

Adresler:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8010
- Swagger: http://localhost:8010/docs

Durdurmak için:

```bash
docker compose down
```

## Ortam Değişkenleri

| Değişken | Amaç |
| --- | --- |
| `APP_ENV` | `development` veya `production` |
| `DATABASE_URL` | PostgreSQL bağlantı adresi |
| `REDIS_URL` | Opsiyonel Redis bağlantı adresi |
| `EVDS_API_KEY` | TCMB EVDS API anahtarı (opsiyonel) |
| `SEED_SAMPLE_DATA` | Yerel demo gözlemlerini açar |
| `ALLOWED_ORIGINS` | CORS origin listesi |
| `VITE_API_BASE_URL` | Frontend API adresi |
| `BACKEND_PORT` | Yerel backend portu, varsayılan `8010` |
| `FRONTEND_PORT` | Yerel frontend portu, varsayılan `5173` |

## EVDS API Key

MacroTR, EVDS anahtarı olmadan demo veriyle çalışır.

Gerçek TCMB EVDS verisi çekmek için:

1. https://evds2.tcmb.gov.tr üzerinden API key oluştur.
2. `.env` dosyasına ekle:

```env
EVDS_API_KEY=your-key
SEED_SAMPLE_DATA=false
```

3. Servisleri yeniden başlat ve local/dev veri çekme endpointini çağır:

```bash
docker compose up --build -d
curl -X POST "http://localhost:8010/api/v1/admin/fetch-data"
```

`POST /api/v1/admin/fetch-data`, `APP_ENV=production` olduğunda otomatik kapalıdır.

## API Endpointleri

- `GET /api/v1/health`
- `GET /api/v1/series`
- `GET /api/v1/series/{code}`
- `GET /api/v1/series/{code}/observations`
- `GET /api/v1/series/{code}/latest`
- `GET /api/v1/dashboard/summary`
- `GET /api/v1/compare?series=USDTRY,CPI`
- `POST /api/v1/admin/fetch-data`

Detay: [API Reference](docs/api-reference.md)

## Testler

Backend:

```bash
pip install -r backend/requirements.txt
ruff check backend/app backend/tests scripts
pytest
```

Frontend:

```bash
cd frontend
npm install
npm run test
npm run build
```

## Deployment

Frontend Vercel'e, backend Railway/Render/Fly.io üzerine deploy edilebilir. PostgreSQL için Neon, Supabase, Railway veya Render kullanılabilir.

Detay: [docs/deployment.md](docs/deployment.md)

## Veri Kaynakları

MVP yalnızca TCMB EVDS odaklıdır. Sonraki sürümlerde TÜİK, World Bank, FRED, BIST veya altın/döviz sağlayıcıları eklenebilir.

Detay: [docs/data-sources.md](docs/data-sources.md)

## Dokümantasyon

- [Mimari](docs/architecture.md)
- [Veri Kaynakları](docs/data-sources.md)
- [API Referansı](docs/api-reference.md)
- [Deployment](docs/deployment.md)
- [Katkı Rehberi](docs/open-source-guide.md)
- [Güvenlik Notları](docs/security-notes.md)
- [Yol Haritası](ROADMAP.md)

## Sorumluluk Reddi

MacroTR yalnızca eğitim ve bilgilendirme amacıyla geliştirilmiştir. Yatırım tavsiyesi, alım-satım önerisi veya finansal danışmanlık hizmeti sunmaz. Veriler halka açık veya üçüncü taraf kaynaklardan alınır ve doğruluğu garanti edilmez.

## Katkı

Katkılar memnuniyetle karşılanır. Başlamak için [CONTRIBUTING.md](CONTRIBUTING.md) ve [docs/open-source-guide.md](docs/open-source-guide.md) dosyalarına bak.

## Lisans

MIT. Detay: [LICENSE](LICENSE).
