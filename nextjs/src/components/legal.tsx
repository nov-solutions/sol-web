import "../../public/static/css/styles.css";

export default function Legal({
    legalBG,
    legalCopyColor,
    legalCopy,
}: {
    legalBG: string;
    legalCopyColor: string;
    legalCopy: string;
}) {

  return (
    <div className={"flex-grow px-4 py-12 lg:px-0 " + legalBG}>
      <div className="flex flex-col mx-auto lg:w-2/3">
        <p className={legalCopyColor}>{legalCopy}</p>
      </div>
    </div>
  );
}
