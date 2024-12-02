import "../../../public/static/css/styles.css";

export default function FinalCTA() {
  return (
    <div className="px-4 py-24 bg-primary lg:px-0">
      <div className="grid items-center gap-8 p-8 mx-auto lg:grid-cols-2 lg:w-2/3">
        <div className="flex flex-col items-center space-y-4 text-center lg:items-start lg:text-left">
          <h3 className="text-4xl font-bold leading-none tracking-tighter text-white">
            TODO
          </h3>
          <p className="font-medium lg:text-lg text-gray-light">
            TODO
          </p>
          <a
            href="TODO"
            className="w-fit btn btn-accent"
          >
            TODO
          </a>
        </div>
        <img
          src="/static/assets/img/TODO"
          alt="TODO"
          className="mx-auto rounded-lg"
        />
      </div>
    </div>
  );
}
