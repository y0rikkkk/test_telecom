import json

def generate_delta_json(original_path: str, patched_path: str, output_path: str) -> None:
    """
    Generates a delta.json file showing differences between two configuration files.

    Args:
        original_path (str): Path to the original config.json.
        patched_path (str): Path to the modified patched_config.json.
        output_path (str): Path to save the resulting delta.json.
    """
    with open(original_path, encoding="utf-8") as f:
        original = json.load(f)

    with open(patched_path, encoding="utf-8") as f:
        patched = json.load(f)

    additions = []
    deletions = []
    updates = []

    for key in original:
        if key not in patched:
            deletions.append(key)
        elif original[key] != patched[key]:
            updates.append({
                "key": key,
                "from": original[key],
                "to": patched[key]
            })

    for key in patched:
        if key not in original:
            additions.append({
                "key": key,
                "value": patched[key]
            })

    delta = {
        "additions": additions,
        "deletions": deletions,
        "updates": updates
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(delta, f, indent=4, ensure_ascii=False)