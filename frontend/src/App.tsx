import { useEffect, useState } from 'react'

type Health = {
  status: string
  service: string
  catalogue: {
    cards: number
  }
}

const navigation = ['Overview', 'Transactions', 'Milestones', 'Rewards']

function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [apiAvailable, setApiAvailable] = useState(true)

  useEffect(() => {
    const controller = new AbortController()

    fetch('/api/health/', { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error('API unavailable')
        return response.json() as Promise<Health>
      })
      .then((payload) => setHealth(payload))
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setApiAvailable(false)
      })

    return () => controller.abort()
  }, [])

  return (
    <div className="min-h-screen bg-[#f6f7f9] text-[#17191c]">
      <aside className="fixed inset-y-0 hidden w-60 border-r border-[#dedfe3] bg-white px-5 py-6 lg:block">
        <div className="flex h-full flex-col">
          <div className="flex items-center gap-3 px-2">
            <span className="grid size-9 place-items-center rounded-md bg-[#15171a] text-sm font-semibold text-white">
              SD
            </span>
            <span className="text-lg font-semibold">SpendDeck</span>
          </div>

          <nav className="mt-10 space-y-1" aria-label="Primary navigation">
            {navigation.map((item, index) => (
              <div
                key={item}
                aria-current={index === 0 ? 'page' : undefined}
                className={
                  index === 0
                    ? 'rounded-md bg-[#eef4ef] px-3 py-2.5 text-sm font-medium text-[#24573b]'
                    : 'px-3 py-2.5 text-sm text-[#676b73]'
                }
              >
                {item}
              </div>
            ))}
          </nav>

          <div className="mt-auto border-t border-[#e5e6e9] px-2 pt-4 text-xs text-[#676b73]">
            <div className="flex items-center gap-2">
              <span
                className={`size-2 rounded-full ${apiAvailable ? 'bg-[#2d7a4f]' : 'bg-[#bd3f35]'}`}
              />
              {apiAvailable ? 'Local service' : 'Service unavailable'}
            </div>
          </div>
        </div>
      </aside>

      <main className="min-h-screen lg:pl-60">
        <header className="border-b border-[#dedfe3] bg-white px-5 py-4 sm:px-8">
          <div className="mx-auto flex max-w-6xl items-center justify-between">
            <div className="flex items-center gap-3 lg:hidden">
              <span className="grid size-8 place-items-center rounded-md bg-[#15171a] text-xs font-semibold text-white">
                SD
              </span>
              <span className="font-semibold">SpendDeck</span>
            </div>
            <p className="hidden text-sm text-[#676b73] lg:block">Overview</p>
            <p className="text-sm text-[#676b73]">
              {health ? `${health.catalogue.cards} supported cards` : 'Connecting'}
            </p>
          </div>
        </header>

        <div className="mx-auto max-w-6xl px-5 py-8 sm:px-8">
          <div className="mb-7">
            <h1 className="text-2xl font-semibold">Your card overview</h1>
            <p className="mt-1 text-sm text-[#676b73]">Current billing cycle</p>
          </div>

          <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4" aria-label="Summary">
            {[
              ['Total spend', '₹0'],
              ['Eligible spend', '₹0'],
              ['Milestones active', '0'],
              ['Rewards pending', '0'],
            ].map(([label, value]) => (
              <article key={label} className="rounded-md border border-[#dedfe3] bg-white p-5">
                <p className="text-sm text-[#676b73]">{label}</p>
                <p className="mt-3 text-2xl font-semibold tabular-nums">{value}</p>
              </article>
            ))}
          </section>

          <section className="mt-8 border-t border-[#dedfe3] pt-7">
            <div className="flex items-end justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold">Cards</h2>
                <p className="mt-1 text-sm text-[#676b73]">No cards are configured yet.</p>
              </div>
              <span className="rounded-md bg-[#fff4d6] px-3 py-1.5 text-xs font-medium text-[#72510c]">
                {health && health.catalogue.cards > 0
                  ? `${health.catalogue.cards} available`
                  : 'Catalogue empty'}
              </span>
            </div>

            <div className="mt-5 overflow-hidden rounded-md border border-[#dedfe3] bg-white">
              <div className="grid grid-cols-[1fr_auto] border-b border-[#e7e8eb] bg-[#fafafa] px-5 py-3 text-xs font-medium text-[#676b73]">
                <span>Card</span>
                <span>Status</span>
              </div>
              <div className="px-5 py-14 text-center">
                <p className="text-sm font-medium">No cards to show</p>
                <p className="mt-1 text-sm text-[#7a7e86]">
                  Supported cards will appear here when their catalogue definitions are added.
                </p>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}

export default App
