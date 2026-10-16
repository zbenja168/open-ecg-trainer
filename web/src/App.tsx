import { useEffect, useMemo, useRef, useState } from 'react'
import { buildSession, conditionOf, gradeFor, nextDue, review, spacedSet, type QueueEntry } from './scheduler'
import { clear, download, load, logAsCsv, newProgress, save } from './storage'
import { useTheme } from './theme'
import type { EcgClass, Item, Progress, ResponseLog } from './types'

type Screen = 'home' | 'practice' | 'done'

export default function App() {
  const [items, setItems] = useState<Item[] | null>(null)
  const [classes, setClasses] = useState<EcgClass[]>([])
  const [error, setError] = useState('')
  const [progress, setProgress] = useState<Progress>(() => load() ?? newProgress())
  const [screen, setScreen] = useState<Screen>('home')
  const [queue, setQueue] = useState<QueueEntry[]>([])
  const [pos, setPos] = useState(0)
  const [sessionId, setSessionId] = useState('')

  useEffect(() => {
    Promise.all([fetch('data/items.json'), fetch('data/classes.json')])
      .then(async ([a, b]) => {
        if (!a.ok || !b.ok) throw new Error('item bank failed to load')
        setItems(await a.json())
        setClasses(await b.json())
      })
      .catch((e) => setError(String(e)))
  }, [])

  useEffect(() => save(progress), [progress])

  if (error) return <Shell><p className="text-danger">Could not load the item bank: {error}</p></Shell>
  if (!items) return <Shell><p>Loading…</p></Shell>

  const start = () => {
    const q = buildSession(items, classes, progress, new Date())
    setQueue(q)
    setPos(0)
    setSessionId(new Date().toISOString())
    setScreen(q.length ? 'practice' : 'done')
  }

  const record = (entry: QueueEntry, response: ResponseLog) => {
    const id = entry.item.id
    let card = progress.cards[id]
    let log = response
    if (entry.condition === 'spaced') {
      const grade = gradeFor(log.correct, log.confidence)
      card = review(progress.cards[id], grade, new Date(log.answeredAt))
      log = { ...log, rating: grade, stabilityBefore: progress.cards[id]?.stability, stabilityAfter: card.stability }
    }
    const blockFinished = entry.condition === 'massed' && !queue.slice(pos + 1).some((q) => q.condition === 'massed')
    setProgress((p) => ({
      ...p,
      log: [...p.log, log],
      cards: entry.condition === 'spaced' ? { ...p.cards, [id]: card } : p.cards,
      massedDone: blockFinished && !p.massedDone.includes(entry.item.classId)
        ? [...p.massedDone, entry.item.classId] : p.massedDone,
    }))
  }

  const advance = () => (pos + 1 < queue.length ? setPos(pos + 1) : setScreen('done'))

  return (
    <Shell>
      {screen === 'home' && (
        <Home items={items} classes={classes} progress={progress} onStart={start}
          onReset={(cb) => { clear(); setProgress(newProgress(cb)) }} />
      )}
      {screen === 'practice' && queue[pos] && (
        <Practice key={`${sessionId}-${pos}`} entry={queue[pos]} classes={classes} index={pos} total={queue.length}
          participant={progress.participant.key} sessionId={sessionId} onAnswer={record} onNext={advance} />
      )}
      {screen === 'done' && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Session complete</h2>
          <p>{queue.length ? `${queue.length} ECGs reviewed.` : 'Nothing is due right now.'}</p>
          <button className="btn" onClick={() => setScreen('home')}>Back to overview</button>
        </div>
      )}
    </Shell>
  )
}

function Shell({ children }: { children: React.ReactNode }) {
  const { theme, cycle } = useTheme()
  return (
    <div className="mx-auto max-w-5xl px-4 py-6">
      <header className="mb-6 flex flex-wrap items-baseline justify-between gap-2 border-b border-line pb-3">
        <h1 className="text-2xl font-semibold tracking-tight">Open ECG Trainer</h1>
        <div className="flex items-baseline gap-3">
          <span className="text-xs text-muted">prototype · items not yet cardiologist-reviewed</span>
          <button className="btn-quiet text-xs" onClick={cycle} title="Switch colour theme">
            Theme: {theme === 'system' ? 'System' : theme === 'light' ? 'Light' : 'Dark'}
          </button>
        </div>
      </header>
      {children}
      <footer className="mt-10 border-t border-line pt-3 text-xs text-muted">
        ECGs: PTB-XL v1.0.3 (Wagner et al., Sci Data 2020; PhysioNet), CC BY 4.0, re-rendered at 25 mm/s and
        10 mm/mV. Code MIT.
      </footer>
    </div>
  )
}

function Home({ items, classes, progress, onStart, onReset }: {
  items: Item[]; classes: EcgClass[]; progress: Progress
  onStart: () => void; onReset: (cb: Progress['participant']['counterbalance']) => void
}) {
  const due = nextDue(items, progress)
  const now = new Date()
  const dueCount = items.filter((i) => conditionOf(i, progress) === 'spaced' && progress.cards[i.id]
    && new Date(progress.cards[i.id].due) <= now).length
  const byClass = useMemo(() => {
    const m = new Map<string, { n: number; right: number }>()
    for (const r of progress.log) {
      const s = m.get(r.classId) ?? { n: 0, right: 0 }
      s.n++
      if (r.correct) s.right++
      m.set(r.classId, s)
    }
    return m
  }, [progress.log])
  const spaced = spacedSet(progress)

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-line bg-panel p-4">
        <p className="text-sm text-muted">
          Participant <code>{progress.participant.key}</code> · set {spaced} spaced, set {spaced === 'A' ? 'B' : 'A'} massed
          · {progress.log.length} responses logged
        </p>
        <p className="mt-1 text-sm text-muted">
          {dueCount} spaced reviews due now
          {due && dueCount === 0 ? `; next due ${due.toLocaleString()}` : ''} · massed blocks done {progress.massedDone.length}
        </p>
        <button className="btn mt-4" onClick={onStart}>Start session</button>
      </section>

      <section>
        <h2 className="mb-2 font-semibold">Accuracy by class</h2>
        <table className="w-full text-sm">
          <thead><tr className="text-left text-muted"><th>Class</th><th>Set</th><th>Seen</th><th>Correct</th></tr></thead>
          <tbody>
            {classes.filter((c) => c.available).map((c) => {
              const s = byClass.get(c.id)
              return (
                <tr key={c.id} className="border-t border-line-soft">
                  <td className="py-1">{c.name}</td><td>{c.set}</td><td>{s?.n ?? 0}</td>
                  <td>{s ? `${Math.round((100 * s.right) / s.n)}%` : '-'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </section>

      <section className="flex flex-wrap gap-2 text-sm">
        <button className="btn-quiet" onClick={() => download('responses.csv', logAsCsv(progress), 'text/csv')}>Export log (CSV)</button>
        <button className="btn-quiet" onClick={() => download('progress.json', JSON.stringify(progress, null, 1), 'application/json')}>Export everything (JSON)</button>
        <button className="btn-quiet" onClick={() => onReset('A-spaced')}>Reset as A-spaced</button>
        <button className="btn-quiet" onClick={() => onReset('B-spaced')}>Reset as B-spaced</button>
      </section>
    </div>
  )
}

function Practice({ entry, classes, index, total, participant, sessionId, onAnswer, onNext }: {
  entry: QueueEntry; classes: EcgClass[]; index: number; total: number; participant: string; sessionId: string
  onAnswer: (e: QueueEntry, log: ResponseLog) => void; onNext: () => void
}) {
  const shownAt = useRef(new Date())
  const [answer, setAnswer] = useState('')
  const [confidence, setConfidence] = useState(0)
  const [result, setResult] = useState<ResponseLog | null>(null)
  const { item } = entry
  const options = classes.filter((c) => c.available)
  const groups = [...new Set(options.map((c) => c.group))]
  const nameOf = (id: string) => classes.find((c) => c.id === id)?.name ?? id

  const submit = () => {
    const answeredAt = new Date()
    const log: ResponseLog = {
      participant, sessionId, itemId: item.id, classId: item.classId, answer,
      correct: item.acceptable.includes(answer), confidence,
      latencyMs: answeredAt.getTime() - shownAt.current.getTime(),
      shownAt: shownAt.current.toISOString(), answeredAt: answeredAt.toISOString(),
      condition: entry.condition,
    }
    onAnswer(entry, log)
    setResult(log)
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-muted">ECG {index + 1} of {total}</p>
      <a href={item.image} target="_blank" rel="noreferrer" title="Open full size">
        {/* latency is timed from when the ECG is visible, not from when the screen mounted */}
        <img src={item.image} alt="12-lead ECG" className="w-full rounded border border-line bg-white"
          onLoad={() => { shownAt.current = new Date() }} />
      </a>

      {!result ? (
        <>
          <div className="space-y-2">
            {groups.map((g) => (
              <div key={g}>
                <p className="text-xs uppercase tracking-wide text-muted">{g}</p>
                <div className="mt-1 flex flex-wrap gap-1.5">
                  {options.filter((c) => c.group === g).map((c) => (
                    <button key={c.id} onClick={() => setAnswer(c.id)}
                      className={`chip ${answer === c.id ? 'chip-on' : ''}`}>{c.name}</button>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm">Confidence</span>
            {[1, 2, 3, 4, 5].map((n) => (
              <button key={n} onClick={() => setConfidence(n)}
                className={`chip w-9 justify-center ${confidence === n ? 'chip-on' : ''}`}>{n}</button>
            ))}
            <span className="text-xs text-muted">1 = guessing, 5 = certain</span>
          </div>
          <button className="btn" disabled={!answer || !confidence} onClick={submit}>Check</button>
        </>
      ) : (
        <div className={`rounded-lg border p-4 ${result.correct ? 'border-ok-line bg-ok' : 'border-bad-line bg-bad'}`}>
          <p className="font-semibold">{result.correct ? 'Correct' : `Not quite: you said ${nameOf(result.answer)}`}</p>
          <p className="mt-1">Label: <strong>{nameOf(item.classId)}</strong>
            {item.acceptable.length > 1 && <> (also accepted: {item.acceptable.filter((a) => a !== item.classId).map(nameOf).join(', ')})</>}
          </p>
          <p className="mt-1 text-xs text-muted">
            {item.source} record {item.ecgId} ·{' '}
            {item.likelihood === null ? 'rhythm/form label (likelihood not graded)' : `label likelihood ${item.likelihood}%`} ·{' '}
            {item.validated ? 'report human-validated' : 'report not human-validated'}
          </p>
          <button className="btn mt-3" onClick={onNext} autoFocus>Next</button>
        </div>
      )}
    </div>
  )
}
