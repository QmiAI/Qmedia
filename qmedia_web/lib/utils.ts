import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { Card } from "@/types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getCard(item: any): Card {
  const noteId = item.info_data?.id || "";
  const hasVideo = !!item.video_data?.video_url?.length;
  const imgSrc = hasVideo
    ? item.video_data?.video_url[0]
    : (item.image_data?.image_urls || [])[0];
  const title = item.info_data?.title || "";
  const author = item.info_data?.user_dict?.nickname || "";
  const avatar = item.info_data?.user_dict?.avatar || "";
  const star = item.info_data?.interact_info?.liked_count || 0;
  return {
    noteId,
    imgSrc,
    title,
    author,
    star,
    avatar,
    hasVideo,
  };
}
