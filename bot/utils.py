import os
import json
import calendar
from datetime import datetime

path = "/root/telegram-bot/VotingBot/"

def get_credentials():
    if not os.path.exists(path + "credentials.json"):
        return None
    with open(path + "credentials.json", "rb") as creds:
        credentials = json.loads(creds.read())
        return credentials


def get_teachers_name():
    with open(path + "docs/list.txt", "rb") as file:
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
            path + "docs/captcha",
            filename,
        ).replace("\\", "/"),
        filename.split(".")[0],
    )
    for filename in os.listdir(
        os.path.join(
            "".join(
                [i + "/" for i in os.path.abspath(__name__).split("\\")[:-2]],
            ),
            path + "docs/captcha",
        )
    )
]


def generate_list(names):
    if not isinstance(names, dict):
        return ""
    return [f"{key}. {value}.\n\n" for key, value in names.items()]


month_names = [calendar.month_name[month_idx] for month_idx in range(1, 13)]


if __name__ == "__main__":
    print(len(month_names))
    print(datetime.now().month)
