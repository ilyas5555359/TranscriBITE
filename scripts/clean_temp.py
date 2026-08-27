from pathlib import Path
import shutil


TEMP_FOLDER = Path(__file__).resolve().parents[1] / "storage" / "temp"


def main() -> None:
	TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
	removed = 0
	for item in TEMP_FOLDER.iterdir():
		if item.is_dir():
			shutil.rmtree(item)
		else:
			item.unlink()
		removed += 1
	print(f"Removed {removed} temporary item(s) from {TEMP_FOLDER}")


if __name__ == "__main__":
	main()
