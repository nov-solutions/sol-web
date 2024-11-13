import "../../public/static/css/styles.css";

export default function Title({ title }: { title: string }) {
  return (
    <div className="px-4 pt-24 pb-12 lg:pt-36 lg:px-0">
      <div className="flex flex-col mx-auto lg:w-2/3">
        <h1 className="text-3xl font-bold leading-none tracking-tighter">
          {title}
        </h1>
      </div>
    </div>
  );
}
