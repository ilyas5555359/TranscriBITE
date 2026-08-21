function TranscriptionInformation({
  language = null,
  duration = null,
  model = null,
  status = null,
}) {
  const hasInformation =
    language || duration || model || status

  if (!hasInformation) {
    return null
  }

  return (
    <section className="transcription-information">
      <h2>Informations</h2>

      <dl>
        {language && (
          <div className="transcription-information__row">
            <dt>Langue</dt>
            <dd>{language}</dd>
          </div>
        )}

        {duration && (
          <div className="transcription-information__row">
            <dt>Durée</dt>
            <dd>{duration}</dd>
          </div>
        )}

        {model && (
          <div className="transcription-information__row">
            <dt>Modèle</dt>
            <dd>{model}</dd>
          </div>
        )}

        {status && (
          <div className="transcription-information__row">
            <dt>Statut</dt>
            <dd>{status}</dd>
          </div>
        )}
      </dl>
    </section>
  )
}

export default TranscriptionInformation
