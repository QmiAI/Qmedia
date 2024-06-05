import { getPublicSearch } from '@/lib/api'

export default async function Page({ searchParams }: { searchParams: { q: string } }) {
  const res = await getPublicSearch(searchParams.q, { backend: true })
  const list = (res || []).map((item: any) => {
    let domain = ''
    try {
      const url = new URL(item.url)
      domain = url.hostname
    } catch (e) {
      console.error(e)
    }

    return {
      title: item.title,
      description: item.description,
      url: item.url,
      domain,
    }
  })

  return (
    <div className="grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3">
      {list.map((item: any) => (
        <a href={item.url} target="_blank" key={item.title} className="block p-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 transition-all">
          <h5 className="h-10 overflow-hidden line-clamp-2 mb-2 text-sm font-bold tracking-tight text-gray-900 dark:text-gray-300">{item.title}</h5>
          <div className="flex items-center">
            <h5 className="truncate text-sm font-normal text-gray-700 dark:text-gray-400">{item.domain}</h5>
          </div>
        </a>
      ))}
    </div>
  )
}
