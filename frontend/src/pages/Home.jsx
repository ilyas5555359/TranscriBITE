import { useState } from 'react'
import Header from '../components/Header'
import LanguageSelector from '../components/LanguageSelector'
import FileUploader from '../components/FileUploader'
import FileInformation from '../components/FileInformation'
import MediaPreview from '../components/MediaPreview'
import StartProcessingButton from '../components/StartProcessingButton'
import ProgressTracker from '../components/ProgressTracker'
import TranscriptViewer from '../components/TranscriptViewer'
import LiveTranscription from '../components/LiveTranscription'
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
  const [mode, setMode] = useState('file')
  const [selectedFile, setSelectedFile] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [transcriptSegments, setTranscriptSegments] = useState([])
  const [mediaCurrentTime, setMediaCurrentTime] = useState(null)
  const [summary, setSummary] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('auto')
  const [summaryLength, setSummaryLength] = useState('normal')
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

  const resetResults = () => {
    setError('')
    setTranscript('')
    setTranscriptSegments([])
    setMediaCurrentTime(null)
    setSummary('')
    setFileId('')
    setProgress(0)
    setProgressMessage('')
  }

  const handleFileSelected = (file) => {
    setSelectedFile(file)
    setFileId('')
    setError('')
    setTranscript('')
    setTranscriptSegments([])
    setMediaCurrentTime(null)
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
      let process = await startProcess(
        upload.file_id,
        selectedLanguage,
        summaryLength,
      )
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
      setTranscriptSegments(transcription.segments ?? [])
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
          summaryLength,
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
            <div className="mode-switcher" role="tablist" aria-label="Mode de transcription">
              <button
                type="button"
                className={`mode-switcher__button${mode === 'live' ? ' mode-switcher__button--active' : ''}`}
                role="tab"
                aria-selected={mode === 'live'}
                onClick={() => { resetResults(); setMode('live') }}
              >
                Parler en direct
              </button>
              <button
                type="button"
                className={`mode-switcher__button${mode === 'file' ? ' mode-switcher__button--active' : ''}`}
                role="tab"
                aria-selected={mode === 'file'}
                onClick={() => { resetResults(); setMode('file') }}
              >
                Importer un fichier
              </button>
            </div>

            <h1>{mode === 'live' ? 'Transcription live' : 'Importer un fichier'}</h1>

            <p>{mode === 'live'
              ? 'Parlez dans votre microphone pour transcrire votre voix et générer un résumé.'
              : 'Importez un fichier audio ou vidéo pour lancer la transcription et son résumé.'}
            </p>

            <LanguageSelector
              value={selectedLanguage}
              onChange={setSelectedLanguage}
            />

            <div className="summary-length-selector">
              <label htmlFor="summary-length">Longueur du résumé</label>
              <select
                id="summary-length"
                value={summaryLength}
                onChange={(event) => setSummaryLength(event.target.value)}
              >
                <option value="short">Très court</option>
                <option value="normal">Normal</option>
                <option value="long">Long</option>
              </select>
            </div>

            {mode === 'live' ? (
              <LiveTranscription
                language={selectedLanguage}
                summaryLength={summaryLength}
                onTranscriptChange={setTranscript}
                onSummaryChange={setSummary}
              />
            ) : (
              <>
                <FileUploader onFileSelected={handleFileSelected} />
                <FileInformation file={selectedFile} />
                <MediaPreview
                  file={selectedFile}
                  onTimeUpdate={setMediaCurrentTime}
                />
                <StartProcessingButton
                  disabled={!selectedFile}
                  onStart={handleStart}
                />
              </>
            )}

            <ErrorMessage message={error} />

            {mode === 'file' && (
              <ProgressTracker
                visible={processing || progress > 0}
                progress={progress}
                message={progressMessage}
              />
            )}

          </div>

          <div className="workspace-right">
            <TranscriptViewer
              transcript={transcript}
              segments={transcriptSegments}
              currentTime={mediaCurrentTime}
            />

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
