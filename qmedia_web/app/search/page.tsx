import { Suspense } from "react";
import Header from "@/components/header";
import Sidebar from "@/components/sidebar";
import { CastIcon, BotMessageSquareIcon, ArrowUpIcon } from "lucide-react";
import ReferencesOutSite from "./references-out-site";
import ReferencesInSite from "./references-in-site";
import Answers from "./answers";
import Skeleton from "./skeleton";

export default async function Page({
  searchParams,
}: {
  searchParams: { q: string };
}) {
  return (
    <>
      <div className="fixed w-screen 2xl:container mx-auto left-1/2 transform -translate-x-1/2 z-10">
        <Header searchParams={searchParams} />
      </div>
      <div className="dark:bg-inherit 2xl:container mx-auto relative flex">
        <Sidebar />
        <main className="pt-24 pl-6 lg:pl-0 pr-6 2xl:pr-0 flex-1 md:h-screen md:flex relative overflow-y-auto">
          <div className="md:grow md:h-full pb-4 flex flex-col">
            <h1 className="text-3xl mb-12">{searchParams.q}</h1>
            <h2 className="text-xl mb-4 flex items-center">
              <CastIcon className="mr-2" />
              来源
            </h2>
            <Suspense fallback={<Skeleton />}>
              <ReferencesOutSite searchParams={searchParams} />
            </Suspense>
            <h2 className="text-xl mt-12 mb-4 flex items-center">
              <BotMessageSquareIcon className="mr-2" />
              答案
            </h2>
            <Suspense fallback={<Skeleton />}>
              <Answers
                className="grow shrink-0 pb-12"
                searchParams={searchParams}
              />
            </Suspense>
            <div className="fixed md:sticky left-0 bottom-0 pb-8 w-full px-4 lg:px-0 z-10 bg-white dark:bg-black">
              <div className="relative lg:w-[44rem] md:w-[34rem]">
                <input
                  type="text"
                  id="default-search"
                  className="block py-3 ps-4 text-sm text-gray-700 rounded-lg border border-gray-400 dark:bg-gray-800 dark:placeholder-gray-400 dark:text-white outline-none w-full"
                  placeholder="提出后续问题"
                />
                <button className="absolute top-1/2 -mt-4 size-8 end-6 flex items-center justify-center cursor-pointer bg-gray-200 dark:bg-gray-600 rounded-full">
                  <ArrowUpIcon className="size-5 text-gray-400 dark:text-gray-400" />
                </button>
              </div>
            </div>
          </div>
          <div className="shrink-0 md:w-[24rem] xl:w-[32rem] ml-4 pb-32">
            <Suspense fallback={<Skeleton />}>
              <ReferencesInSite searchParams={searchParams} />
            </Suspense>
          </div>
        </main>
        <div className="mb-12"></div>
      </div>
    </>
  );
}
