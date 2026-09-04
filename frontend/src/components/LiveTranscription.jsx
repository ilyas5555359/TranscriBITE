import { useEffect, useRef, useState } from 'react'
import { generateLiveSummary } from '../services/api'

const SPEECH_LANGUAGES = {
  auto: 'fr-FR',
  fr: 'fr-FR',
  en: 'en-US',
  ar: 'ar-SA',
}

function LiveTranscription({
  language = 'auto',
  summaryLength = 'normal',
  onTranscriptChange,
  onSummaryChange,
}) {
  const recognitionRef = useRef(null)
  const [isListening, setIsListening] = useState(false)
  const [finalTranscript, setFinalTranscript] = useState('')
  const [interimTranscript, setInterimTranscript] = useState('')
  const [error, setError] = useState('')
  const [summarizing, setSummarizing] = useState(false)
  const SpeechRecognition = window.SpeechRecognition
    || window.webkitSpeechRecognition
  const isSupported = Boolean(SpeechRecognition)

  useEffect(() => {
    if (!SpeechRecognition) {
      return undefined
    }

    const recognition = new SpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = SPEECH_LANGUAGES[language] || SPEECH_LANGUAGES.auto

    recognition.onresult = (event) => {
      let nextFinalTranscript = ''
      let nextInterimTranscript = ''

      for (let index = event.resultIndex; index < event.results.length; index += 1) {
        const text = event.results[index][0].transcript
        if (event.results[index].isFinal) {
          nextFinalTranscript += `${text} `
        } else {
          nextInterimTranscript += text
        }
      }

      if (nextFinalTranscript) {
        setFinalTranscript((current) => `${current} ${nextFinalTranscript}`.trim())
      }
      setInterimTranscript(nextInterimTranscript.trim())
    }

    recognition.onerror = (event) => {
      if (event.error !== 'aborted') {
        setError(`Erreur de reconnaissance vocale : ${event.error}`)
      }
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      recognition.abort()
      recognitionRef.current = null
    }
  }, [SpeechRecognition, language])

  useEffect(() => {
    onTranscriptChange?.(`${finalTranscript} ${interimTranscript}`.trim())
  }, [finalTranscript, interimTranscript, onTranscriptChange])

  const startListening = () => {
    if (!recognitionRef.current || isListening) {
      return
    }

    setError('')
    setInterimTranscript('')
    setIsListening(true)
    recognitionRef.current.start()
  }

  const stopListening = () => {
    recognitionRef.current?.stop()
    setIsListening(false)
  }

  const clearTranscript = () => {
    setFinalTranscript('')
    setInterimTranscript('')
    setError('')
    onTranscriptChange?.('')
    onSummaryChange?.('')
  }

  const handleSummary = async () => {
    if (!finalTranscript || summarizing) {
      return
    }

    setSummarizing(true)
    setError('')
    try {
      const result = await generateLiveSummary(
        finalTranscript,
        language === 'auto' ? 'fr' : language,
        summaryLength,
      )
      onSummaryChange?.(result.data?.summary ?? '')
    } catch (requestError) {
      setError(requestError.message || 'Le résumé live a échoué.')
    } finally {
      setSummarizing(false)
    }
  }

  const interimWords = interimTranscript.split(/\s+/).filter(Boolean)
  const currentWord = interimWords.pop() || ''
  const previousInterimWords = interimWords.join(' ')

  return (
    <section className="live-transcription" dir={language === 'ar' ? 'rtl' : 'ltr'}>
      <div className="live-transcription__header">
        <div>
          <h2>Transcription live</h2>
          <p>Les mots en cours de reconnaissance apparaissent en surbrillance.</p>
        </div>
        <span className={`live-transcription__status${isListening ? ' live-transcription__status--active' : ''}`}>
          {isListening ? 'En écoute' : 'En pause'}
        </span>
      </div>

      {!isSupported ? (
        <p className="live-transcription__notice">
          La transcription live n’est pas disponible dans ce navigateur. Utilisez Chrome ou Edge.
        </p>
      ) : (
        <>
          <div className="live-transcription__actions">
            <button
              type="button"
              className="button button--primary"
              disabled={isListening}
              onClick={startListening}
            >
              Démarrer le direct
            </button>
            <button
              type="button"
              className="button button--secondary"
              disabled={!isListening}
              onClick={stopListening}
            >
              Arrêter
            </button>
            <button
              type="button"
              className="button button--secondary"
              disabled={!finalTranscript && !interimTranscript}
              onClick={clearTranscript}
            >
              Effacer
            </button>
            <button
              type="button"
              className="button button--secondary"
              disabled={!finalTranscript || summarizing}
              onClick={handleSummary}
            >
              {summarizing ? 'Résumé en cours…' : 'Générer le résumé'}
            </button>
          </div>

          <div className="live-transcription__content" aria-live="polite">
            {finalTranscript || interimTranscript ? (
              <>
                <span>{finalTranscript} </span>
                <span>{previousInterimWords} </span>
                {currentWord && (
                  <mark className="live-transcription__current-word">{currentWord}</mark>
                )}
              </>
            ) : (
              <span className="live-transcription__empty">
                Lancez le direct puis commencez à parler.
              </span>
            )}
          </div>
        </>
      )}

      {error && <p className="live-transcription__error" role="alert">{error}</p>}
    </section>
  )
}

export default LiveTranscription
