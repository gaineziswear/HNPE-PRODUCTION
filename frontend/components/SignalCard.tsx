export default function SignalCard({signal}) {
  return (
    <div className="p-3 border rounded">
      <div>{signal.symbol} — {signal.direction}</div>
      <div>Score: {signal.score}</div>
    </div>
  )
}
