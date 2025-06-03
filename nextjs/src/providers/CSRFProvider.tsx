"use client";

import { useEffect } from "react";
import { initializeCSRF } from "@/utils/axios";

// A client component that initializes CSRF
export default function CSRFProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  useEffect(() => {
    // Initialize CSRF token when the component mounts
    initializeCSRF();
  }, []);

  return <>{children}</>;
}
