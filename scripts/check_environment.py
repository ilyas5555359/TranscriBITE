import importlib.util
import shutil
import subprocess
import sys


REQUIRED_MODULES = ("fastapi", "pydantic", "faster_whisper", "torch")


def has_ollama_model(model: str = "gemma2:2b") -> bool:
	ollama = shutil.which("ollama")
	if ollama is None:
		return False

	result = subprocess.run(
		[ollama, "list"],
		capture_output=True,
		text=True,
		check=False,
	)
	return any(line.startswith(model) for line in result.stdout.splitlines())


def main() -> int:
	checks = {
		"Python 3.12": sys.version_info[:2] == (3, 12),
		"FFmpeg": shutil.which("ffmpeg") is not None,
		"Ollama": shutil.which("ollama") is not None,
		"Ollama model gemma2:2b": has_ollama_model(),
	}
	checks.update({
		module: importlib.util.find_spec(module) is not None
		for module in REQUIRED_MODULES
	})

	for name, available in checks.items():
		print(f"{'OK' if available else 'MISSING'}: {name}")

	return 0 if all(checks.values()) else 1


if __name__ == "__main__":
	raise SystemExit(main())
