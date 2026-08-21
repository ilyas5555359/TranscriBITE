import { useRef, useState } from 'react'

function FileUploader({ onFileSelected }) {
  const inputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFile = (file) => {
    if (!file) {
      return
    }

    onFileSelected(file)
  }

  const handleInputChange = (event) => {
    const file = event.target.files?.[0]

    handleFile(file)
  }

  const handleDrop = (event) => {
    event.preventDefault()
    setIsDragging(false)

    const file = event.dataTransfer.files?.[0]

    handleFile(file)
  }

  const handleDragOver = (event) => {
    event.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (event) => {
    event.preventDefault()
    setIsDragging(false)
  }

  const handleBrowse = () => {
    inputRef.current?.click()
  }

  return (
    <div className="file-uploader">
      <div
        className={`drop-zone ${isDragging ? 'drop-zone--dragging' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <p className="drop-zone__title">
          Déposez votre fichier audio ou vidéo ici
        </p>

        <p className="drop-zone__separator">ou</p>

        <button
          type="button"
          className="button button--primary"
          onClick={handleBrowse}
        >
          Choisir un fichier
        </button>

        <input
          ref={inputRef}
          type="file"
          className="file-input"
          onChange={handleInputChange}
          accept="audio/*,video/*"
        />
      </div>
    </div>
  )
}

export default FileUploader
