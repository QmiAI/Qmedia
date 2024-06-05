"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Search } from "lucide-react";
import Logo from "./logo";

export default function Header({
  searchParams,
}: {
  searchParams?: { q: string };
}) {
  const router = useRouter();
  const [value, setValue] = useState(searchParams?.q || "");

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      router.push(`/search?q=${encodeURIComponent(value)}`);
    }
  };

  return (
    <header className="flex items-center justify-between bg-white dark:bg-black py-3 px-8">
      <h1 className="text-3xl font-bold">
        <Link href="/">
          <Logo />
        </Link>
      </h1>
      <div className="relative grow md:grow-0 lg:w-[32rem] md:w-[28rem] mx-6 sm:mx-10">
        <input
          type="text"
          id="default-search"
          className="block py-2 md:py-3 ps-6 text-sm text-gray-700 rounded-full bg-gray-50 dark:bg-gray-800 dark:placeholder-gray-400 dark:text-white outline-none w-full"
          placeholder="搜索 Qmedia"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyUp={handleKeyPress}
        />
        <button className="absolute inset-y-0 end-6 flex items-center ps-3 cursor-pointer">
          <Search className="w-4 h-4 text-gray-500 dark:text-gray-400" />
        </button>
      </div>
      <div className="flex items-center text-gray-500 dark:text-gray-300">
        业务合作
      </div>
    </header>
  );
}
