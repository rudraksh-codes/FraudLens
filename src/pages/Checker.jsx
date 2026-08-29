import { useState } from 'react'
import { analyzeMessage } from '../api'
import RiskGauge from '../components/RiskGauge'
import './Checker.css'

const EXAMPLE = `Dear Customer, your KYC has expired. Update immediately at http://kyc-verify-secure.in or your account will be suspended within 24 hours.`

const RISK_COPY = {
  HIGH: {
    heading: 'This looks like a scam',
    guidance: 'Do not click any links, share OTPs, or make any payment. Block and report the sender.',
  },
  MEDIUM: {
    heading: 'Proceed with caution',
    guidance: 'Some suspicious signals found. Verify through an official channel before acting.',
  },
  LOW: {
    heading: 'No major red flags found',
    guidance: 'This message looks relatively safe, but always stay alert with unknown senders.',
  },
}

export default function Checker() {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!content.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeMessage(content.trim())
      setResult(data)
    } catch (err) {
      setError(
        err.response
          ? 'The scan could not complete. Please try again in a moment.'
          : 'Could not reach the server. Check that the backend is running.',
      )
    } finally {
      setLoading(false)
    }
  }

  function loadExample() {
    setContent(EXAMPLE)
    setResult(null)
    setError(null)
  }

  function reset() {
    setContent('')
    setResult(null)
    setError(null)
  }

  const copy = result ? RISK_COPY[result.risk_level] || RISK_COPY.MEDIUM : null

  return (
    <section className="checker">
      <div className="checker-intro">
        <span className="checker-eyebrow">Message · SMS · WhatsApp · Email · URL</span>
        <h1 className="checker-title">Paste it before you trust it.</h1>
        <p className="checker-subtitle">
          Sentinel scans the text for the signals real scam campaigns leave behind — urgency, credential
          requests, suspicious links — and tells you what to do next.
        </p>
      </div>

      <form className="checker-panel" onSubmit={handleSubmit}>
        <label htmlFor="message-input" className="checker-panel-label">
          Paste the message or URL
        </label>
        <textarea
          id="message-input"
          className="checker-textarea"
          placeholder="e.g. Dear Customer, your account will be blocked. Click here to verify..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={7}
        />

        <div className="checker-actions">
          <button type="button" className="btn btn-ghost" onClick={loadExample}>
            Try an example
          </button>
          <div className="checker-actions-right">
            {(content || result) && (
              <button type="button" className="btn btn-ghost" onClick={reset}>
                Clear
              </button>
            )}
            <button type="submit" className="btn btn-primary" disabled={loading || !content.trim()}>
              {loading ? 'Scanning…' : 'Check message'}
            </button>
          </div>
        </div>
      </form>

      {loading && (
        <div className="checker-scanning" role="status" aria-live="polite">
          <span className="checker-scanning-bar" />
          <span>Running rule checks and matching known campaigns…</span>
        </div>
      )}

      {error && <div className="checker-error">{error}</div>}

      {result && !loading && (
        <div className="checker-result" aria-live="polite">
          <div className="checker-result-top">
            <RiskGauge riskLevel={result.risk_level} score={result.score ?? 0} />
            <div className="checker-result-summary">
              <h2 className="checker-result-heading">{copy.heading}</h2>
              <p className="checker-result-guidance">{result.recommendation || copy.guidance}</p>
              {result.matched_campaign && (
                <div className="checker-campaign-tag">
                  Matches known campaign: <strong>{result.matched_campaign}</strong>
                </div>
              )}
            </div>
          </div>

          {Array.isArray(result.reasons) && result.reasons.length > 0 && (
            <div className="checker-reasons">
              <h3 className="checker-reasons-heading">Why we flagged this</h3>
              <ul className="checker-reasons-list">
                {result.reasons.map((reason, i) => (
                  <li key={i}>{reason}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </section>
  )
}
