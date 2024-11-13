import AppNav from "@/layouts/appnav";

const AppPageContainer = ({
  currentNavPage,
  children,
}: {
  currentNavPage: string;
  children: React.ReactNode;
}) => {
  return (
    <>
      <AppNav currentNavPage={currentNavPage} />
      <div className="flex flex-col w-full min-h-full p-16 space-y-8 overflow-y-auto bg-white">
        {children}
      </div>
    </>
  );
};

export default AppPageContainer;
