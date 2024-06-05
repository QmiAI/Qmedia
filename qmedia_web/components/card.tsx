import Link from "next/link";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { HeartIcon } from "@radix-ui/react-icons";
import type { Card } from "@/types";

export default function Card({
  card,
  className,
}: {
  card: Card;
  className?: string;
}) {
  const item = card;

  return (
    <div
      key={item.imgSrc}
      className={`mt-4 flex flex-col rounded-lg overflow-hidden ${className}`}
    >
      <Link className="w-full h-full" href={`/explore/${item.noteId}`}>
        {item.hasVideo ? (
          <video
            className="w-full h-full max-h-[20rem] object-cover rounded-lg"
            src={item.imgSrc}
          />
        ) : (
          <img
            className="w-full h-full max-h-[20rem] object-cover rounded-lg"
            src={item.imgSrc}
            alt=""
          />
        )}
      </Link>
      <div className="px-2">
        <div className="text-sm mt-2 truncate">{item.title}</div>
        <div className="flex items-center text-xs text-gray-600 dark:text-gray-300 mt-2">
          <Avatar className="w-4 h-4 mr-1 border border-gray-200">
            <AvatarImage src={item.avatar} alt={item.author} />
            <AvatarFallback>
              <div className="size-full bg-gray-200"></div>
            </AvatarFallback>
          </Avatar>
          <div className="flex-1">{item.author}</div>
          <div className="flex items-center">
            <HeartIcon className="mr-1" />
            {item.star}
          </div>
        </div>
      </div>
    </div>
  );
}
