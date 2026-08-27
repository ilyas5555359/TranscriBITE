/**
 * Service d'appels HTTP vers le backend FastAPI.
 * Base URL : http://localhost:8000
 */

const API_BASE = 'http://localhost:8000'

/**
 * Upload un fichier audio/vidéo.
 * @param {File} file
 * @returns {Promise<object>} { success, file_id, original_filename, ... }
 */
export async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE}/upload/`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `Erreur upload (${response.status})`)
  }

  return response.json()
}

/**
 * Lancer le traitement complet d'un fichier.
 * @param {string} fileId - UUID du fichier
 * @returns {Promise<object>}
 */
export async function startProcess(fileId, language = 'auto') {
  const response = await fetch(
    `${API_BASE}/process/start?file_id=${fileId}&language=${language}`,
    { method: 'POST' },
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `Erreur process (${response.status})`)
  }

  return response.json()
}

/**
 * Récupérer la progression du traitement.
 * @param {string} fileId - UUID du fichier
 * @returns {Promise<object>}
 */
export async function getProgress(fileId) {
  const response = await fetch(`${API_BASE}/progress/${fileId}`)

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `Erreur progress (${response.status})`)
  }

  return response.json()
}

/**
 * Générer un résumé via Ollama.
 * @param {string} jobId
 * @param {string} text - Texte transcrit
 * @param {string} language - Code langue (fr, en, auto)
 * @returns {Promise<object>}
 */
export async function generateSummary(jobId, text, language = 'fr') {
  const response = await fetch(`${API_BASE}/summary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      job_id: jobId,
      text,
      language,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `Erreur summary (${response.status})`)
  }

  return response.json()
}

/**
 * Vérifier l'état de santé du backend.
 * @returns {Promise<object>}
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE}/health`)

  if (!response.ok) {
    throw new Error(`Backend inaccessible (${response.status})`)
  }

  return response.json()
}

/**
 * Télécharger un résultat ou le rapport complet (TXT, JSON ou PDF).
 * @param {string} fileId
 * @param {string} format - "txt" ou "json"
 */
export async function downloadResult(fileId, format) {
  const response = await fetch(
    `${API_BASE}/download/${fileId}/${format}`,
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `Erreur download (${response.status})`)
  }

  const blob = await response.blob()
  const url = URL.createObjectURL(blob)

  const extension = format === 'json' ? 'json' : format === 'pdf' ? 'pdf' : 'txt'
  const link = document.createElement('a')
  link.href = url
  link.download = format === 'pdf' ? 'rapport-transcription.pdf' : `transcription.${extension}`
  document.body.appendChild(link)
  link.click()
  link.remove()

  URL.revokeObjectURL(url)
}
