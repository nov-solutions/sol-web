import "../../public/static/css/styles.css";

import Link from "next/link";

export default function FinalCTA({
    finalCTABG,
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
    <div className="px-4 py-24 lg:px-0">
      <div className={"grid items-center gap-8 mx-auto lg:grid-cols-2 lg:w-2/3 p-8 rounded-lg shadow-lg " + finalCTABG}>
        <div className="flex flex-col space-y-4">
            <h3 className={"!mt-2 text-3xl font-semibold tracking-tight leading-none " + finalCTATitleColor}>{finalCTATitle}</h3>
            <p className={"font-medium " + finalCTASubtitleColor}>{finalCTASubtitle}</p>
            <Link href={finalCTALoc} className="text-white w-fit btn btn-sm btn-primary">{finalCTA}</Link>
        </div>
        <img src={"/static/assets/img/" + finalCTAImageFileName} alt={finalCTAImageAlt} className="mx-auto rounded-lg shadow-lg" />
      </div>
    </div>
  );
}
