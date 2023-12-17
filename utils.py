def get_teachers_name():
    with open("list.txt", "rb") as file:
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


def generate_list(names):
    if not isinstance(names, dict):
        return ""
    return "".join(f"{key}. {value}.\n" for key, value in names.items())


if __name__ == "__main__":
    print(get_teachers_name())
