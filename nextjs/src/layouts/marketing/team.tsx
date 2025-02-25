export default function Team() {
  const team = [
    {
      headshotLoc: "TODO",
      name: "TODO",
      role: "TODO",
      linkedInLoc: "https://www.linkedin.com/in/TODO/",
    },
  ];

  return (
    <div className="flex-grow px-4 py-12 bg-white lg:px-0">
      <div className="grid items-stretch gap-4 mx-auto lg:grid-cols-4 lg:w-2/3">
        {team.map((teammate, i) => (
          <div
            key={i}
            className="flex flex-col items-center justify-center w-full h-full p-4 text-center border rounded-lg shadow-lg lg:p-8 border-gray-light"
          >
            <img
              src={`/assets/img/headshots/${teammate.headshotLoc}`}
              alt={`${teammate.name}'s headshot`}
              className="w-1/2 mx-auto rounded-full filter grayscale"
            />
            <h2 className="mt-4 text-sm font-medium">{teammate.name}</h2>
            <h3 className="text-xs text-gray">{teammate.role}</h3>
            <a
              href={teammate.linkedInLoc}
              target="_blank"
              className="mt-4 w-fit"
            >
              <i className="h-5 ri-linkedin-fill lg:text-black/75 hover:text-black"></i>
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
