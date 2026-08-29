import './RiskGauge.css'

const RISK_CONFIG = {
  HIGH: { color: 'var(--risk-high)', label: 'High Risk', angle: 152 },
  MEDIUM: { color: 'var(--risk-medium)', label: 'Medium Risk', angle: 90 },
  LOW: { color: 'var(--risk-low)', label: 'Low Risk', angle: 28 },
}

// Semicircle gauge: 0 = far left (-90deg), 100 = far right (+90deg)
function scoreToRotation(score) {
  const clamped = Math.max(0, Math.min(100, score))
  return -90 + (clamped / 100) * 180
}

export default function RiskGauge({ riskLevel, score }) {
  const config = RISK_CONFIG[riskLevel] || RISK_CONFIG.MEDIUM
  const rotation = scoreToRotation(score)

  return (
    <div className="risk-gauge" style={{ '--gauge-color': config.color }}>
      <svg viewBox="0 0 200 110" className="risk-gauge-svg">
        <path
          d="M 10 100 A 90 90 0 0 1 190 100"
          fill="none"
          stroke="var(--border-bright)"
          strokeWidth="14"
          strokeLinecap="round"
        />
        <path
          d="M 10 100 A 90 90 0 0 1 190 100"
          fill="none"
          stroke="var(--gauge-color)"
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray="283"
          strokeDashoffset={283 - (Math.max(0, Math.min(100, score)) / 100) * 283}
          className="risk-gauge-arc"
        />
        <g className="risk-gauge-needle" style={{ transform: `rotate(${rotation}deg)` }}>
          <line x1="100" y1="100" x2="100" y2="28" stroke="var(--ink)" strokeWidth="3" strokeLinecap="round" />
          <circle cx="100" cy="100" r="7" fill="var(--ink)" />
        </g>
      </svg>
      <div className="risk-gauge-readout">
        <span className="risk-gauge-score">{Math.round(score)}</span>
        <span className="risk-gauge-label">{config.label}</span>
      </div>
    </div>
  )
}
