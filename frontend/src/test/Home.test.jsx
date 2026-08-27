import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import Home from '../pages/Home'
import * as api from '../services/api'

vi.mock('../services/api', () => ({
  generateSummary: vi.fn(),
  getProgress: vi.fn(),
  startProcess: vi.fn(),
  uploadFile: vi.fn(),
}))

const selectedFile = new File(['audio'], 'sample.wav', { type: 'audio/wav' })

function selectFile() {
  fireEvent.change(document.querySelector('input[type="file"]'), {
    target: { files: [selectedFile] },
  })
}

describe('Home workflow', () => {
  afterEach(() => {
    cleanup()
    vi.clearAllMocks()
  })

  it('keeps processing disabled until a file is selected', () => {
    render(<Home />)

    expect(screen.getByRole('button', {
      name: 'Commencer la transcription',
    })).toBeDisabled()
  })

  it('displays transcription and summary after successful processing', async () => {
    api.uploadFile.mockResolvedValue({ file_id: 'job-123' })
    api.startProcess.mockResolvedValue({
      processing: {
        progress_percentage: 100,
        transcription_result: {
          text: 'Bonjour TranscriBITE',
          language: 'fr',
        },
      },
    })
    api.generateSummary.mockResolvedValue({
      data: { summary: 'Résumé du test' },
    })

    render(<Home />)
    selectFile()
    fireEvent.click(screen.getByRole('button', {
      name: 'Commencer la transcription',
    }))

    expect(await screen.findByText('Bonjour TranscriBITE')).toBeInTheDocument()
    expect(await screen.findByText('Résumé du test')).toBeInTheDocument()
    expect(api.generateSummary).toHaveBeenCalledWith(
      'job-123',
      'Bonjour TranscriBITE',
      'fr',
    )
  })

  it('renders an API error after processing fails', async () => {
    api.uploadFile.mockRejectedValue(new Error('Backend indisponible'))

    render(<Home />)
    selectFile()
    fireEvent.click(screen.getByRole('button', {
      name: 'Commencer la transcription',
    }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Backend indisponible',
    )
    await waitFor(() => expect(api.startProcess).not.toHaveBeenCalled())
  })
})
