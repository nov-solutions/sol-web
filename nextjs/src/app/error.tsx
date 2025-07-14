"use client";

import ErrorLayout from "@/layouts/errorpage";

export default function Error({
  error,
}: {
  error: Error & { cause?: { code?: string } };
}) {
  return (
    <ErrorLayout
      statusCode={error.cause?.code ?? "500"}
      statusDescription={error.message ?? "Something went wrong!"}
    />
  );
}
