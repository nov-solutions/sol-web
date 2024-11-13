import "../../public/static/css/styles.css";

export default function AppTitle({ title }: { title: string }) {
  return (
    <h1 className="text-3xl font-bold leading-none tracking-tight">{title}</h1>
  );
}
