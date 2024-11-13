import "../../public/static/css/styles.css";

export default function Splash() {
  return (
    <div className="px-4 pb-24 bg-white pt-36 lg:pt-48 lg:px-0">
      <div className="grid items-center gap-16 mx-auto lg:grid-cols-2 lg:w-2/3">
        <div className="flex flex-col items-center space-y-4 text-center lg:items-start lg:text-left">
          <img
            src="/static/assets/img/logos/app.png"
            alt="Logo"
            className="w-1/6 lg:w-1/12"
          />
          <h1 className="!mt-2 text-4xl lg:text-6xl font-bold leading-none tracking-tighter text-primary">
            TODO
          </h1>
          <h2 className="font-medium lg:text-lg text-gray">TODO</h2>
          <a href="TODO" className="text-left text-white w-fit btn btn-primary">
            TODO
          </a>
        </div>
        <img
          src="/static/assets/img/mockup.png"
          alt="Mockup"
          className="lg:mx-auto"
        />
      </div>
    </div>
  );
}
