function ErrorMessage({ message = '' }) {
  if (!message) {
    return null
  }

  return (
    <section className="error-message" role="alert">
      <div className="error-message__icon" aria-hidden="true">
        !
      </div>

      <div className="error-message__content">
        <h2>Une erreur est survenue</h2>
        <p>{message}</p>
      </div>
    </section>
  )
}

export default ErrorMessage
