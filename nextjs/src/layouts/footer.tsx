import "../../public/static/css/styles.css";

import Link from "next/link";

export default function Footer({
  footerDividerColor,
  footerLogoFileName,
  SITE_NAME,
  pages,
  pagesLocs,
  footerPagesColor,
  footerTaglineColor,
  footerTagline,
  socialsLocs,
  socialsColor,
  socialsIcons,
  legal,
  legalLocs,
  legalColor,
  footerFinePrintColor,
}: {
  footerDividerColor: string;
  footerLogoFileName: string;
  SITE_NAME: string;
  pages?: string[];
  pagesLocs?: string[];
  footerPagesColor?: string;
  footerTaglineColor: string;
  footerTagline: string;
  socialsLocs?: string[];
  socialsColor?: string;
  socialsIcons?: string[];
  legal?: string[];
  legalLocs?: string[];
  legalColor?: string;
  footerFinePrintColor: string;
}) {
  const pagesHTML =
    pages && pagesLocs && footerPagesColor
      ? pages.map((page, i) => (
            <Link key={page[i]} href={pagesLocs[i]} className={"font-semibold text-opacity-50 lg:hover:text-opacity-100 " + footerPagesColor}>
              {page}
            </Link>
        ))
      : null;
      
  const socialsHTML =
    socialsLocs && socialsColor && socialsIcons ? (
      <div className="flex items-center space-x-4">
        {socialsLocs.map((socialLoc, i) => (
          <Link key={socialLoc[i]} href={socialsLocs[i]} target="_blank" className={"text-opacity-50 lg:hover:text-opacity-100 " + socialsColor}>
            <i className={"text-xl " + socialsIcons[i]}></i>
          </Link>
        ))}
      </div>
    ) : null;

    const legalHTML =
    legal && legalLocs && legalColor ? (
      <div className="flex items-center space-x-4">
        {legal.map((legal, i) => (
          <Link key={legalLocs[i]} href={legalLocs[i]} target="_blank" className={"text-opacity-50 lg:hover:text-opacity-100 " + legalColor}>
            {legal}
          </Link>
        ))}
      </div>
    ) : null;

  return (
    <footer className="w-full py-4">
      <div className="flex flex-col justify-center px-4 mx-auto space-y-8 lg:px-0 lg:w-2/3">
        <hr className={"w-full border-t border-opacity-10 " + footerDividerColor }/>
        <div className="flex flex-col w-full space-y-8 text-sm lg:space-y-0 lg:justify-between lg:flex-row">
          <div className="flex flex-col space-y-4">
            <Link href="/">
              <img src={"/static/assets/img/logos/" + footerLogoFileName} alt={SITE_NAME + " logo"} className="h-5 my-auto" />
            </Link>
            <p className={"font-medium " + footerTaglineColor}>{footerTagline}</p>
            {socialsHTML}
            {legalHTML}
          </div>
          <div className="flex space-x-4">
            {pagesHTML}
          </div>
        </div>
        <div className={"text-xs self-end " + footerFinePrintColor}>
          <p>{"© " + new Date().getFullYear() + " " + SITE_NAME}</p>
        </div>
      </div>
    </footer>
  );
}
