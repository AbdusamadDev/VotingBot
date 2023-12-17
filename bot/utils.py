import os
import json


def get_credentials():
    if not os.path.exists("../credentials.json"):
        return None
    with open("../credentials.json", "rb") as creds:
        credentials = json.loads(creds.read())
        return credentials


def get_teachers_name():
    with open("../docs/list.txt", "rb") as file:
        names = {}
        for name in file.read().decode().split("\n"):
            try:
                sliced = name.split("	")
                names[
                    f"{sliced[0]} - maktab" if sliced[0].isdigit() else sliced[0]
                ] = sliced[1]
            except IndexError:
                return names
        file.close()
    return {}


captcha_images = [
    (
        os.path.join(
            "".join(
                [i + "/" for i in os.path.abspath(__name__).split("\\")[:-2]],
            ),
            "docs/captcha",
            filename,
        ).replace("\\", "/"),
        filename.split(".")[0],
    )
    for filename in os.listdir(
        os.path.join(
            "".join(
                [i + "/" for i in os.path.abspath(__name__).split("\\")[:-2]],
            ),
            "docs/captcha",
        )
    )
]


def generate_list(names):
    if not isinstance(names, dict):
        return ""
    return [f"{key}. {value}.\n\n" for key, value in names.items()]


if __name__ == "__main__":
    print(get_credentials())
