import pytest
from practice.module_6_web_scraping.stock_info_requests import sort_sheet_dict_list

def test_sort_sheet_dict_list():
    data = [
        {"week_change": 5.2, "Name": "Company A"},
        {"week_change": 12.3, "Name": "Company B"},
        {"week_change": 3.1, "Name": "Company C"}
    ]

    sorted_data = sort_sheet_dict_list(data, "week_change", reverse=False)

    assert sorted_data[0]["Name"] == "Company C"
    assert sorted_data[1]["Name"] == "Company A"
    assert sorted_data[2]["Name"] == "Company B"

def test_sort_sheet_dict_list_reverse():
    data = [
        {"week_change": 5.2, "Name": "Company A"},
        {"week_change": 12.3, "Name": "Company B"},
        {"week_change": 3.1, "Name": "Company C"}
    ]

    sorted_data = sort_sheet_dict_list(data, "week_change", reverse=True)

    assert sorted_data[0]["Name"] == "Company B"
    assert sorted_data[1]["Name"] == "Company A"
    assert sorted_data[2]["Name"] == "Company C"

def test_sort_sheet_dict_list_empty_field():
    data = [
        {"week_change": 5.2, "Name": "Company A"},
        {"week_change": None, "Name": "Company B"},
        {"week_change": 3.1, "Name": "Company C"}
    ]

    with pytest.raises(TypeError):
        sort_sheet_dict_list(data, "week_change", reverse=False)