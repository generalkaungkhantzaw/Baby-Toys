#!/usr/bin/env python3


def caesar(text, shift):
    result = ""

    for char in text:
        if "a" <= char <= "z":
            result += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        elif "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
        else:
            result += char

    return result


text = input("Input: ")
shift = input("Shift: ")

print("\n========== CAESAR ==========")
print("Input:", text)

if shift:
    try:
        shift = int(shift)
        print(f"Shift: {shift}")
        print("\nResult:", caesar(text, shift))
    except ValueError:
        print("Shift must be a number.")
else:
    print("\n---------- ALL SHIFTS ----------")

    for shift in range(26):
        print(f"{shift:2}: {caesar(text, shift)}")

print("===============================")
