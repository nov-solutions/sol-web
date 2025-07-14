"use client";

import { useEffect } from "react";

import { Button } from "@/components/ui/button";
import { PAGES, SITE_NAME } from "@/constants";
import Image from "next/image";
import Link from "next/link";

export default function Nav() {
  const pages = PAGES.filter(
    ({ relativePath }) =>
      relativePath !== "/" && !relativePath.startsWith("/app"),
  ).map(({ name, relativePath }) => ({ name, relativePath }));

  useEffect(() => {
    const mobileNavbar = document.getElementById("mobile-navbar");
    const mobileDrawerToggle = document.getElementById("mobile-drawer-toggle");

    let isDrawerOpen = false;

    mobileDrawerToggle!.addEventListener("click", () => {
      isDrawerOpen = !isDrawerOpen;

      if (isDrawerOpen) {
        mobileNavbar!.classList.remove("bg-white/75");
        mobileNavbar!.classList.add("bg-white");
      } else {
        mobileNavbar!.classList.add("bg-white/75");
        mobileNavbar!.classList.remove("bg-white");
      }
    });
  }, []);

  return (
    <nav className="fixed top-0 left-0 z-10 w-full ">
      <div className="items-center justify-between hidden w-1/2 h-full p-4 mx-auto mt-2 text-sm rounded-lg shadow-lg lg:flex backdrop-blur-lg bg-foreground/40">
        <Link href="/" className="flex items-center">
          <Image
            src="/assets/img/logos/wordmark.png"
            alt={SITE_NAME + " wordmark"}
            className="h-5 my-auto"
            width={60}
            height={60}
          />
        </Link>
        <div className="items-center space-x-4 font-semibold">
          {pages.map((page, i) => (
            <Button variant="link" asChild key={i}>
              <Link href={page.relativePath}>{page.name}</Link>
            </Button>
          ))}
        </div>
        <Button asChild>
          <Link href="TODO">TODO</Link>
        </Button>
      </div>

      <div
        id="mobile-navbar"
        className="flex items-center justify-between w-full h-full py-2 pl-4 rounded-b-lg shadow-lg lg:hidden bg-foreground/40 backdrop-blur-lg"
      >
        <Link href="/" className="flex items-center">
          <Image
            src="/assets/img/logos/wordmark.png"
            alt={SITE_NAME + " wordmark"}
            className="h-5 my-auto"
            width={60}
            height={60}
          />
        </Link>
        <div className="flex items-center space-x-2">
          <Button variant="link" asChild>
            <Link href="TODO">TODO</Link>
          </Button>

          <details className="dropdown dropdown-end">
            <summary
              tabIndex={Number(0)}
              id="mobile-drawer-toggle"
              className="text-2xl ri-menu-fill btn btn-ghost text-primary"
            />
            <ul
              tabIndex={Number(0)}
              id="mobile-drawer"
              className="z-20 flex flex-col w-screen p-4 space-y-4 font-semibold bg-white rounded-b-lg shadow-lg dropdown-content"
            >
              {pages.map((page, i) => (
                <li key={i}>
                  <Link href={page.relativePath}>{page.name}</Link>
                </li>
              ))}
            </ul>
          </details>
        </div>
      </div>
    </nav>
  );
}
