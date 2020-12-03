import json


def write_json(link, data):
    try:
        if type(data) == str:
            data = data.replace("'", '"')
            data = json.loads(data)
        elif type(data) == dict:
            pass
        with open(link, 'w', encoding="utf8") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
    except json.decoder.JSONDecodeError as e:
        e = str(e)
        if 'Expecting property name enclosed in double quotes' in e:
            print("Один из ключей указан не в двойных скобках '%s'" % e)
        return 0


def read_json(link):
    try:
        open(link, "r", encoding="utf8")
    except IOError:
        with open(link, "w", encoding="utf8") as write_file:
            json.dump({}, write_file, indent=4, ensure_asci=False)
    finally:
        with open(link, "r", encoding="utf8") as read_file:
            data = json.load(read_file)
        return data
