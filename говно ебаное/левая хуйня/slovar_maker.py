
with open("ru_slovar.txt", "r", encoding="cp1251", errors="ignore") as input_file:
    with open("output.txt", "w") as output_file:
        for line in input_file:
            line = line.replace("́", "").split(",")[0]
            line = line.replace(";", "")
            line = line.replace("'", "")
            line = line.replace(":", "")
            line = line.strip()
            if not line:
                continue
            words = line.split()
            for word in words:
                if len(word) > 5:
                    output_file.write(word + " ")
                    break
            output_file.write("\n")
