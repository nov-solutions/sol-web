import "../../public/static/css/styles.css";

export default function Body({ children, bodyBG }: { children: React.ReactNode; bodyBG: string }) {
  return <body className={"flex flex-col min-h-[100dvh] lg:min-h-[100vh] " + bodyBG}>{children}</body>;
}
