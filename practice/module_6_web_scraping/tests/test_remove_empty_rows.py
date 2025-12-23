from practice.module_6_web_scraping.stock_info_requests import remove_empty_rows

def test_remove_empty_rows():
    data = [
        {"ceo_year_born": 1970, "Name": "Company A"},
        {"ceo_year_born": None, "Name": "Company B"},
        {"ceo_year_born": 1985, "Name": "Company C"}
    ]

    filtered = remove_empty_rows(data, "ceo_year_born")

    assert len(filtered) == 2
    assert all(row["ceo_year_born"] is not None for row in filtered)
    assert filtered[0]["Name"] == "Company A"
    assert filtered[1]["Name"] == "Company C"
