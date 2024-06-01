import "../../public/static/css/styles.css";

import Link from "next/link";

export default function Splash({
  splashBG,
  splashLogoFileName,
  SITE_NAME,
  splashTitleColor,
  splashTitle,
  splashSubtitleColor,
  splashSubtitle,
  ctaLoc,
  splashCTA,
  splashImageFileName,
  splashImageAlt,
}: {
  splashBG: string;
  splashLogoFileName: string;
  SITE_NAME: string;
  splashTitleColor: string;
  splashTitle: string;
  splashSubtitleColor: string;
  splashSubtitle: string;
  ctaLoc: string;
  splashCTA: string;
  splashImageFileName: string;
  splashImageAlt: string;
}) {

  return (
    <div className={"mt-[7.5vh] px-4 py-12 lg:py-24 lg:px-0 " + splashBG}>
      <div className="grid items-center gap-16 mx-auto lg:grid-cols-2 lg:w-2/3">
        <div className="flex flex-col items-center space-y-4 text-center lg:items-start lg:text-left">
          <img src={"/static/assets/img/logos/" + splashLogoFileName} alt={SITE_NAME + " logo"} className="w-1/12" />
          <h1 className={"text-6xl font-bold leading-none tracking-tight " + splashTitleColor}>{splashTitle}</h1>
          <h2 className={"!mt-2 text-xl font-medium w-fit " + splashSubtitleColor}>{splashSubtitle}</h2>
          <Link href={ctaLoc} className="text-left text-white w-fit btn btn-sm btn-primary">{splashCTA}</Link>
        </div>
        <img src={"/static/assets/img/" + splashImageFileName} alt={splashImageAlt} className="lg:mx-auto" />
      </div>
    </div>
  );
}
