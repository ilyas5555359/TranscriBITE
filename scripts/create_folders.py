from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
	folders = (
		ROOT / "storage" / "uploads",
		ROOT / "storage" / "outputs",
		ROOT / "storage" / "temp",
		ROOT / "storage" / "cache",
		ROOT / "logs",
	)
	for folder in folders:
		folder.mkdir(parents=True, exist_ok=True)
		print(f"Created: {folder}")


if __name__ == "__main__":
	main()
