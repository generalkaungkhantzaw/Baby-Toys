#!/usr/bin/env python3

import os
import stat
import pwd
import grp


def get_owner(uid):
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return str(uid)


def get_group(gid):
    try:
        return grp.getgrgid(gid).gr_name
    except KeyError:
        return str(gid)


def get_file_type(mode):
    if stat.S_ISREG(mode):
        return "Regular file"
    if stat.S_ISDIR(mode):
        return "Directory"
    if stat.S_ISLNK(mode):
        return "Symbolic link"
    if stat.S_ISCHR(mode):
        return "Character device"
    if stat.S_ISBLK(mode):
        return "Block device"
    if stat.S_ISFIFO(mode):
        return "FIFO"
    if stat.S_ISSOCK(mode):
        return "Socket"

    return "Unknown"


def explain_permissions(mode):
    permissions = []

    permissions.append(
        "Owner:  "
        + ("r" if mode & stat.S_IRUSR else "-")
        + ("w" if mode & stat.S_IWUSR else "-")
        + ("x" if mode & stat.S_IXUSR else "-")
    )

    permissions.append(
        "Group:  "
        + ("r" if mode & stat.S_IRGRP else "-")
        + ("w" if mode & stat.S_IWGRP else "-")
        + ("x" if mode & stat.S_IXGRP else "-")
    )

    permissions.append(
        "Others: "
        + ("r" if mode & stat.S_IROTH else "-")
        + ("w" if mode & stat.S_IWOTH else "-")
        + ("x" if mode & stat.S_IXOTH else "-")
    )

    return permissions


def special_bits(mode):
    bits = []

    if mode & stat.S_ISUID:
        bits.append("SUID")

    if mode & stat.S_ISGID:
        bits.append("SGID")

    if mode & stat.S_ISVTX:
        bits.append("Sticky bit")

    return bits


def main():
    filename = input("Input file: ")

    if not os.path.exists(filename):
        print("File not found.")
        return

    try:
        info = os.stat(filename)
    except PermissionError:
        print("Permission denied.")
        return

    mode = info.st_mode
    permissions = stat.filemode(mode)

    print("\n========== PERMISSIONS ==========")

    print("Path:        ", os.path.abspath(filename))
    print("Type:        ", get_file_type(mode))
    print("Permissions: ", permissions)
    print("Octal:       ", oct(mode & 0o7777))
    print("Owner:       ", get_owner(info.st_uid))
    print("UID:         ", info.st_uid)
    print("Group:       ", get_group(info.st_gid))
    print("GID:         ", info.st_gid)

    print("\n---------- ACCESS ----------")

    for permission in explain_permissions(mode):
        print(permission)

    print("\n---------- SPECIAL BITS ----------")

    bits = special_bits(mode)

    if bits:
        print("Detected: ", ", ".join(bits))
    else:
        print("Detected: None")

    print("=================================")


if __name__ == "__main__":
    main()
