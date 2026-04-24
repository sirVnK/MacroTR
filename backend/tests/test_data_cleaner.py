from app.services.data_cleaner import clean_observations, normalize_points, parse_numeric


def test_parse_numeric_accepts_comma_decimal():
    assert parse_numeric("12,34") == parse_numeric("12.34")


def test_clean_observations_skips_nd_values():
    rows = [
        {"Tarih": "01-01-2024", "TP_DK_USD_A_YTL": "29,50"},
        {"Tarih": "02-01-2024", "TP_DK_USD_A_YTL": "ND"},
    ]

    cleaned = clean_observations(rows, "TP.DK.USD.A.YTL")

    assert len(cleaned) == 1
    assert cleaned[0][1] == parse_numeric("29.50")


def test_normalize_points_uses_first_non_zero_value():
    result = normalize_points(
        [
            {"date": "2024-01-01", "value": 10},
            {"date": "2024-01-02", "value": 15},
        ]
    )

    assert result[0]["value"] == 100
    assert result[1]["value"] == 150

