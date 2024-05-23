import "../../public/static/css/styles.css";

export default function Heading({
    headingBG,
    headingColor,
    heading,
}: {
    headingBG: string;
    headingColor: string;
    heading: string;
}) {

  return (
    <div className={"px-4 py-24 lg:px-0 " + headingBG}>
      <div className="flex flex-col items-center mx-auto text-center lg:w-1/2">
        <h3 className={"text-3xl font-semibold tracking-tight leading-none " + headingColor}>{heading}</h3>
      </div>
    </div>
  );
}
