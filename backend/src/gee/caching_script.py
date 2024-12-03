import json

content = [
    {"timestamp": 1493251200, "value": 0.6265267304234295},
    {"timestamp": 1494720000, "value": 0.68603163673333},
    {"timestamp": 1494979200, "value": 0.755257128311451},
]
var_name = "msavi_daily_cache"
file_name = "../cache/temp_cache.py"
INDENT = "    "

def combine_chache_with_update():
    # update existing cache
    return

def write_year(file, year, results):
    file.write(f"{INDENT}# Year {year}\n")

def write_results_to_cache(results: list, var_name: str, file_name: str):
    with open(file_name, "w") as file:
        file.write(f"{var_name} = [\n")
        for day in results:
            file.write(f"{INDENT}{json.dumps(day)},\n")
        file.write("]\n")
    file.close()

    return


# write_results_to_cache(content, var_name, file_name)
