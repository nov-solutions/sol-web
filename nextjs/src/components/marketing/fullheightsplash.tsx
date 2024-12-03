import "../../../public/static/css/styles.css";

import { SITE_NAME } from "@/constants";

export default function FullHeightSplash() {
  return (
    <div className="flex justify-center h-[100dvh] px-4 lg:px-0">
      <div className="grid items-center gap-16 mx-auto lg:grid-cols-2 lg:w-2/3">
        <div className="flex flex-col items-center space-y-4 text-center lg:items-start lg:text-left">
          <img
            src="/static/assets/img/logos/logo.png"
            alt={SITE_NAME + " logo"}
            className="w-1/6 lg:w-1/12"
          />
          <h1 className="!mt-2 text-4xl lg:text-6xl font-bold leading-none tracking-tighter text-primary">
            TODO
          </h1>
          <h2 className="font-medium lg:text-lg text-gray">TODO</h2>
          <a href="TODO" className="text-left text-white w-fit btn btn-primary">
            TODO
          </a>
        </div>
        <img src="/static/assets/img/TODO" alt="TODO" className="lg:mx-auto" />
      </div>
    </div>
  );
}
