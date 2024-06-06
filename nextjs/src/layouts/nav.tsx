'use client';

import "../../public/static/css/styles.css";

import { useEffect } from "react";

import Link from "next/link";

export default function Nav({
  navBG,
  navLogoFileName,
  SITE_NAME,
  pages,
  pagesLocs,
  navPagesColor,
  cta,
  ctaLoc,
  mobileDrawerToggleColor,
}: {
  navBG: string;
  navLogoFileName: string;
  SITE_NAME: string;
  pages?: string[];
  pagesLocs?: string[];
  navPagesColor?: string;
  cta?: string;
  ctaLoc?: string;
  mobileDrawerToggleColor: string;
}) {
  const pagesCTAHTML =
    pages && pagesLocs && navPagesColor ? (
      <div className="items-center hidden space-x-4 font-semibold lg:flex">
        {pages.map((page, i) => (
          <Link key={page[i]} href={pagesLocs[i]} className={"text-opacity-50 lg:hover:text-opacity-100 " + navPagesColor}>
            {page}
          </Link>
        ))}
        {cta && ctaLoc ? (
          <Link href={ctaLoc} className="text-white btn btn-sm btn-primary">
            {cta}
          </Link>
        ) : null}
      </div>
    ) : null;

    const mobilePagesCTAHTML =
    pages && pagesLocs && navPagesColor ? (
      <ul
        tabIndex={Number(0)}
        id="mobile-drawer"
        className={"z-20 dropdown-content flex flex-col p-4 space-y-4 font-semibold dropdown-end fixed left-0 top-[7.5vh] w-screen shadow-gray/10 shadow-[inset_0px_-1px_1px] " + navBG + " " + navPagesColor}
      >
        {pages.map((page, i) => (
          <li key={i}>
            <Link href={pagesLocs[i] } className="text-xl">{page}</Link>
          </li>
        ))}
        {cta && ctaLoc ? (
          <li key={ctaLoc}>
            <Link href={ctaLoc} className="text-white btn btn-sm btn-primary">{cta}</Link>
          </li>
        ) : null}
      </ul>
    ) : null;

      useEffect(() => {
        const navBar = document.getElementById("navbar");
        const mobileDrawerToggle = document.getElementById("mobile-drawer-toggle");

        if (navBar && mobileDrawerToggle) {
          mobileDrawerToggle.addEventListener("click", () => {
            navBar.classList.remove("bg-opacity-75", "shadow-gray/10", "shadow-[inset_0px_-1px_1px]");
            navBar.classList.add("bg-opacity-100");
          });
          document.addEventListener("click", (e) => {
            if (e.target !== mobileDrawerToggle) {
              navBar.classList.add("bg-opacity-75", "shadow-gray/10", "shadow-[inset_0px_-1px_1px]");
              navBar.classList.remove("bg-opacity-100");
            }
          });
        }
      },
    );

  return (
    <nav
      id="navbar"
      className={"fixed top-0 left-0 z-10 w-full h-[7.5vh] bg-opacity-75 backdrop-blur-sm shadow-gray/10 shadow-[inset_0px_-1px_1px] " + navBG}
    >
      <div className="items-center justify-between hidden w-2/3 h-full px-0 mx-auto text-sm lg:flex">
        <Link href="/" className="flex items-center">
          <img src={"/static/assets/img/logos/" + navLogoFileName} alt={SITE_NAME + " logo"} className="h-5 my-auto" />
        </Link>

        {pagesCTAHTML}
      </div>

      <div className="flex items-center justify-between w-full h-full px-4 dropdown lg:hidden">
        <Link href="/" className="flex items-center">
          <img src={"/static/assets/img/logos/" + navLogoFileName} alt={SITE_NAME + " logo"} className="h-5 my-auto" />
        </Link>

        <div tabIndex={Number(0)} id="mobile-drawer-toggle" className={"text-xl ri-menu-fill " + mobileDrawerToggleColor}></div>
        {mobilePagesCTAHTML}
      </div>
    </nav>
  );
}
