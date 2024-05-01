import "../../public/static/css/styles.css";

export default function FullHeightSplash({
  splashBG,
  splashLogoFileName,
  SITE_NAME,
  splashTitleColor,
  splashTitle,
  splashSubtitleColor,
  splashSubtitle,
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
  splashImageFileName: string;
  splashImageAlt: string;
}) {

  return (
    <div className={"flex-grow mt-[7.5vh] px-4 py-12 lg:px-0 " + splashBG}>
      <div className="grid items-center h-full gap-16 mx-auto lg:grid-cols-2 lg:w-2/3">
        <div className="flex flex-col space-y-4 text-center lg:text-left">
          <img src={"/static/assets/img/logos/" + splashLogoFileName} alt={SITE_NAME + " logo"} className="w-1/12 mx-auto lg:mx-0" />
          <h1 className={"text-6xl font-bold leading-none tracking-tight " + splashTitleColor}>{splashTitle}</h1>
          <h2 className={"mx-auto text-lg lg:mx-0 w-fit " + splashSubtitleColor}>{splashSubtitle}</h2>
        </div>
        <img src={"/static/assets/img/" + splashImageFileName} alt={splashImageAlt} className="mx-auto" />
      </div>
    </div>
  );
}
