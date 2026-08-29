import axios from 'axios'

// Set VITE_API_URL in a .env file. Falls back to local Django dev server.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Sends a message/URL to the backend for scam-risk analysis.
 * Expected response shape from Django:
 * {
 *   risk_level: "HIGH" | "MEDIUM" | "LOW",
 *   score: 0-100,
 *   reasons: string[],
 *   matched_campaign: string | null,
 *   recommendation: string
 * }
 */
export async function analyzeMessage(content) {
  const { data } = await client.post('/api/analyze/', { content })
  return data
}

/**
 * Submits a confirmed scam report to help grow the campaign database.
 */
export async function reportScam(content, category) {
  const { data } = await client.post('/api/report/', { content, category })
  return data
}

/**
 * Fetches trending scam categories/campaigns for the dashboard.
 * Expected response shape:
 * { categories: [{ name: string, count: number }], total_submissions: number, total_scams_caught: number }
 */
export async function getTrending() {
  const { data } = await client.get('/api/trending/')
  return data
}

export default client
