function LanguageSelector() {
  return (
    <div className="language-selector">
      <label htmlFor="language">Langue</label>

      <select id="language" name="language" defaultValue="auto">
        <option value="auto">Détection automatique</option>
        <option value="fr">Français</option>
        <option value="en">English</option>
      </select>
    </div>
  )
}

export default LanguageSelector
