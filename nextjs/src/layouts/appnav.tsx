'use client';

import "../../public/static/css/styles.css";

import { useEffect } from "react";

import Link from "next/link";

export default function AppNav({
  navBG,
  navLogoFileName,
  SITE_NAME,
  pages,
  pagesLocs,
  navPagesColor,
  mobileDrawerToggleColor,
}: {
  navBG: string;
  navLogoFileName: string;
  SITE_NAME: string;
  pages?: string[];
  pagesLocs?: string[];
  navPagesColor?: string;
  mobileDrawerToggleColor: string;
}) {
  const pagesHTML =
    pages && pagesLocs && navPagesColor ? (
      <div className="items-center hidden space-x-4 font-semibold lg:flex">
        {pages.map((page, i) => (
          <Link key={page[i]} href={pagesLocs[i]} className={"text-opacity-50 lg:hover:text-opacity-100 " + navPagesColor}>
            {page}
          </Link>
        ))}
      </div>
    ) : null;

    const mobilePagesHTML =
    pages && pagesLocs && navPagesColor ? (
      <nav
        id="mobile-drawer"
        className={"z-20 dropdown-content dropdown-end fixed left-0 top-[7.5vh] w-screen border-b border-black border-opacity-10 " + navBG}
        >
      <ul className={"flex flex-col p-4 space-y-4 font-semibold text-center " + navPagesColor}>
        {pages.map((page, i) => (
          <li key={i}>
            <Link href={pagesLocs[i]}>{page}</Link>
          </li>
        ))}
      </ul>
      </nav>
    ) : null;

      useEffect(() => {
        const navBar = document.getElementById("navbar");
        const mobileDrawerToggle = document.getElementById("mobile-drawer-toggle");

        if (navBar && mobileDrawerToggle) {
          mobileDrawerToggle.addEventListener("click", () => {
            navBar.classList.remove("bg-opacity-75", "border-b");
            navBar.classList.add("bg-opacity-100");
          });
          document.addEventListener("click", (e) => {
            if (e.target !== mobileDrawerToggle) {
              navBar.classList.add("bg-opacity-75", "border-b");
              navBar.classList.remove("bg-opacity-100");
            }
          });
        }
      },
    );

  return (
    <nav
      id="navbar"
      className={"fixed top-0 left-0 z-10 w-full h-[7.5vh] bg-opacity-75 backdrop-blur-sm border-b border-black border-opacity-10 " + navBG}
    >
      <div className="items-center justify-between hidden w-2/3 h-full px-0 mx-auto text-sm lg:flex">
        <Link href="/" className="flex items-center">
          <img src={"/static/assets/img/logos/" + navLogoFileName} alt={SITE_NAME + " logo"} className="h-5 my-auto" />
        </Link>

        {pagesHTML}
      </div>

      <div className="flex items-center justify-between w-full h-full px-4 dropdown lg:hidden">
        <Link href="/" className="flex items-center">
          <img src={"/static/assets/img/logos/" + navLogoFileName} alt={SITE_NAME + " logo"} className="h-5 my-auto" />
        </Link>

        <button id="mobile-drawer-toggle" className={"h-full material-icons " + mobileDrawerToggleColor}> menu </button>
        {mobilePagesHTML}
      </div>
    </nav>
  );
}
