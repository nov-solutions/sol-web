"use client";

import { useEffect } from "react";

import Link from "next/link";

import { PAGES, SITE_NAME } from "@/constants";

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
    <nav className="fixed top-0 left-0 z-10 w-full">
      <div className="items-center justify-between hidden w-1/2 h-full p-4 mx-auto mt-2 text-sm rounded-lg shadow-lg lg:flex backdrop-blur-lg bg-white/75">
        <Link href="/" className="flex items-center">
          <img
            src="/assets/img/logos/wordmark.png"
            alt={SITE_NAME + " wordmark"}
            className="h-5 my-auto"
          />
        </Link>
        <div className="items-center space-x-4 font-semibold">
          {pages.map((page, i) => (
            <Link
              key={i}
              href={page.relativePath}
              className="lg:text-black/75 hover:text-black"
            >
              {page.name}
            </Link>
          ))}
        </div>
        <a href="TODO" className="text-white btn btn-sm btn-primary">
          TODO
        </a>
      </div>

      <div
        id="mobile-navbar"
        className="flex items-center justify-between w-full h-full py-2 pl-4 rounded-b-lg shadow-lg lg:hidden bg-white/75 backdrop-blur-lg"
      >
        <Link href="/" className="flex items-center">
          <img
            src="/assets/img/logos/wordmark.png"
            alt={SITE_NAME + " wordmark"}
            className="h-5 my-auto"
          />
        </Link>
        <div className="flex items-center space-x-2">
          <a href="TODO" className="text-white btn btn-sm btn-primary">
            TODO
          </a>
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
