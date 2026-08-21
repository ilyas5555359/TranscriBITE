function TranscriptViewer({ transcript = '' }) {
  return (
    <section className="transcript-viewer">
      <div className="transcript-viewer__header">
        <div>
          <h2>Transcription</h2>
          <p>Résultat de la transcription audio</p>
        </div>

        <button
          type="button"
          className="button button--secondary"
          disabled={!transcript}
          onClick={() => navigator.clipboard.writeText(transcript)}
        >
          Copier
        </button>
      </div>

      <div className="transcript-viewer__content">
        {transcript ? (
          <p>{transcript}</p>
        ) : (
          <p className="transcript-viewer__empty">
            La transcription apparaîtra ici après le traitement du fichier.
          </p>
        )}
      </div>
    </section>
  )
}

export default TranscriptViewer
