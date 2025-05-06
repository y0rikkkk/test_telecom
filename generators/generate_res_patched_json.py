import json

def generate_res_pastched_json(config_path: str, delta_path: str, output_path: str) -> None:
    """
    Applies a delta to the original config.json and writes the result to res_patched_config.json.

    Args:
        config_path (str): Path to the original config.json.
        delta_path (str): Path to the delta.json file.
        output_path (str): Path to save the resulting res_patched_config.json file.
        """
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    with open(delta_path, encoding="utf-8") as f:
        delta = json.load(f)

    result = config.copy()

    for key in delta.get("deletions", []):
        result.pop(key, None)

    for item in delta.get("updates", []):
        result[item["key"]] = item["to"]

    for item in delta.get("additions", []):
        result[item["key"]] = item["value"]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)