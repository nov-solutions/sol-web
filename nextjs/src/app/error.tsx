'use client';

import { Metadata, Viewport } from "next";

import RootLayout from "./layout";
import ErrorPage from "@/layouts/errorpage";
import Body from "@/layouts/body";

// TODO: THIS DONT WORK
const SITE_NAME = String(process.env.SITE_NAME).replace(/\b\w/g, (char) => char.toUpperCase());

const logoFileName = "TODO";
const statusCode = "500";
const statusDescription = "Something went wrong!";


export const viewport: Viewport = {
  width: "device-width",
  height: "device-height",
  initialScale: 1,
  minimumScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: "cover",
  themeColor: "#000000",
};

export default function Error() {
  return (
    <RootLayout>
      <Body bodyBG={"bg-black"}>
        <ErrorPage
          logoFileName={logoFileName}
          // TODO: THIS DONT WORK
          SITE_NAME={SITE_NAME}
          statusCode={statusCode}
          statusDescription={statusDescription}
        />
      </Body>
    </RootLayout>
  );
}
