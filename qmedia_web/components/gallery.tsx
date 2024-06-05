"use client";

import { useState, useEffect } from "react";
import Card from "@/components/card";
import { getNotes } from "@/lib/api";
import type { Card as CardType } from "@/types";

export default function Component() {
  const [loading, setLoading] = useState(false);
  const [list, setList] = useState<CardType[]>([]);
  const getData = async () => {
    setLoading(true);
    try {
      const data = await getNotes();
      const parsed = data.map((item: any) => {
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
      });
      setList(parsed);
      setLoading(false);
    } catch (error) {
      setLoading(false);
    }
  };
  useEffect(() => {
    if (loading) {
      return;
    }
    getData();
  }, []);

  return (
    <div className="grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
      {list.map((item) => (
        <Card key={item.noteId} card={item} />
      ))}
    </div>
  );
}
