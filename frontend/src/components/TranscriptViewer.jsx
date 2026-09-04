function TranscriptViewer({ transcript = '', segments = [], currentTime = null }) {
  const renderTranscript = () => {
    if (!segments.length || currentTime === null) {
      return <p>{transcript}</p>
    }

    return (
      <p>
        {segments.map((segment, segmentIndex) => {
          const words = segment.text.trim().split(/\s+/).filter(Boolean)
          const isActiveSegment = currentTime >= segment.start
            && currentTime <= segment.end
          const segmentDuration = Math.max(segment.end - segment.start, 0.01)
          const elapsed = Math.min(Math.max(currentTime - segment.start, 0), segmentDuration)
          const activeWordIndex = isActiveSegment
            ? Math.min(words.length - 1, Math.floor((elapsed / segmentDuration) * words.length))
            : -1

          return (
            <span key={`${segment.start}-${segmentIndex}`}>
              {words.map((word, wordIndex) => (
                <span key={`${word}-${wordIndex}`}>
                  {segmentIndex > 0 || wordIndex > 0 ? ' ' : ''}
                  {isActiveSegment && wordIndex === activeWordIndex ? (
                    <mark className="transcript-viewer__current-word">{word}</mark>
                  ) : word}
                </span>
              ))}
            </span>
          )
        })}
      </p>
    )
  }

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
          renderTranscript()
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
