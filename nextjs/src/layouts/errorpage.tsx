import "../../public/static/css/styles.css";

import Link from "next/link";

export default function ErrorPage({
  statusCode,
  statusDescription,
}: {
  statusCode: string;
  statusDescription: string;
}) {
  return (
    <>
      <img
        className="w-10 aspect-square"
        src="/static/assets/img/logos/TODO"
        alt="TODO"
      />
      <div className="!mt-2 flex items-center space-x-2 divide-x divide-gray-light divide-opacity-25">
        <h1 className="font-bold leading-none tracking-tight text-primary">{statusCode}</h1>
        <h2 className="pl-2 text-white">{statusDescription}</h2>
      </div>
      <Link href="/" className="btn btn-sm btn-primary">
        Home
      </Link>
    </>
  );
}
