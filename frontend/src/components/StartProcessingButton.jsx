function StartProcessingButton({ disabled = false, onStart }) {
  const handleClick = () => {
    if (disabled) {
      return
    }

    onStart()
  }

  return (
    <div className="start-processing">
      <button
        type="button"
        className="button button--primary start-processing__button"
        disabled={disabled}
        onClick={handleClick}
      >
        Commencer la transcription
      </button>
    </div>
  )
}

export default StartProcessingButton
