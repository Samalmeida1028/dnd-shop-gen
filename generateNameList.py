import json
def main():
    filename = input("Enter file name: ")
    nameList = []

    while True:
        user_input = input()

        # if user pressed Enter without a value, break out of loop
        if user_input == '':
            break
        else:
            nameList.append(user_input + '\n')

    generateFileList(filename, nameList)


# just generates a list given a user input separated by a space, useful for inputting large lists of items

def generateFileList(filename, namelist):
    try:
        f = open(filename, "x")
    except FileExistsError:
        f = open(filename, "r+")
    lines = []
    for l in f:
        l.strip("\n")
        lines = l.split(",")
    for i in range(len(lines) - 1):
        lines[i] = lines[i].strip("\n")
    lines = ','.join(lines)
    namelist = ','.join(namelist)
    lines += namelist
    json.dump(lines, f)
    f.close()


if __name__ == '__main__':
    main()
