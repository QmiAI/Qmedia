"use client";

import { useState, useEffect } from "react";
import Markdown from "react-markdown";
import remarkBreaks from "remark-breaks";

function sleep(ms: number = 400) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const CustomComponents: React.ComponentProps<typeof Markdown>["components"] = {
  h1: ({ node, ...props }) => <h1 className="text-4xl font-bold" {...props} />,
  h2: ({ node, ...props }) => <h2 className="text-3xl font-bold" {...props} />,
  h3: ({ node, ...props }) => <h3 className="text-2xl font-bold" {...props} />,
  h4: ({ node, ...props }) => <h4 className="text-xl font-bold" {...props} />,
  h5: ({ node, ...props }) => <h5 className="text-base font-bold" {...props} />,
  h6: ({ node, ...props }) => <h6 className="text-base font-bold" {...props} />,
  p: ({ node, ...props }) => <p className="text-base" {...props} />,
};

export default function Page({
  text,
  className,
}: {
  text: string;
  className?: string;
}) {
  const [txt, setTxt] = useState<string>("");

  useEffect(() => {
    (async () => {
      for (const char of text) {
        await sleep(2);
        setTxt((x) => `${x}${char}`);
      }
    })();
  }, [text]);

  return (
    <div className={`text-gray-600 dark:text-gray-300 ${className || ""}`}>
      <Markdown remarkPlugins={[remarkBreaks]} components={CustomComponents}>
        {txt}
      </Markdown>
    </div>
  );
}
