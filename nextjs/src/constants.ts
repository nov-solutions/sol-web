export const SITE_NAME = String(process.env.NEXT_PUBLIC_SITE_NAME).replace(
  /\b\w/g,
  (char) => char.toUpperCase(),
);
// TODO: update tagline, description
export const SITE_TAGLINE = "Rock Bottom";
export const SITE_DESCRIPTION = "Software";
export const SITE_BASE_DOMAIN = String(
  process.env.NEXT_PUBLIC_SITE_BASE_DOMAIN,
);

export interface Page {
  name: string;
  relativePath: string;
  appPage?: boolean;
  icon?: string;
  external?: boolean;
}
export const PAGES: Page[] = [{ name: "Home", relativePath: "/" }];
