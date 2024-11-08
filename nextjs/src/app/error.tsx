'use client';

import { Viewport } from "next";

import RootLayout from "./layout";
import ErrorPageContainer from "@/layouts/errorpagecontainer";
import ErrorPage from "@/layouts/errorpage";
import Body from "@/layouts/body";

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
        <ErrorPageContainer>
          <ErrorPage
            statusCode={statusCode}
            statusDescription={statusDescription}
          />
        </ErrorPageContainer>
      </Body>
    </RootLayout>
  );
}
