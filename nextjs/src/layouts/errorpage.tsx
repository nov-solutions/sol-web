import Link from "next/link";

import { SITE_NAME } from "@/constants";

export default function ErrorPage({
  statusCode,
  statusDescription,
}: {
  statusCode: string;
  statusDescription: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center h-[100dvh] px-4 lg:px-0 bg-black">
      <div className="flex flex-col items-center space-y-4 lg:w-1/5">
        <img
          className="w-10 aspect-square"
          src="/static/assets/img/logos/logo.png"
          alt={SITE_NAME + " logo"}
        />
        <div className="!mt-2 flex items-center space-x-2 divide-x divide-gray-light divide-opacity-25">
          <h1 className="font-bold leading-none tracking-tight text-primary">
            {statusCode}
          </h1>
          <h2 className="pl-2 text-white">{statusDescription}</h2>
        </div>
        <Link href="/" className="btn btn-sm btn-primary">
          Home
        </Link>
      </div>
    </div>
  );
}
