import { useState } from 'react'
import { downloadResult } from '../services/api'

function DownloadButtons({ fileId = '', onError }) {
  const [downloading, setDownloading] = useState(false)

  const handleDownload = async () => {
    if (!fileId || downloading) {
      return
    }

    setDownloading(true)

    try {
      await downloadResult(fileId, 'pdf')
    } catch (error) {
      onError?.(error.message || 'Le téléchargement a échoué.')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <section className="download-buttons">
      <h2>Exporter</h2>

      <div className="download-buttons__actions">
        <button
          type="button"
          className="button button--secondary"
          disabled={!fileId || downloading}
          onClick={handleDownload}
        >
          {downloading ? 'Génération…' : 'Télécharger le rapport (PDF)'}
        </button>
      </div>
    </section>
  )
}

export default DownloadButtons
