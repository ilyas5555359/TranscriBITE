function ProgressTracker({
  progress = 0,
  message = 'En attente du traitement...',
  estimatedTime = null,
  visible = false,
}) {
  if (!visible) {
    return null
  }

  const safeProgress = Math.min(100, Math.max(0, progress))

  return (
    <section className="progress-tracker">
      <div className="progress-tracker__header">
        <h2>Progression</h2>
        <span>{safeProgress}%</span>
      </div>

      <div
        className="progress-bar"
        role="progressbar"
        aria-valuenow={safeProgress}
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div
          className="progress-bar__fill"
          style={{ width: `${safeProgress}%` }}
        />
      </div>

      <p className="progress-tracker__message">
        {message}
      </p>

      {estimatedTime && (
        <p className="progress-tracker__time">
          Temps estimé : {estimatedTime}
        </p>
      )}
    </section>
  )
}

export default ProgressTracker
