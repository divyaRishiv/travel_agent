import { useState } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    destination: '',
    nationality: '',
    dates: '',
    purpose: 'Tourism'
  })
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/evaluate-travel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      
      const data = await response.json()
      
      if (data.status === 'error') {
        setError(data.error_message)
      } else {
        setResult(data.visa_checklist)
      }
    } catch (err) {
      setError('Failed to connect to the agent. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="background-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
      </div>
      
      <div className="main-card">
        <header className="header">
          <h1>Travel AI Co-pilot</h1>
          <p>Plan your journey securely and effortlessly.</p>
        </header>

        <div className="content">
          <form className="glass-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="destination">Destination</label>
              <input 
                type="text" 
                id="destination"
                name="destination" 
                value={formData.destination} 
                onChange={handleChange} 
                placeholder="e.g. Japan"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="nationality">Nationality</label>
              <input 
                type="text" 
                id="nationality"
                name="nationality" 
                value={formData.nationality} 
                onChange={handleChange} 
                placeholder="e.g. American"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="dates">Travel Dates</label>
              <input 
                type="text" 
                id="dates"
                name="dates" 
                value={formData.dates} 
                onChange={handleChange} 
                placeholder="e.g. Oct 10 - Oct 25"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="purpose">Purpose of Travel</label>
              <select id="purpose" name="purpose" value={formData.purpose} onChange={handleChange}>
                <option value="Tourism">Tourism</option>
                <option value="Business">Business</option>
                <option value="Transit">Transit</option>
                <option value="Study">Study</option>
              </select>
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? <span className="loader"></span> : 'Generate Checklist'}
            </button>
          </form>

          <div className="result-section">
            {error && (
              <div className="alert error">
                <span className="icon">⚠️</span>
                <p>{error}</p>
              </div>
            )}

            {result && (
              <div className="checklist-card">
                <h2>Your Visa Checklist</h2>
                <div className="markdown-content">
                  {/* Basic parsing for demonstration. In a real app, use react-markdown */}
                  {result.split('\n').map((line, i) => {
                    if (line.startsWith('###')) return <h3 key={i}>{line.replace('###', '').trim()}</h3>;
                    if (line.startsWith('**')) {
                      const [bold, rest] = line.split('**').filter(Boolean);
                      return <p key={i}><strong>{bold}</strong> {rest}</p>;
                    }
                    if (line.startsWith('*')) return <li key={i}>{line.replace('*', '').trim()}</li>;
                    return <p key={i}>{line}</p>;
                  })}
                </div>
              </div>
            )}
            
            {!result && !error && !loading && (
              <div className="empty-state">
                <div className="icon-placeholder">🌍</div>
                <p>Fill out the form to let the AI agent analyze your requirements.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
