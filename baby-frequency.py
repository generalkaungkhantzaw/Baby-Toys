#!/usr/bin/env python3

from collections import Counter
import string


ENGLISH_FREQUENCY = {
    "E": 12.70,
    "T": 9.06,
    "A": 8.17,
    "O": 7.51,
    "I": 6.97,
    "N": 6.75,
    "S": 6.33,
    "H": 6.09,
    "R": 5.99,
    "D": 4.25,
    "L": 4.03,
    "C": 2.78,
    "U": 2.76,
    "M": 2.41,
    "W": 2.36,
    "F": 2.23,
    "G": 2.02,
    "Y": 1.97,
    "P": 1.93,
    "B": 1.49,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.10,
    "Z": 0.07,
}


def analyze(text):
    total = len(text)
    characters = Counter(text)
    letters = Counter(c.upper() for c in text if c.isalpha())
    digits = Counter(c for c in text if c.isdigit())

    return total, characters, letters, digits


def show_table(counter, total, limit=None):
    items = counter.most_common(limit)

    if not items:
        print("None")
        return

    print(f"{'Char':<8}{'Count':>8}{'Percent':>12}")
    print("-" * 28)

    for char, count in items:
        percent = count / total * 100 if total else 0

        if char == "\n":
            display = "\\n"
        elif char == "\r":
            display = "\\r"
        elif char == "\t":
            display = "\\t"
        elif char == " ":
            display = "SPACE"
        elif not char.isprintable():
            display = f"0x{ord(char):02x}"
        else:
            display = char

        print(f"{display:<8}{count:>8}{percent:>11.2f}%")


def show_letter_analysis(letters):
    total = sum(letters.values())

    print("\n---------- LETTERS ----------")

    if not total:
        print("No letters found.")
        return

    print(f"{'Letter':<8}{'Count':>8}{'Percent':>12}{'English':>12}")
    print("-" * 40)

    for letter, count in letters.most_common():
        percent = count / total * 100
        expected = ENGLISH_FREQUENCY.get(letter, 0)

        print(
            f"{letter:<8}"
            f"{count:>8}"
            f"{percent:>11.2f}%"
            f"{expected:>11.2f}%"
        )


def show_summary(text, characters, letters, digits):
    whitespace = sum(c.isspace() for c in text)
    printable = sum(c.isprintable() for c in text)

    print("\n---------- SUMMARY ----------")
    print("Total characters:", len(text))
    print("Letters:         ", sum(letters.values()))
    print("Digits:          ", sum(digits.values()))
    print("Whitespace:      ", whitespace)
    print("Printable:       ", printable)
    print("Unique characters:", len(characters))


def read_input():
    mode = input("Input type [text/file]: ").strip().lower()

    if mode == "file":
        filename = input("File: ").strip()

        try:
            with open(filename, "rb") as file:
                data = file.read()

            return data.decode("utf-8", errors="replace")

        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")

    elif mode == "text":
        return input("Text: ")

    else:
        print("Choose 'text' or 'file'.")

    return None


def main():
    text = read_input()

    if text is None:
        return

    if not text:
        print("Input is empty.")
        return

    total, characters, letters, digits = analyze(text)

    print("\n========== FREQUENCY ==========")

    show_summary(text, characters, letters, digits)

    print("\n---------- CHARACTERS ----------")
    show_table(characters, total)

    show_letter_analysis(letters)

    print("\n---------- DIGITS ----------")
    show_table(digits, sum(digits.values()))

    print("\n---------- TOP 10 ----------")
    show_table(characters, total, 10)

    print("===============================")


if __name__ == "__main__":
    main()
