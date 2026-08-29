import './About.css'

const PIPELINE = [
  { step: 'Rules', detail: 'Checks for urgency, credential requests, suspicious URLs and domains' },
  { step: 'Campaign match', detail: 'Fuzzy-matches the message against known scam templates' },
  { step: 'Score', detail: 'Signals are weighted and combined into a LOW / MEDIUM / HIGH score' },
  { step: 'Explain', detail: 'An LLM turns the flagged signals into a plain-language reason' },
]

export default function About() {
  return (
    <section className="about">
      <span className="checker-eyebrow">How Sentinel works</span>
      <h1 className="about-title">Rules decide the risk. AI explains it.</h1>
      <p className="about-lead">
        Sentinel is built for the everyday moment before you click — a suspicious SMS, a WhatsApp
        forward, an email asking for your KYC. It does not use an AI model to guess whether something
        is a scam. A deterministic rule engine scores the message; a language model only translates
        that score into a reason a human can understand.
      </p>

      <div className="about-pipeline">
        {PIPELINE.map((item, i) => (
          <div className="about-pipeline-item" key={item.step}>
            <div className="about-pipeline-index">{String(i + 1).padStart(2, '0')}</div>
            <div>
              <h3 className="about-pipeline-step">{item.step}</h3>
              <p className="about-pipeline-detail">{item.detail}</p>
            </div>
            {i < PIPELINE.length - 1 && <div className="about-pipeline-connector" aria-hidden="true" />}
          </div>
        ))}
      </div>

      <div className="about-why">
        <h2 className="about-why-heading">Why it matters</h2>
        <p className="about-why-body">
          Scam messages in India increasingly follow campaigns — the same fake KYC or delivery-fee
          template reused across thousands of numbers. By recognising when a new message belongs to a
          known campaign, Sentinel gets more accurate the more people use it, without ever needing to
          store who sent or received a message.
        </p>
      </div>
    </section>
  )
}
