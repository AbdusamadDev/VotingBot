def get_teachers_name():
    with open("list.txt", "rb") as file:
        names = {}
        for name in file.read().decode().split("\n"):
            sliced = name.split("")
            names[sliced[0].strip()] = sliced[-1].strip()
    print(names)


get_teachers_name()
