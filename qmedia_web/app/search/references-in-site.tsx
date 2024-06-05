import Link from "next/link";
import { getRagSearch } from "@/lib/api";
import Card from "@/components/card";
import type { Card as CardType } from "@/types";
import { getCard } from "@/lib/utils";

export default async function Page({
  searchParams,
}: {
  searchParams: { q: string };
}) {
  const res = await getRagSearch(searchParams.q, { backend: true });
  const list: CardType[] = (res.search_nodes || []).map(getCard);

  return (
    <div className="grid gap-4 grid-cols-2 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2">
      {list.map((item) => (
        <Link
          key={item.noteId}
          href={`/explore/${item.noteId}`}
          className="hover:scale-105 transition-all"
        >
          <Card card={item} />
        </Link>
      ))}
    </div>
  );
}
