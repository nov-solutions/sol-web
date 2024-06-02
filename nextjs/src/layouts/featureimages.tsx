import "../../public/static/css/styles.css";

export default function FeatureImages({
    featureImagesBG,
    featureImagesTitleColor,
    featureImagesTitle,
    featureImagesSubtitleColor,
    featureImagesSubtitle,
    imagesCardBG,
    imageOneFileName,
    imageOneAlt,
    imagesTitleColor,
    imageOneTitle,
    imagesDescriptionColor,
    imageOneDescription,
    imageTwoFileName,
    imageTwoAlt,
    imageTwoTitle,
    imageTwoDescription,
    imageThreeFileName,
    imageThreeAlt,
    imageThreeTitle,
    imageThreeDescription
}: {
    featureImagesBG: string;
    featureImagesTitleColor: string;
    featureImagesTitle: string;
    featureImagesSubtitleColor: string;
    featureImagesSubtitle: string;
    imagesCardBG: string;
    imageOneFileName: string;
    imageOneAlt: string;
    imagesTitleColor: string;
    imageOneTitle: string;
    imagesDescriptionColor: string;
    imageOneDescription: string;
    imageTwoFileName: string;
    imageTwoAlt: string;
    imageTwoTitle: string;
    imageTwoDescription: string;
    imageThreeFileName: string;
    imageThreeAlt: string;
    imageThreeTitle: string;
    imageThreeDescription: string;
}) {

  return (
    <div className={"px-4 py-24 lg:px-0 " + featureImagesBG}>
      <div className="flex flex-col mx-auto space-y-8 text-left lg:text-center lg:items-center lg:w-2/3">
        <h3 className={"text-4xl font-semibold tracking-tight leading-none " + featureImagesTitleColor}>{featureImagesTitle}</h3>
        <p className={"!mt-2 text-2xl font-medium " + featureImagesSubtitleColor}>{featureImagesSubtitle}</p>
        <div className="grid gap-8 text-left lg:grid-cols-3">
          <div className={"flex flex-col p-8 space-y-4 rounded-lg " + imagesCardBG}>
            <img src={"/static/assets/img/" + imageOneFileName} alt={imageOneAlt} className="rounded-lg" />
            <h4 className={"text-lg font-semibold " + imagesTitleColor}>{imageOneTitle}</h4>
            <p className={"!mt-2 text-sm " + imagesDescriptionColor}>{imageOneDescription}</p>
          </div>
          <div className={"flex flex-col p-8 space-y-4 rounded-lg " + imagesCardBG}>
            <img src={"/static/assets/img/" + imageTwoFileName} alt={imageTwoAlt} className="rounded-lg" />
            <h4 className={"text-lg font-semibold " + imagesTitleColor}>{imageTwoTitle}</h4>
            <p className={"!mt-2 text-sm " + imagesDescriptionColor}>{imageTwoDescription}</p>
          </div>
          <div className={"flex flex-col p-8 space-y-4 rounded-lg " + imagesCardBG}>
            <img src={"/static/assets/img/" + imageThreeFileName} alt={imageThreeAlt} className="rounded-lg" />
            <h4 className={"text-lg font-semibold " + imagesTitleColor}>{imageThreeTitle}</h4>
            <p className={"!mt-2 text-sm " + imagesDescriptionColor}>{imageThreeDescription}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
