const ErrorPageContainer = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex flex-col items-center justify-center flex-grow w-full px-4 lg:px-0">
      <div className="flex flex-col items-center space-y-4 lg:w-1/5">
        {children}
      </div>
    </div>
  );
};

export default ErrorPageContainer;
