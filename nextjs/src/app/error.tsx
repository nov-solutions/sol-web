"use client";

import { Viewport } from "next";

import ErrorPage from "@/layouts/errorpage";

const statusCode = "500";
const statusDescription = "Something went wrong!";

export const viewport: Viewport = {
  themeColor: "#000000",
};

export default function Error() {
  return (
    <ErrorPage statusCode={statusCode} statusDescription={statusDescription} />
  );
}
