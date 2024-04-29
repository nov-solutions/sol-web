import "../../public/static/css/styles.css";

export default function Content({
    contentBG,
    contentSupertitleColor,
    contentSupertitle,
    contentTitleColor,
    contentTitle,
    contentSubtitleColor,
    contentSubtitle,
    contentImageFileName,
    contentImageAlt
}: {
    contentBG: string;
    contentSupertitleColor: string;
    contentSupertitle: string;
    contentTitleColor: string;
    contentTitle: string;
    contentSubtitleColor: string;
    contentSubtitle: string;
    contentImageFileName: string;
    contentImageAlt: string;
}) {

  return (
    <div className={"px-4 py-24 lg:px-0 " + contentBG}>
        <div className="grid gap-8 mx-auto rounded-lg lg:grid-cols-2 lg:w-2/3">
            <div className="flex flex-col space-y-4 text-center lg:text-left lg:w-2/3">
                <p className={"text-xs font-semibold uppercase " + contentSupertitleColor}>{contentSupertitle}</p>
                <h3 className={"!mt-2 text-3xl font-semibold tracking-tight leading-none " + contentTitleColor}>{contentTitle}</h3>
                <p className={"font-medium " + contentSubtitleColor}>{contentSubtitle}</p>
            </div>
            <img src={"/static/assets/img/" + contentImageFileName} alt={contentImageAlt} className="w-3/4 mx-auto rounded-lg shadow-lg" />
        </div>
    </div>
  );
}
