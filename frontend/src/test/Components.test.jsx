import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import DownloadButtons from '../components/DownloadButtons'
import ProgressTracker from '../components/ProgressTracker'

vi.mock('../services/api', () => ({
  downloadResult: vi.fn(),
}))

afterEach(() => cleanup())

describe('processing components', () => {
  it('disables downloads when no file is selected', () => {
    render(<DownloadButtons />)

    expect(screen.getByRole('button', {
      name: 'Télécharger la transcription (TXT)',
    })).toBeDisabled()
    expect(screen.getByRole('button', {
      name: 'Télécharger les données (JSON)',
    })).toBeDisabled()
  })

  it('displays the current progress and message', () => {
    render(
      <ProgressTracker
        visible
        progress={42}
        message="Transcription en cours"
      />,
    )

    expect(screen.getByRole('progressbar')).toHaveAttribute(
      'aria-valuenow',
      '42',
    )
    expect(screen.getByText('Transcription en cours')).toBeInTheDocument()
  })
})
