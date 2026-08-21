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

function Home() {
  const [selectedFile, setSelectedFile] = useState(null)

    const handleStart = () => {
        console.log('Démarrage du traitement :', selectedFile)

        setProcessing(true)

        setTranscript(
            'Ceci est une transcription de démonstration générée par TranscriBITE. Elle sera remplacée plus tard par le résultat réel de Faster-Whisper.'
        )

        setSummary(
            'Résumé de démonstration : le fichier contient une présentation générale du contenu qui sera prochainement généré automatiquement par Ollama.'
        )

        setTranscriptionInformation({
            language: 'Français',
            duration: '03:42',
            model: 'Faster-Whisper',
            status: 'Terminée',
            })
    }

  const [processing, setProcessing] = useState(false)

  const [transcript, setTranscript] = useState('')

  const [summary, setSummary] = useState('')

  const [transcriptionInformation, setTranscriptionInformation] = useState({
  language: null,
  duration: null,
  model: null,
  status: null,
    }
  )

  const [error, setError] = useState('')

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

            <LanguageSelector />

            <FileUploader onFileSelected={setSelectedFile} />

            <FileInformation file={selectedFile} />

            <StartProcessingButton
              disabled={!selectedFile}
              onStart={handleStart}
            />

            <ErrorMessage message={error} />

            <ProgressTracker
            visible={processing}
            progress={65}
            message="Transcription en cours..."
            estimatedTime="01:42"
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
                transcript={transcript}
                summary={summary}
            />

          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}

export default Home
