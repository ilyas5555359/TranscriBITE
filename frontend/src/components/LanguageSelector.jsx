function LanguageSelector({ value = 'auto', onChange }) {
  return (
    <div className="language-selector">
      <label htmlFor="language">Langue</label>

      <select
        id="language"
        name="language"
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
      >
        <option value="auto">Détection automatique</option>
        <option value="fr">Français</option>
        <option value="en">English</option>
        <option value="ar">العربية</option>
      </select>
    </div>
  )
}

export default LanguageSelector
