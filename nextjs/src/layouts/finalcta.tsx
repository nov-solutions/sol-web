import "../../public/static/css/styles.css";

import Link from "next/link";

export default function FinalCTA({
    finalCTABG,
    finalCTACardBG,
    finalCTATitleColor,
    finalCTATitle,
    finalCTASubtitleColor,
    finalCTASubtitle,
    finalCTAImageFileName,
    finalCTAImageAlt,
    finalCTALoc,
    finalCTA
}: {
    finalCTABG: string;
    finalCTACardBG: string;
    finalCTATitleColor: string;
    finalCTATitle: string;
    finalCTASubtitleColor: string;
    finalCTASubtitle: string;
    finalCTAImageFileName: string;
    finalCTAImageAlt: string;
    finalCTALoc: string;
    finalCTA: string;
}) {

  return (
    <div className={"px-4 py-24 lg:px-0 " + finalCTABG}>
      <div className={"grid items-center gap-8 mx-auto lg:grid-cols-2 lg:w-2/3 p-8 rounded-lg " + finalCTACardBG}>
        <div className="flex flex-col items-center space-y-4 text-center lg:items-start lg:text-left">
            <h3 className={"text-4xl font-bold tracking-tight leading-none " + finalCTATitleColor}>{finalCTATitle}</h3>
            <p className={"!mt-2 text-2xl font-medium " + finalCTASubtitleColor}>{finalCTASubtitle}</p>
            <Link href={finalCTALoc} className="text-white w-fit btn btn-sm btn-primary">{finalCTA}</Link>
        </div>
        <img src={"/static/assets/img/" + finalCTAImageFileName} alt={finalCTAImageAlt} className="mx-auto rounded-lg" />
      </div>
    </div>
  );
}
