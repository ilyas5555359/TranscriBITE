from uuid import UUID

from app.schemas.process_schema import ProcessingStatus


class ProcessingState:

    def __init__(self):

        self._processing_states: dict[
            UUID,
            ProcessingStatus
        ] = {}

    async def add_processing(
        self,
        file_id: UUID,
        processing: ProcessingStatus
    ) -> None:

        self._processing_states[file_id] = processing

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

    async def exists(
        self,
        file_id: UUID
    ) -> bool:

        return file_id in self._processing_states


processing_state = ProcessingState()
