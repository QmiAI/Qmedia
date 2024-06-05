import { Suspense } from "react";
import Header from "@/components/header";
import Sidebar from "@/components/sidebar";
import { getNote } from "@/lib/api";
import {
  HeartIcon,
  StarIcon,
  ChatBubbleIcon,
  Share1Icon,
} from "@radix-ui/react-icons";

import Detail from "./detail";

const getData = async (noteId: string) => {
  const data = await getNote(noteId, { backend: true });
  const author = data?.info_data?.user_dict.nickname;
  const avatar = data?.info_data?.user_dict.avatar;
  const hasVideo = !!data.video_data?.video_url?.length;
  const videoSrc = hasVideo && data.video_data?.video_url[0];
  const imgUrls = data.image_data?.image_urls || [];
  const title = data.info_data?.title || "";
  const desc = (data.info_data?.desc || "").trim();
  const star = data.info_data?.interact_info?.liked_count || 0;
  return {
    ...data,
    imgUrls,
    title,
    desc,
    author,
    star,
    avatar,
    hasVideo,
    videoSrc,
  };
};

function Skeleton() {
  return (
    <main className="pt-24 lg:pr-6 2xl:pr-0 lg:pb-8 flex-1 h-full">
      <div className="w-full h-full flex flex-col lg:flex-row">
        <div className="lg:hidden py-2 px-6 flex items-center border-t"></div>
        <div className="lg:flex-1 h-[40rem] lg:h-full flex items-center justify-center bg-gray-100">
          <div className="text-3xl font-bold text-gray-400">Loading...</div>
        </div>
        <div className="lg:w-96 lg:h-full lg:overflow-y-scroll flex flex-col grow lg:flex-none lg:ml-4">
          <div className="border-b dark:border-b-gray-700 shrink-0 py-2 px-6"></div>
          <div className="flex-1 w-full flex justify-center items-center">
            <div className="text-2xl font-bold text-gray-400">COMMENT</div>
          </div>
          <div className="sticky bottom-0 bg-white dark:bg-inherit shrink-0 h-16 border-t dark:border-gray-700 flex items-center px-6">
            <div className="relative h-10 flex-1 bg-gray-100 dark:bg-gray-800 rounded-full">
              <div className="absolute left-1 top-1 size-8 bg-gray-200 dark:bg-gray-600 rounded-full"></div>
            </div>
            <div className="space-x-3 flex items-center ml-4 text-2xl">
              <HeartIcon className="size-6" />
              <StarIcon className="size-6" />
              <ChatBubbleIcon className="size-6" />
              <Share1Icon className="size-6" />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

export default async function Page({ params }: { params: { id: string } }) {
  const data = await getData(params.id);
  return (
    <>
      <div className="fixed w-screen 2xl:container mx-auto left-1/2 transform -translate-x-1/2 z-10">
        <Header />
      </div>
      <div className="dark:bg-inherit 2xl:container mx-auto relative lg:flex h-screen">
        <Sidebar />
        <Suspense fallback={<Skeleton />}>
          <Detail params={params} />
        </Suspense>
      </div>
    </>
  );
}
