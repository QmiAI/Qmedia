"use client";

import * as React from "react";
import { Moon, Sun, Menu, SunMoon } from "lucide-react";
import { ThemeProvider, useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const getModeTxt = (theme: string | undefined) => {
  if (theme === "light") return "浅色模式";
  if (theme === "dark") return "深色模式";
  return "跟随系统";
};

export function Main() {
  const { setTheme, theme } = useTheme();

  const modeTxt = getModeTxt(theme);

  return (
    <div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            className="justify-start text-sm px-4 py-4 w-full rounded-full"
            variant="ghost"
          >
            <Menu className="w-5 h-5 mr-2" />
            更多
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <div className="flex items-center p-2">
            <div className="text-gray-700 dark:text-gray-300 mr-6">
              {modeTxt}
            </div>
            <TooltipProvider>
              <div className="flex items-center">
                <Tooltip>
                  <TooltipTrigger>
                    <DropdownMenuItem onClick={() => setTheme("system")}>
                      <SunMoon className="transition-all w-4 h-4" />
                    </DropdownMenuItem>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>跟随系统</p>
                  </TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger>
                    <DropdownMenuItem onClick={() => setTheme("light")}>
                      <Sun className="transition-all w-4 h-4" />
                    </DropdownMenuItem>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>浅色模式</p>
                  </TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger>
                    <DropdownMenuItem onClick={() => setTheme("dark")}>
                      <Moon className="transition-all w-4 h-4" />
                    </DropdownMenuItem>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>深色模式</p>
                  </TooltipContent>
                </Tooltip>
              </div>
            </TooltipProvider>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

export default function ThemeSelector() {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <Main />
    </ThemeProvider>
  );
}
