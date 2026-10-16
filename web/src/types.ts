import type { Card } from 'ts-fsrs'

export type SetId = 'A' | 'B'

export interface EcgClass {
  id: string
  group: string
  name: string
  set: SetId | 'both'
  available: boolean
}

export interface Item {
  id: string
  classId: string
  /** every teaching class the record matches; any of them is scored correct */
  acceptable: string[]
  set: SetId | 'both'
  source: string
  ecgId: number
  likelihood: number
  validated: boolean
  image: string
}

/** A = set A spaced and set B massed; B = the reverse. */
export type Counterbalance = 'A-spaced' | 'B-spaced'
export type Condition = 'spaced' | 'massed' | 'foil'

export interface Participant {
  key: string
  counterbalance: Counterbalance
  createdAt: string
}

export interface ResponseLog {
  participant: string
  itemId: string
  classId: string
  answer: string
  correct: boolean
  confidence: number
  latencyMs: number
  shownAt: string
  answeredAt: string
  condition: Condition
  sessionId: string
  /** FSRS rating given to the scheduler (spaced items only) */
  rating?: number
  stabilityBefore?: number
  stabilityAfter?: number
}

export interface Progress {
  participant: Participant
  cards: Record<string, Card>
  massedDone: string[]
  log: ResponseLog[]
}
