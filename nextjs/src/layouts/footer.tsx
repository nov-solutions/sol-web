import "../../public/static/css/styles.css";

import Link from "next/link";

export default function Footer({
  footerDividerColor,
  footerLogoFileName,
  SITE_NAME,
  pages,
  pagesLocs,
  footerPagesColor,
  socialsLocs,
  socialsColor,
  socialsIcons,
  footerFinePrintColor,
}: {
  footerDividerColor: string;
  footerLogoFileName: string;
  SITE_NAME: string;
  pages?: string[];
  pagesLocs?: string[];
  footerPagesColor?: string;
  socialsLocs?: string[];
  socialsColor?: string;
  socialsIcons?: string[];
  footerFinePrintColor: string;
}) {
  const pagesHTML =
    pages && pagesLocs && footerPagesColor
      ? pages.map((page, i) => (
          <Link key={page[i]} href={pagesLocs[i]} className={"text-opacity-50 lg:hover:text-opacity-100 " + footerPagesColor}>
            {page}
          </Link>
        ))
      : null;
  const socialsHTML =
    socialsLocs && socialsColor && socialsIcons ? (
      <div className="flex items-center space-x-4">
        {socialsLocs.map((socialLoc, i) => (
          <Link key={socialLoc[i]} href={socialsLocs[i]} target="_blank" className={"text-opacity-50 lg:hover:text-opacity-100 " + socialsColor}>
            <i className={"h-5 bi " + socialsIcons[i]}></i>
          </Link>
        ))}
      </div>
    ) : null;

  return (
    <footer className="h-[15vh] w-full">
      <div className="flex flex-col items-center justify-center h-full px-4 mx-auto space-y-4 text-xs lg:px-0 lg:w-1/2">
        <hr className={"w-full border-t border-opacity-25 " + footerDividerColor }/>
        <div className="flex justify-between w-full">
          <div className="flex items-center space-x-4">
            <Link href="/" className="flex items-center">
              <img src={"/static/assets/img/logos/" + footerLogoFileName} alt={SITE_NAME + " logo"} className="h-5 my-auto" />
            </Link>
            {pagesHTML}
          </div>
          {socialsHTML}
        </div>
        <div className={"flex items-center self-start " + footerFinePrintColor}>
          <p>{"© " + new Date().getFullYear() + " " + SITE_NAME}</p>
        </div>
      </div>
    </footer>
  );
}
