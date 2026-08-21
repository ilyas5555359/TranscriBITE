function SummaryViewer({ summary = '' }) {
  return (
    <section className="summary-viewer">
      <div className="summary-viewer__header">
        <div>
          <h2>Résumé</h2>
          <p>Synthèse du contenu transcrit</p>
        </div>
      </div>

      <div className="summary-viewer__content">
        {summary ? (
          <p>{summary}</p>
        ) : (
          <p className="summary-viewer__empty">
            Le résumé apparaîtra ici après le traitement.
          </p>
        )}
      </div>
    </section>
  )
}

export default SummaryViewer
