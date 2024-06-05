"use client";

import { useState } from "react";
import clsx from "clsx";
import { useRouter } from "next/navigation";
import { HomeIcon, PlusCircledIcon, CircleIcon } from "@radix-ui/react-icons";
import { BellIcon } from "@heroicons/react/24/outline";
import { Button } from "@/components/ui/button";

import ThemeSelector from "@/components/theme-selector";

const tabs = [
  {
    id: 1,
    name: "发现",
    icon: HomeIcon,
  },
  {
    id: 2,
    name: "发布",
    icon: PlusCircledIcon,
  },
  {
    id: 3,
    name: "通知",
    icon: BellIcon,
  },
  {
    id: 4,
    name: "我",
    icon: CircleIcon,
  },
];

export default function Sidebar() {
  const [activeTab, setActiveTab] = useState(1);
  const router = useRouter();

  return (
    <aside className="left-0 h-screen w-72 flex-shrink-0 flex-col px-4 pb-4 pt-24 sticky top-0 hidden lg:flex overflow-y-hidden">
      <ul className="space-y-2 flex-1">
        {tabs.map((tab) => (
          <li key={tab.id}>
            <Button
              className={clsx(
                "justify-start text-sm px-6 py-6 w-full rounded-full",
                activeTab === tab.id && "bg-gray-100 dark:bg-gray-700"
              )}
              variant="ghost"
              onClick={() => {
                setActiveTab(tab.id);
                if (tab.id === 1 && location.pathname !== "/") {
                  router.push("/");
                }
              }}
            >
              <tab.icon className="w-5 h-5 mr-2" />
              {tab.name}
            </Button>
          </li>
        ))}
      </ul>
      <ThemeSelector />
    </aside>
  );
}
