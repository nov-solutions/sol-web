export const SITE_NAME = String(process.env.NEXT_PUBLIC_SITE_NAME).replace(
    /\b\w/g,
    (char) => char.toUpperCase(),
);
export const SITE_TAGLINE = String(process.env.NEXT_PUBLIC_SITE_TAGLINE);
export const SITE_DESCRIPTION = String(process.env.NEXT_PUBLIC_SITE_DESCRIPTION);
export const SITE_BASE_DOMAIN = String(process.env.NEXT_PUBLIC_SITE_BASE_DOMAIN);

export interface Page {
    name: string;
    relativePath: string;
    appPage?: boolean;
    icon?: string;
    external?: boolean;
  }
  export const PAGES: Page[] = [
    { name: "Home", relativePath: "/" },
  ];