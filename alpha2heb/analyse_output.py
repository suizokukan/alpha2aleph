import unicodedata
with open("output.txt") as src:
    data = src.read()

    print(data)

    for i, char in enumerate(data):

        try:
            name = unicodedata.name(char)

            print("*", i, "["+char+"]", hex(ord(char)), name)
        except ValueError as err:
            name = "UNKNOWN"
            print("?", i, "["+char+"]", hex(ord(char)), err)
