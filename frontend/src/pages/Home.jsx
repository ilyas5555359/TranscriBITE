import { useState } from 'react'
import Header from '../components/Header'
import LanguageSelector from '../components/LanguageSelector'
import FileUploader from '../components/FileUploader'
import FileInformation from '../components/FileInformation'
import StartProcessingButton from '../components/StartProcessingButton'
import ProgressTracker from '../components/ProgressTracker'
import TranscriptViewer from '../components/TranscriptViewer'
import SummaryViewer from '../components/SummaryViewer'
import TranscriptionInformation from '../components/TranscriptionInformation'
import DownloadButtons from '../components/DownloadButtons'
import ErrorMessage from '../components/ErrorMessage'
import Footer from '../components/Footer'
import {
  generateSummary,
  getProgress,
  startProcess,
  uploadFile,
} from '../services/api'

async function waitForProcessing(fileId, onProgress) {
  let result = await getProgress(fileId)

  while (!['Terminée', 'Échec'].includes(
    result.processing.current_status,
  )) {
    onProgress(result.processing)
    await new Promise((resolve) => setTimeout(resolve, 250))
    result = await getProgress(fileId)
  }

  onProgress(result.processing)
  return result
}

function Home() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [summary, setSummary] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('auto')
  const [fileId, setFileId] = useState('')
  const [progress, setProgress] = useState(0)
  const [progressMessage, setProgressMessage] = useState('')
  const [transcriptionInformation, setTranscriptionInformation] = useState({
    language: null,
    duration: null,
    model: null,
    status: null,
  })
  const [error, setError] = useState('')

  const handleFileSelected = (file) => {
    setSelectedFile(file)
    setFileId('')
    setError('')
    setTranscript('')
    setSummary('')
    setProgress(0)
    setProgressMessage('')
    setTranscriptionInformation({
      language: null,
      duration: null,
      model: null,
      status: null,
    })
  }

  const handleStart = async () => {
    if (!selectedFile || processing) {
      return
    }

    setProcessing(true)
    setError('')
    setTranscript('')
    setSummary('')
    setProgress(0)
    setProgressMessage('Envoi du fichier vers le serveur…')

    try {
      const upload = await uploadFile(selectedFile)
      setFileId(upload.file_id)

      setProgressMessage('Transcription en cours…')
      let process = await startProcess(upload.file_id, selectedLanguage)
      if (process.processing.current_status === 'En attente') {
        process = await waitForProcessing(upload.file_id, (current) => {
          setProgress(current.progress_percentage)
          setProgressMessage(`Étape : ${current.current_step}`)
        })
      }
      const transcription = process.processing.transcription_result

      if (!transcription?.text) {
        throw new Error('Le backend n’a retourné aucun texte transcrit.')
      }

      setTranscript(transcription.text)
      setProgress(process.processing.progress_percentage)
      setProgressMessage('Génération du résumé…')

      const language = selectedLanguage === 'auto'
        ? transcription.language
        : selectedLanguage
      const summary = process.processing.summary_result
      if (summary?.summary) {
        setSummary(summary.summary)
      } else {
        const summaryResult = await generateSummary(
          upload.file_id,
          transcription.text,
          language,
        )
        setSummary(summaryResult.data?.summary ?? '')
      }
      setProgress(100)
      setProgressMessage('Traitement terminé.')
      setTranscriptionInformation({
        language: transcription.language,
        duration: null,
        model: 'Faster-Whisper',
        status: 'Terminée',
      })
    } catch (requestError) {
      setProgressMessage('')
      setError(requestError.message || 'Une erreur inattendue est survenue.')
      setTranscriptionInformation((current) => ({
        ...current,
        status: 'Échec',
      }))
    } finally {
      setProcessing(false)
    }
  }

  return (
    <>
      <Header />

      <main className="home">
        <section className="workspace">
          <div className="workspace-left">
            <h1>Importer un fichier</h1>

            <p>
              Importez un fichier audio ou vidéo pour commencer la
              transcription.
            </p>

            <LanguageSelector
              value={selectedLanguage}
              onChange={setSelectedLanguage}
            />

            <FileUploader onFileSelected={handleFileSelected} />

            <FileInformation file={selectedFile} />

            <StartProcessingButton
              disabled={!selectedFile}
              onStart={handleStart}
            />

            <ErrorMessage message={error} />

            <ProgressTracker
              visible={processing || progress > 0}
              progress={progress}
              message={progressMessage}
            />

          </div>

          <div className="workspace-right">
            <TranscriptViewer transcript={transcript} />

            <SummaryViewer summary={summary} />

            <TranscriptionInformation
                language={transcriptionInformation.language}
                duration={transcriptionInformation.duration}
                model={transcriptionInformation.model}
                status={transcriptionInformation.status}
            />

            <DownloadButtons
              fileId={fileId}
              onError={setError}
            />

          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}

export default Home
