from pathlib import Path
import sys
import shutil


def normalize(name):
    map = {
        ord("а"): "a",
        ord("б"): "b",
        ord("в"): "v",
        ord("г"): "h",
        ord("ґ"): "g",
        ord("д"): "d",
        ord("е"): "e",
        ord("є"): "ie",
        ord("ж"): "zh",
        ord("з"): "z",
        ord("и"): "y",
        ord("і"): "i",
        ord("ї"): "i",
        ord("й"): "i",
        ord("к"): "k",
        ord("л"): "l",
        ord("м"): "m",
        ord("н"): "n",
        ord("о"): "o",
        ord("п"): "p",
        ord("р"): "r",
        ord("с"): "s",
        ord("т"): "t",
        ord("у"): "u",
        ord("ф"): "f",
        ord("х"): "kh",
        ord("ц"): "ts",
        ord("ч"): "ch",
        ord("ш"): "sh",
        ord("щ"): "shch",
        ord("ь"): "",
        ord("ю"): "iu",
        ord("я"): "ia",
        ord("А"): "A",
        ord("Б"): "B",
        ord("В"): "V",
        ord("Г"): "H",
        ord("Ґ"): "G",
        ord("Д"): "D",
        ord("Е"): "E",
        ord("Є"): "Ye",
        ord("Ж"): "Zh",
        ord("З"): "Z",
        ord("И"): "Y",
        ord("І"): "I",
        ord("Ї"): "Yi",
        ord("Й"): "Y",
        ord("К"): "K",
        ord("Л"): "L",
        ord("М"): "M",
        ord("Н"): "N",
        ord("О"): "O",
        ord("П"): "P",
        ord("Р"): "R",
        ord("С"): "S",
        ord("Т"): "T",
        ord("У"): "U",
        ord("Ф"): "F",
        ord("Х"): "Kh",
        ord("Ц"): "Ts",
        ord("Ч"): "Ch",
        ord("Ш"): "Sh",
        ord("Щ"): "Shch",
        ord("Ю"): "Yu",
        ord("Я"): "Ya",
        ord("Ё"): "Yo",
        ord("ё"): "yo",
        ord("Ъ"): "",
        ord("ъ"): "",
        ord("Ь"): "",
    }
    normalize_name = name.translate(map)
    finally_name = "".join(ch if ch.isalnum() else "_" for ch in normalize_name)

    return finally_name


def sort_file(folder_name):
    path = Path(folder_name)

    if path.exists():
        if path.is_dir():
            items = path.glob("**/*")

            for item in items:
                try:
                    if item.suffix in [".mp4", ".avi", ".mov", ".mkv"]:
                        dir = path / "video"
                    elif item.suffix in [".mp3", ".ogg", ".wav", ".amr"]:
                        dir = path / "audio"
                    elif item.suffix in [
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".svg",
                        ".snagx",
                        ".gif",
                    ]:
                        dir = path / "images"
                    elif item.suffix in [
                        ".txt",
                        ".doc",
                        ".docx",
                        ".pdf",
                        ".xlsx",
                        ".pptx",
                    ]:
                        dir = path / "documents"
                    elif item.suffix in [".zip", ".gz", ".tar"]:
                        dir = path / "archives" / item.stem
                        dir.mkdir(parents=True, exist_ok=True)
                        shutil.unpack_archive(item, dir)
                        continue
                    elif item.is_dir() and item.name not in [
                        "video",
                        "audio",
                        "images",
                        "documents",
                        "archives",
                    ]:
                        if not any(item.iterdir()):
                            item.rmdir()
                        else:
                            try:
                                item.rename(
                                    item.resolve().parent / Path(normalize(item.name))
                                )
                            except FileExistsError:
                                item.rename(
                                    item.resolve().parent
                                    / Path(normalize(item.name) + "1")
                                )
                        continue

                    else:
                        continue

                    dir.mkdir(parents=True, exist_ok=True)
                    item.rename(dir / (normalize(item.stem) + item.suffix))
                except PermissionError:
                    print(f"The file {item.name} is occupied by a program or process")

        else:
            print(f"{path} is e file")
    else:
        print(f"{path.absolute()} is not exist")


def main():
    folder_name = r"C:\Users\AndriiVlasiuk\Desktop"
    sort_file(folder_name=folder_name)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
        sort_file(folder_name)
    else:
        main()
