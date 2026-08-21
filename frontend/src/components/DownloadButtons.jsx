function DownloadButtons({
  transcript = '',
  summary = '',
}) {
  const downloadText = (content, filename) => {
    if (!content) {
      return
    }

    const blob = new Blob([content], {
      type: 'text/plain;charset=utf-8',
    })

    const url = URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = filename

    document.body.appendChild(link)
    link.click()
    link.remove()

    URL.revokeObjectURL(url)
  }

  return (
    <section className="download-buttons">
      <h2>Télécharger</h2>

      <div className="download-buttons__actions">
        <button
          type="button"
          className="button button--secondary"
          disabled={!transcript}
          onClick={() =>
            downloadText(transcript, 'transcription.txt')
          }
        >
          Télécharger la transcription
        </button>

        <button
          type="button"
          className="button button--secondary"
          disabled={!summary}
          onClick={() =>
            downloadText(summary, 'resume.txt')
          }
        >
          Télécharger le résumé
        </button>
      </div>
    </section>
  )
}

export default DownloadButtons
