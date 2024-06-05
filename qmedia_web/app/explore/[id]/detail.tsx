import { getNote } from "@/lib/api";
import {
  HeartIcon,
  StarIcon,
  ChatBubbleIcon,
  Share1Icon,
} from "@radix-ui/react-icons";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

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
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
export default async function Page({ params }: { params: { id: string } }) {
  await sleep(3000);
  const data = await getData(params.id);
  return (
    <main className="pt-20 lg:pr-6 2xl:pr-0 lg:pb-8 flex-1 h-full">
      <div className="w-full h-full flex flex-col lg:flex-row">
        <div className="lg:hidden py-2 px-6 flex items-center border-t">
          <Avatar className="w-10 h-10 mr-2 border border-gray-200">
            <AvatarImage src={data.avatar} alt={data.author} />
            <AvatarFallback>
              <div className="size-full bg-gray-200"></div>
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 text-gray-400">{data.author}</div>
        </div>
        <div className="lg:flex-1 h-[40rem] lg:h-full flex items-center justify-center dark:bg-black">
          {data.hasVideo ? (
            <video
              controls
              className="object-contain h-full"
              src={data.videoSrc}
            ></video>
          ) : (
            <Carousel className="h-full">
              <CarouselContent className="h-full">
                {data.imgUrls.map((url: string) => (
                  <CarouselItem key={url} className="h-full">
                    <img
                      src={url}
                      className="w-full h-full object-contain"
                      alt=""
                    />
                  </CarouselItem>
                ))}
              </CarouselContent>
              <CarouselPrevious />
              <CarouselNext />
            </Carousel>
          )}
        </div>
        <div className="lg:w-96 lg:h-full lg:overflow-y-scroll flex flex-col grow lg:flex-none lg:ml-4">
          <div className="border-b dark:border-b-gray-700 shrink-0 py-2 px-6">
            <div className="font-medium">{data.title}</div>
            <div className="text-gray-600 dark:text-gray-300 text-sm lg:text-base mt-2 lg:mt-4">
              {data.desc || data.title}
            </div>
          </div>
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
