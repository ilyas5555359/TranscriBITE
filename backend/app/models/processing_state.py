import json
from uuid import UUID
from pathlib import Path

from app.config import CACHE_FOLDER
from app.schemas.process_schema import ProcessingStatus


class ProcessingState:

    def __init__(self, state_file: str | Path | None = None):
        self._state_file = Path(state_file) if state_file else (
            Path(CACHE_FOLDER) / "processing_states.json"
        )
        self._processing_states: dict[UUID, ProcessingStatus] = self._load()

    def _load(self) -> dict[UUID, ProcessingStatus]:
        if not self._state_file.is_file():
            return {}
        try:
            data = json.loads(self._state_file.read_text(encoding="utf-8"))
            return {
                UUID(file_id): ProcessingStatus.model_validate(value)
                for file_id, value in data.items()
            }
        except (OSError, ValueError, TypeError):
            return {}

    def _save(self) -> None:
        try:
            self._state_file.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                str(file_id): state.model_dump(mode="json")
                for file_id, state in self._processing_states.items()
                if isinstance(state, ProcessingStatus)
            }
            temporary_file = self._state_file.with_suffix(".tmp")
            temporary_file.write_text(
                json.dumps(payload, ensure_ascii=False),
                encoding="utf-8",
            )
            temporary_file.replace(self._state_file)
        except (OSError, TypeError, ValueError):
            pass

    async def add_processing(
        self,
        file_id: UUID,
        processing: ProcessingStatus
    ) -> None:

        self._processing_states[file_id] = processing
        self._save()

    async def get_processing(
        self,
        file_id: UUID
    ) -> ProcessingStatus | None:

        return self._processing_states.get(file_id)

    async def remove_processing(
        self,
        file_id: UUID
    ) -> None:

        self._processing_states.pop(
            file_id,
            None
        )
        self._save()

    async def exists(
        self,
        file_id: UUID
    ) -> bool:

        return file_id in self._processing_states


processing_state = ProcessingState()
