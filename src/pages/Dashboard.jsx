import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { getTrending } from '../api'
import './Dashboard.css'

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div className="dashboard-tooltip">
      <div className="dashboard-tooltip-label">{label}</div>
      <div className="dashboard-tooltip-value">{payload[0].value} reports</div>
    </div>
  )
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await getTrending()
        if (!cancelled) setData(res)
      } catch (err) {
        if (!cancelled) setError('Could not load trending data. Is the backend running?')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <section className="dashboard">
      <div className="dashboard-header">
        <span className="checker-eyebrow">Live campaign intelligence</span>
        <h1 className="dashboard-title">What's spreading right now</h1>
        <p className="checker-subtitle">
          Every message checked on Sentinel quietly strengthens this picture of active scam campaigns.
        </p>
      </div>

      {loading && <div className="dashboard-state">Loading trends…</div>}
      {error && <div className="checker-error">{error}</div>}

      {data && !loading && (
        <>
          <div className="dashboard-stats">
            <div className="dashboard-stat-card">
              <span className="dashboard-stat-value">{data.total_submissions ?? '—'}</span>
              <span className="dashboard-stat-label">Messages checked</span>
            </div>
            <div className="dashboard-stat-card">
              <span className="dashboard-stat-value" style={{ color: 'var(--risk-high)' }}>
                {data.total_scams_caught ?? '—'}
              </span>
              <span className="dashboard-stat-label">Scams caught</span>
            </div>
            <div className="dashboard-stat-card">
              <span className="dashboard-stat-value">{data.categories?.length ?? '—'}</span>
              <span className="dashboard-stat-label">Active campaign types</span>
            </div>
          </div>

          <div className="dashboard-chart-panel">
            <h3 className="checker-reasons-heading">Top scam categories</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.categories || []} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid stroke="var(--border)" vertical={false} />
                <XAxis
                  dataKey="name"
                  tick={{ fill: 'var(--ink-dim)', fontSize: 12 }}
                  axisLine={{ stroke: 'var(--border)' }}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: 'var(--ink-dim)', fontSize: 12 }}
                  axisLine={{ stroke: 'var(--border)' }}
                  tickLine={false}
                />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--bg-void)' }} />
                <Bar dataKey="count" fill="var(--accent)" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </section>
  )
}
