import re
import json


def load_or_fetch(json_path, fetch_func):
    try:
        res = json.load(open(json_path))
    except FileNotFoundError:
        res = fetch_func()
        json.dump(res, open(json_path, "w"))
    return res


def get_fields_from_schema(schema):
    text_fields = []
    obj_fields = []
    for property, spec in schema["properties"].items():
        if spec["type"] == "string":
            text_fields.append(property)
        elif spec["type"] in ["array", "object"]:
            obj_fields.append(property)
        else:
            ValueError(
                "We shouldn't have types other than string, array and object."
            )
    all_fields = text_fields + obj_fields
    return text_fields, obj_fields, all_fields


def replace_spaces(text):
    # This regex will match one or more consecutive whitespace characters (including newlines)
    return re.sub(r"\s+", " ", text).strip()


# Get text or number from element with id
def ge(soup, id):
    try:
        element = soup.find(id=id)
        return replace_spaces(element.get_text(strip=True))
    except (AttributeError, ValueError):
        return ""


# Get HTML from element with id
def gh(soup, id):
    try:
        element = soup.find(id=id)
        return replace_spaces(element.decode_contents()) if element else ""
    except AttributeError:
        return ""


# Get a table from element with id
def gt(soup, headers):
    rows_data = []
    # Find all rows in the table (assuming they are in the <tbody> under <tr>)
    for row in soup.select("tbody tr"):
        row_data = {}
        # Find all cells in the row that are not row number cells
        cells = row.find_all("td")
        for header, cell in zip(headers, cells):
            row_data[header] = replace_spaces(cell.get_text(strip=True))

        # Force the data to conform to the format
        for header in headers:
            if header not in row_data:
                row_data[header] = ""
        rows_data.append(row_data)
    return rows_data
