import "../../public/static/css/styles.css";

import Link from "next/link";

export default function ErrorPage({
  logoFileName,
  SITE_NAME,
  statusCode,
  statusDescription,
}: {
  logoFileName: string;
  SITE_NAME: string;
  statusCode: string;
  statusDescription: string;
}) {
  return (
    <section className="flex flex-col items-center justify-center flex-grow px-4 py-24 mx-auto space-y-4 lg:w-1/2 lg:px-0">
      <img className="w-1/6 lg:w-1/12" src={"/static/assets/img/logos/" + logoFileName} alt={SITE_NAME + " logo"} />
      <div className="flex items-center space-x-2 divide-x divide-gray-light divide-opacity-25">
        <h1 className="text-lg font-medium text-primary">{statusCode}</h1>
        <h2 className="pl-2 text-white">{statusDescription}</h2>
      </div>
      <Link href="/" className="btn btn-sm btn-primary">
        Home
      </Link>
    </section>
  );
}
