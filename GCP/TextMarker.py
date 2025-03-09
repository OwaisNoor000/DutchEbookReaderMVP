def markText(current_dir):
    with open(f"{current_dir}/Text.txt",encoding="UTF-8") as file:
        content = file.read()

    sentences = content.split(".")

    markedUpSentences = ["<speak>"]

    for i,sentence in enumerate(sentences):
        markedUpSentences.append(f"<mark name='sentence{i}'/>{sentence}.")
    markedUpSentences.append("</speak>")

    newContent = "".join(markedUpSentences)

    with open(f"{current_dir}/markedText.txt","w",encoding="UTF-8") as f:
        f.write(newContent)

# markText("PREPROCESSED/Jip&Janneke/PAGE12")