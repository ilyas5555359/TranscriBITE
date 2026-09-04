import { useEffect, useMemo } from 'react'

function MediaPreview({ file, onTimeUpdate }) {
  const mediaUrl = useMemo(
    () => (file ? URL.createObjectURL(file) : ''),
    [file],
  )

  useEffect(() => {
    if (!mediaUrl) {
      return undefined
    }

    return () => URL.revokeObjectURL(mediaUrl)
  }, [mediaUrl])

  if (!file || !mediaUrl) {
    return null
  }

  const isVideo = file.type.startsWith('video/')
  const MediaElement = isVideo ? 'video' : 'audio'

  return (
    <section className="media-preview">
      <div className="media-preview__header">
        <div>
          <h2>Écouter le fichier</h2>
          <p>Vous pouvez écouter le média pendant sa transcription.</p>
        </div>
        <span className="media-preview__type">{isVideo ? 'Vidéo' : 'Audio'}</span>
      </div>

      <MediaElement
        className="media-preview__player"
        src={mediaUrl}
        controls
        preload="metadata"
        onTimeUpdate={(event) => onTimeUpdate?.(event.currentTarget.currentTime)}
      >
        Votre navigateur ne prend pas en charge la lecture de ce média.
      </MediaElement>
    </section>
  )
}

export default MediaPreview
