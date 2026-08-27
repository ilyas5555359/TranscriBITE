import { useState } from 'react'
import { downloadResult } from '../services/api'

function DownloadButtons({ fileId = '', onError }) {
  const [downloadingFormat, setDownloadingFormat] = useState('')

  const handleDownload = async (format) => {
    if (!fileId || downloadingFormat) {
      return
    }

    setDownloadingFormat(format)

    try {
      await downloadResult(fileId, format)
    } catch (error) {
      onError?.(error.message || 'Le téléchargement a échoué.')
    } finally {
      setDownloadingFormat('')
    }
  }

  return (
    <section className="download-buttons">
      <h2>Télécharger</h2>

      <div className="download-buttons__actions">
        <button
          type="button"
          className="button button--secondary"
          disabled={!fileId || Boolean(downloadingFormat)}
          onClick={() => handleDownload('txt')}
        >
          {downloadingFormat === 'txt'
            ? 'Téléchargement…'
            : 'Télécharger la transcription (TXT)'}
        </button>

        <button
          type="button"
          className="button button--secondary"
          disabled={!fileId || Boolean(downloadingFormat)}
          onClick={() => handleDownload('json')}
        >
          {downloadingFormat === 'json'
            ? 'Téléchargement…'
            : 'Télécharger les données (JSON)'}
        </button>

        <button
          type="button"
          className="button button--secondary"
          disabled={!fileId || Boolean(downloadingFormat)}
          onClick={() => handleDownload('pdf')}
        >
          {downloadingFormat === 'pdf'
            ? 'Téléchargement…'
            : 'Télécharger le rapport (PDF)'}
        </button>
      </div>
    </section>
  )
}

export default DownloadButtons
