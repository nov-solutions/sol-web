'use client';

import "../../public/static/css/styles.css";

import Link from "next/link";

export default function AppNav({
  appNavBG,
  SITE_NAME,
  currentNavPage,
  navPages,
  navPagesIcons,
  navPagesLocs,
  navPagesCurrentDisplay,
  navPagesHoverInteraction,
  navPagesColor,
  appNavLogoLoc,
  appNavLogoFileName,
  SITE_BASE_DOMAIN,
  signOutLoc,
}: {
  appNavBG: string;
  SITE_NAME: string;
  currentNavPage: string;
  navPages: string[];
  navPagesLocs: string[];
  navPagesCurrentDisplay: string;
  navPagesHoverInteraction: string;
  navPagesColor: string;
  navPagesIcons: string[];
  appNavLogoLoc: string;
  appNavLogoFileName: string;
  SITE_BASE_DOMAIN: string;
  signOutLoc: string;
}) {

  const navPagesHTML = (
    <ul className="space-y-2">
      {navPages.map((navPage, i) => (
        <li key={navPage[i]}>
          <Link href={navPagesLocs[i]} className={currentNavPage == navPage ? "p-2 flex font-medium rounded-lg " + navPagesCurrentDisplay + " " + navPagesColor : "p-2 flex font-medium rounded-lg " + navPagesHoverInteraction + " " + navPagesColor}>
            <i className={"mr-2 " + navPagesIcons[i]}></i>
            {navPage}
          </Link>
        </li>
      ))}
    </ul>
  );

  const sideNavHTML = (
    <nav
      className={"fixed top-[7.5vh] left-0 h-full lg:w-64 z-10 border-r border-gray border-opacity-10 " + appNavBG}>
      <div className="flex flex-col p-4">
        {navPagesHTML}
      </div>
    </nav>
  );

  const topNavHTML = (
    <nav
      className={"fixed place-items-center top-0 left-0 w-full z-10 h-[7.5vh] border-b border-gray border-opacity-10 " + appNavBG}>
      <div className="flex justify-between h-full px-8 text-sm">
        <Link href={appNavLogoLoc} className="my-auto h-1/2">
          <img src={"/static/assets/img/logos/" + appNavLogoFileName} alt={SITE_NAME + " logo"} className="h-full" />
        </Link>
        <div className="flex flex-col my-auto space-y-4 h-1/2 my dropdown dropdown-bottom dropdown-end">
          <div tabIndex={Number(0)} className="h-full">
            <img src="https://docs.material-tailwind.com/img/face-2.jpg" alt={"Account avatar"} className="h-full rounded-full hover:cursor-pointer" />
          </div>
          <div className="z-20 w-32 bg-white rounded-lg shadow-lg dropdown-content menu">
            <li>
              <Link href={SITE_BASE_DOMAIN + signOutLoc}>
                Sign out
              </Link>
            </li>
          </div>
        </div>
      </div>
    </nav>
  );

  return (
    <>
      {sideNavHTML}
      {topNavHTML}
    </>
  );
}
