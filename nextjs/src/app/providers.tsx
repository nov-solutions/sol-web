import ProgressBarProvider from "@/providers/progressBarProvider";
import { ThemeProvider } from "@/providers/theme-provider";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ProgressBarProvider>
      <ThemeProvider
        attribute="class"
        defaultTheme="dark"
        enableSystem
        disableTransitionOnChange
      >
        {children}
      </ThemeProvider>
    </ProgressBarProvider>
  );
}
