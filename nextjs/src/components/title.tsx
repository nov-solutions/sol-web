import "../../public/static/css/styles.css";

export default function Title({
    titleBG,
    titleColor,
    titleText,
}: {
    titleBG: string;
    titleColor: string;
    titleText: string;
}) {

  return (
    <div className={"mt-[7.5vh] py-12 px-4 lg:px-0 " + titleBG}>
      <div className="flex flex-col mx-auto lg:w-2/3">
        <h1 className={"text-3xl font-bold leading-none tracking-tight " + titleColor}>{titleText}</h1>
      </div>
    </div>
  );
}
