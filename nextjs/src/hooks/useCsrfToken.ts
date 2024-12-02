import axios from "axios";

import { useState, useEffect } from "react";

export default function useCsrfToken({
  SITE_BASE_DOMAIN,
}: {
  SITE_BASE_DOMAIN: string;
}) {

  const [csrfToken, setCsrfToken] = useState("");

  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await axios.get(`http://${SITE_BASE_DOMAIN}/api/get-csrf-token/`, {
          withCredentials: true,
        });
        const csrfToken = response.data.csrftoken;
        setCsrfToken(csrfToken);
      } catch (error) {
          console.error("Failed to fetch CSRF token:", error);
      }
    };

    fetchCsrfToken();
  }, [SITE_BASE_DOMAIN]);

  return csrfToken;
};
