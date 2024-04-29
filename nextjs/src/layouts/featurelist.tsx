import "../../public/static/css/styles.css";

export default function FeatureList({
    featureListBG,
    featureListImageFileName,
    featureListImageAlt,
    featureListSupertitleColor,
    featureListSupertitle,
    featureListItemOneTextColor,
    featureListItemOneIcon,
    featureListItemOneText,
    featureListItemTwoTextColor,
    featureListItemTwoIcon,
    featureListItemTwoText,
    featureListItemThreeTextColor,
    featureListItemThreeIcon,
    featureListItemThreeText,
}: {
    featureListBG: string;
    featureListImageFileName: string;
    featureListImageAlt: string;
    featureListSupertitleColor: string;
    featureListSupertitle: string;
    featureListItemOneTextColor: string;
    featureListItemOneIcon: string;
    featureListItemOneText: string;
    featureListItemTwoTextColor: string;
    featureListItemTwoIcon: string;
    featureListItemTwoText: string;
    featureListItemThreeTextColor: string;
    featureListItemThreeIcon: string;
    featureListItemThreeText: string;
}) {

  return (
    <div className="px-4 py-24 lg:px-0">
      <div className={"grid items-center gap-8 mx-auto lg:grid-cols-2 lg:w-2/3 p-8 rounded-lg " + featureListBG}>
        <img src={"/static/assets/img/" + featureListImageFileName} alt={featureListImageAlt} className="w-3/4 mx-auto rounded-lg shadow-lg" />
        <div className="flex flex-col space-y-16">
          <p className={"text-xs self-center lg:self-start font-semibold uppercase " + featureListSupertitleColor}>{featureListSupertitle}</p>
          <div className={"!mt-4 flex items-center space-x-2 " + featureListItemOneTextColor}>
            <i className="mr-2 material-icons">{featureListItemOneIcon}</i>
            <h3 className="text-3xl font-semibold leading-none tracking-tight">{featureListItemOneText}</h3>
          </div>
          <div className={"flex items-center space-x-2 " + featureListItemTwoTextColor}>
            <i className="mr-2 material-icons">{featureListItemTwoIcon}</i>
            <h3 className="text-3xl font-semibold leading-none tracking-tight">{featureListItemTwoText}</h3>
          </div>
          <div className={"flex items-center space-x-2 " + featureListItemThreeTextColor}>
            <i className="mr-2 material-icons">{featureListItemThreeIcon}</i>
            <h3 className="text-3xl font-semibold leading-none tracking-tight">{featureListItemThreeText}</h3>
          </div>
        </div>
      </div>
    </div>
  );
}
