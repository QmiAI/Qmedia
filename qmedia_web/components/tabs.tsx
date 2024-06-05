"use client";

import { useState } from "react";
import clsx from "clsx";

const data = [
  {
    id: 1,
    title: "推荐",
  },
  {
    id: 2,
    title: "电子公园",
  },
  {
    id: 3,
    title: "穿搭",
  },
  {
    id: 4,
    title: "美食",
  },
  {
    id: 5,
    title: "彩妆",
  },
  {
    id: 6,
    title: "影视",
  },
  {
    id: 7,
    title: "职场",
  },
  {
    id: 8,
    title: "家具",
  },
  {
    id: 9,
    title: "游戏",
  },
  {
    id: 10,
    title: "旅行",
  },
  {
    id: 11,
    title: "健身",
  },
];

export default function Tabs() {
  const [activeTab, setActiveTab] = useState(1);

  return (
    <ul
      className={clsx(
        "flex flex-wrap text-sm font-medium text-center text-gray-500 dark:text-gray-400"
      )}
    >
      {data.map((item) => (
        <li
          key={item.id}
          className="me-2"
          onClick={() => setActiveTab(item.id)}
        >
          <span
            className={clsx(
              "inline-block px-3 py-2 text-gray-600 dark:text-gray-300 rounded-full text-base font-light cursor-pointer",
              activeTab === item.id
                ? "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 font-medium"
                : ""
            )}
            aria-current="page"
          >
            {item.title}
          </span>
        </li>
      ))}
    </ul>
  );
}
