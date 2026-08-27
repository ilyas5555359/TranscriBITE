import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.ai.whisper_manager import WhisperModelManager
from app.services.transcription_service import TranscriptionService


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mesure le temps de transcription Faster-Whisper."
    )
    parser.add_argument("audio", type=Path)
    parser.add_argument("--model", default="base")
    parser.add_argument("--language", default="auto")
    args = parser.parse_args()

    if not args.audio.is_file():
        print(f"Fichier introuvable : {args.audio}")
        return 1

    started = time.perf_counter()
    service = TranscriptionService(WhisperModelManager(args.model))
    result = service.transcribe(
        str(args.audio),
        language=args.language,
    )
    elapsed = time.perf_counter() - started

    print(f"file={args.audio}")
    print(f"size_bytes={args.audio.stat().st_size}")
    print(f"duration_seconds={elapsed:.2f}")
    print(f"language={result['language']}")
    print(f"segments={len(result['segments'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
