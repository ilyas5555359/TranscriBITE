function formatFileSize(bytes) {
  if (bytes === 0) {
    return '0 octet'
  }

  const units = ['octets', 'Ko', 'Mo', 'Go']
  const index = Math.floor(Math.log(bytes) / Math.log(1024))
  const size = bytes / 1024 ** index

  return `${size.toFixed(index === 0 ? 0 : 2)} ${units[index]}`
}

function FileInformation({ file }) {
  if (!file) {
    return null
  }

  return (
    <section className="file-information">
      <h2>Fichier sélectionné</h2>

      <dl>
        <div className="file-information__row">
          <dt>Nom</dt>
          <dd>{file.name}</dd>
        </div>

        <div className="file-information__row">
          <dt>Type</dt>
          <dd>{file.type || 'Type inconnu'}</dd>
        </div>

        <div className="file-information__row">
          <dt>Taille</dt>
          <dd>{formatFileSize(file.size)}</dd>
        </div>
      </dl>
    </section>
  )
}

export default FileInformation
