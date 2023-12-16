def get_teachers_name():
    with open("list.txt", "rb") as file:
        names = {}
        for name in file.read().decode().split("\n"):
            try:
                sliced = name.split("	")
                print(sliced)
                names[
                    f"{sliced[0]} - maktab" if sliced[0].isdigit() else sliced[0]
                ] = sliced[1]
            except IndexError:
                return names


if __name__ == "__main__":
    print(get_teachers_name())
