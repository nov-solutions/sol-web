import "../../public/static/css/styles.css";

import ProgressBarProvider from "@/providers/progressbarprovider";

export default function Body({
  children,
  bodyBG = "bg-white",
}: {
  children: React.ReactNode;
  bodyBG?: string;
}) {
  return (
    <body className={"flex min-h-[100dvh] lg:h-screen " + bodyBG}>
      <ProgressBarProvider>
        {children}
      </ProgressBarProvider>
    </body>
  );
}
