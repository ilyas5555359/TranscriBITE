import argparse
import shutil
import subprocess


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Installe le modèle de résumé Ollama requis par TranscriBITE."
	)
	parser.add_argument("--model", default="gemma2:2b")
	args = parser.parse_args()

	ollama = shutil.which("ollama")
	if ollama is None:
		print("Ollama est introuvable dans le PATH.")
		return 1

	result = subprocess.run([ollama, "pull", args.model], check=False)
	return result.returncode


if __name__ == "__main__":
	raise SystemExit(main())
