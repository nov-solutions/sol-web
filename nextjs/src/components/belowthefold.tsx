import "../../public/static/css/styles.css";

export default function BelowTheFold({
  belowTheFoldBG,
  sectionTitleLightColor,
  sectionSubtitleLightColor
}: {
  belowTheFoldBG: string;
  sectionTitleLightColor: string;
  sectionSubtitleLightColor: string;
}) {

  return (
    <div className={"px-4 py-24 lg:px-0 " + belowTheFoldBG}>
      <div className="flex flex-col items-center mx-auto space-y-4 text-left lg:text-center lg:w-1/2">
        <h3 className={"text-2xl font-semibold tracking-tight leading-none " + sectionTitleLightColor}></h3>
        <p className={"font-medium " + sectionSubtitleLightColor}></p>
      </div>
    </div>
  );
}
