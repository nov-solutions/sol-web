import "../../public/static/css/styles.css";

export default function FeatureList({
    featureListBG,
    listsCardBG,
    featureListImageFileName,
    featureListImageAlt,
    featureListItemOneCardBG,
    featureListItemOneTextColor,
    featureListItemOneIcon,
    featureListItemOneText,
    featureListItemTwoCardBG,
    featureListItemTwoTextColor,
    featureListItemTwoIcon,
    featureListItemTwoText,
    featureListItemThreeCardBG,
    featureListItemThreeTextColor,
    featureListItemThreeIcon,
    featureListItemThreeText,
}: {
    featureListBG: string;
    listsCardBG: string;
    featureListImageFileName: string;
    featureListImageAlt: string;
    featureListItemOneCardBG: string;
    featureListItemOneTextColor: string;
    featureListItemOneIcon: string;
    featureListItemOneText: string;
    featureListItemTwoCardBG: string;
    featureListItemTwoTextColor: string;
    featureListItemTwoIcon: string;
    featureListItemTwoText: string;
    featureListItemThreeCardBG: string;
    featureListItemThreeTextColor: string;
    featureListItemThreeIcon: string;
    featureListItemThreeText: string;
}) {

  return (
    <div className={"px-4 py-24 lg:px-0 " + featureListBG}>
      <div className="flex flex-col mx-auto space-y-8 text-left lg:text-center lg:items-center lg:w-3/4">
        <div className="grid gap-8 text-left lg:grid-cols-5">
          <div className={"flex flex-col p-8 rounded-lg lg:col-span-3 " + listsCardBG}>
            <img src={"/static/assets/img/" + featureListImageFileName} alt={featureListImageAlt} className="rounded-lg shadow-lg" />
          </div>
          <div className={"flex flex-col p-8 lg:justify-evenly justify-normal space-y-8 lg:space-y-0 text-3xl lg:col-span-2 rounded-lg " + listsCardBG}>
            <div className={"flex space-x-2 rounded-lg p-4 " + featureListItemOneCardBG + " " + featureListItemOneTextColor}>
              <i className={"mr-2 " + featureListItemOneIcon}></i>
              <h3 className="font-semibold leading-none tracking-tight">{featureListItemOneText}</h3>
            </div>
            <div className={"flex space-x-2 rounded-lg p-4 " + featureListItemTwoCardBG + " " + featureListItemTwoTextColor}>
              <i className={"mr-2 " + featureListItemTwoIcon}></i>
              <h3 className="font-semibold leading-none tracking-tight">{featureListItemTwoText}</h3>
            </div>
            <div className={"flex space-x-2 rounded-lg p-4 " + featureListItemThreeCardBG + " " + featureListItemThreeTextColor}>
              <i className={"mr-2 " + featureListItemThreeIcon}></i>
              <h3 className="font-semibold leading-none tracking-tight">{featureListItemThreeText}</h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
