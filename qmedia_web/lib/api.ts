const _fetch = async (url: string) => {
  const res = await fetch(url, {
    next: { revalidate: 1 },
    headers: {
      'Content-Type': 'application/json',
    },
  })
  const data = await res.json()

  if (data?.code !== 0) {
    throw new Error(data.data?.msg)
  }

  return data.data
}

const endpoint = process.env.SERVICE_ENDPOINT
const getEndpoint = (backend?: boolean) => (backend ? endpoint : '/api')

export async function getNotes() {
  return _fetch('/api/notes')
}

export async function getNote(id: string, { backend }: { backend?: boolean }) {
  return _fetch(`${getEndpoint(backend)}/note/${id}`)
}

export async function getPublicSearch(q: string, { backend }: { backend?: boolean }) {
  return _fetch(`${getEndpoint(backend)}/public-search/?query=${encodeURIComponent(q)}`)
}

export async function getRagSearch(q: string, { backend }: { backend?: boolean }) {
  return _fetch(`${getEndpoint(backend)}/mm-rag-search/?query=${encodeURIComponent(q)}`)
}

export async function getRagQuery(q: string, { backend }: { backend?: boolean }) {
  return _fetch(`${getEndpoint(backend)}/mm-rag-query/?query=${encodeURIComponent(q)}`)
}
