export async function GET() {
  const res = await fetch(`${process.env.SERVICE_ENDPOINT}/notes`, {
    next: { revalidate: 1 },
    headers: {
      'Content-Type': 'application/json',
    },
  })
  const data = await res.json()

  return Response.json(data)
}
