import os
from lxml import etree
import json
from statistics import mean

def generate_xml_file():
    # Get city names and the date
    cities = os.listdir(os.path.join(os.path.dirname(__file__), "source_data"))
    dates = set([os.listdir(os.path.join(os.path.dirname(__file__), "source_data", c))[0].split(".")[0] for c in cities])

    for date in dates:
        # Create xml root and other elements
        root = etree.Element("weather", country="Spain", date=date)
        cities_el = etree.Element("cities")
        root.append(cities_el)

        # Generate list of dictionaries from .json files
        date_cities_data_dicts = []

        for i, c in enumerate(cities):
            date_city_data_dict = {"city": c, "city_temps": [], "city_wind_speeds": []}
            date_city_file = os.path.join(os.path.dirname(__file__), "source_data", c, f"{date}.json")
            date_city_data_dict["date_city_file"] = date_city_file

            # Get information from a singular .json file
            with open(date_city_file, "r") as f:
                date_city_dict = json.loads(f.read())["hourly"]

            # Combine hourly data
            for h in date_city_dict:
                date_city_data_dict["city_temps"].append(h["temp"])
                date_city_data_dict["city_wind_speeds"].append(h["wind_speed"])

            date_cities_data_dicts.append(date_city_data_dict)

        # Calculate necessary statistics for cities
        for d in date_cities_data_dicts:
            d["mean_temp"] = round(mean(d["city_temps"]), 2)
            d["max_temp"] = round(max(d["city_temps"]), 2)
            d["min_temp"] = round(min(d["city_temps"]), 2)
            d["mean_wind_speed"] = round(mean(d["city_wind_speeds"]), 2)
            d["max_wind_speed"] = round(max(d["city_wind_speeds"]), 2)
            d["min_wind_speed"] = round(min(d["city_wind_speeds"]), 2)

            # Add all cities to the .xml file structure
            city = etree.Element(d["city"].replace(" ", "_"), mean_temp=str(d["mean_temp"]), max_temp=str(d["max_temp"]),
                                      min_temp=str(d["min_temp"]), mean_wind_speed=str(d["mean_wind_speed"]),
                                      max_wind_speed=str(d["max_wind_speed"]), min_wind_speed=str(d["min_wind_speed"]))
            cities_el.append(city)

        # Calculate necessary statistics for summary
        mean_temp = round(mean(d["mean_temp"] for d in date_cities_data_dicts), 2)
        mean_wind_speed = round(mean(d["mean_wind_speed"] for d in date_cities_data_dicts), 2)
        coldest_place = min(date_cities_data_dicts, key = lambda x: x["mean_temp"])["city"]
        warmest_place = max(date_cities_data_dicts, key = lambda x: x["mean_temp"])["city"]
        windiest_place = max(date_cities_data_dicts, key = lambda x: x["mean_wind_speed"])["city"]

        # Add summary to the .xml file structure
        root.append(etree.Element("summary", mean_temp=str(mean_temp), mean_wind_speed=str(mean_wind_speed),
                                  coldest_place=coldest_place, warmest_place=warmest_place,
                                  windiest_place=windiest_place))

        # Create .xml file
        tree = etree.ElementTree(root)
        file = os.path.join(os.path.dirname(__file__), "tests/example_result.xml")
        tree.write(file, pretty_print=True)


if __name__ == "__main__":
    generate_xml_file()