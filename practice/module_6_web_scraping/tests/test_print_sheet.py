from practice.module_6_web_scraping.stock_info_requests import print_sheet

def test_print_sheet_output(capfd):
    sheet_title = "Sheet"
    sheet_dict_list = [
        {
            "Name": "Pfizer Inc.",
            "Code": "PFE",
            "Country": "United States",
            "Employees": "78500",
            "CEO Name": "Dr. Albert Bourla D.V.M., DVM, Ph.D.",
            "CEO Year Born": "1962",
        },
        {
            "Name": "Pfizer Inc.",
            "Code": "PFE",
            "Country": "United States",
            "Employees": "78500",
            "CEO Name": "Dr. Albert Bourla D.V.M., DVM, Ph.D.",
            "CEO Year Born": "1962",
        },
    ]

    print_sheet(sheet_title, sheet_dict_list[0].keys(), sheet_dict_list)

    captured = capfd.readouterr()

    expected = (
        "==================================================Sheet==================================================\n"
        "| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |\n"
        "---------------------------------------------------------------------------------------------------------\n"
        "| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |\n\n"
    )

    assert captured.out == expected

