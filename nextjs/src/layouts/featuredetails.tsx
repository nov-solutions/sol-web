import "../../public/static/css/styles.css";

export default function FeatureDetails({
    featureDetailsBG,
    featureDetailsSupertitleColor,
    featureDetailsSupertitle,
    featureDetailsTitleColor,
    featureDetailsTitle,
    featureDetailsSubtitleColor,
    featureDetailsSubtitle,
    detailOneIcon,
    detailsTitleColor,
    detailOneTitle,
    detailsDescriptionColor,
    detailOneDescription,
    detailTwoIcon,
    detailTwoTitle,
    detailTwoDescription,
    detailThreeIcon,
    detailThreeTitle,
    detailThreeDescription
}: {
    featureDetailsBG: string;
    featureDetailsSupertitleColor: string;
    featureDetailsSupertitle: string;
    featureDetailsTitleColor: string;
    featureDetailsTitle: string;
    featureDetailsSubtitleColor: string;
    featureDetailsSubtitle: string;
    detailOneIcon: string;
    detailsTitleColor: string;
    detailOneTitle: string;
    detailsDescriptionColor: string;
    detailOneDescription: string;
    detailTwoIcon: string;
    detailTwoTitle: string;
    detailTwoDescription: string;
    detailThreeIcon: string;
    detailThreeTitle: string;
    detailThreeDescription: string;
}) {

  return (
    <div className={"px-4 py-24 lg:px-0 " + featureDetailsBG}>
      <div className="flex flex-col items-center mx-auto space-y-4 lg:w-2/3">
        <p className={"text-xs text-center font-semibold uppercase " + featureDetailsSupertitleColor}>{featureDetailsSupertitle}</p>
        <h3 className={"!mt-2 text-3xl text-center font-semibold tracking-tight leading-none " + featureDetailsTitleColor}>{featureDetailsTitle}</h3>
        <p className={"font-medium text-center " + featureDetailsSubtitleColor}>{featureDetailsSubtitle}</p>
        <div className="grid grid-cols-1 place-items-center lg:place-items-start !mt-8 gap-8 lg:grid-cols-3">
          <div className="flex flex-col w-3/4 p-8 space-y-2 rounded-lg lg:w-auto">
            <h4 className={"font-semibold " + detailsTitleColor}><i className={"mr-2 " + detailOneIcon}></i>{detailOneTitle}</h4>
            <p className={"text-sm" + detailsDescriptionColor}>{detailOneDescription}</p>
          </div>
          <div className="flex flex-col w-3/4 p-8 space-y-2 rounded-lg lg:w-auto">
            <h4 className={"font-semibold " + detailsTitleColor}><i className={"mr-2 " + detailTwoIcon}></i>{detailTwoTitle}</h4>
            <p className={"text-sm" + detailsDescriptionColor}>{detailTwoDescription}</p>
          </div>
          <div className="flex flex-col w-3/4 p-8 space-y-2 rounded-lg lg:w-auto">
            <h4 className={"font-semibold " + detailsTitleColor}><i className={"mr-2 " + detailThreeIcon}></i>{detailThreeTitle}</h4>
            <p className={"text-sm" + detailsDescriptionColor}>{detailThreeDescription}</p>
          </div>
        </div>
    </div>
    </div>
  );
}
