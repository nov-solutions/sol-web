import "../../public/static/css/styles.css";

import Link from "next/link";

export default function Team({
    teamBG,
    teamCardBG,
    team,
    teamCardNameColor,
    teamCardRoleColor,
    teamCardLinkedInIconColor,
}: {
    teamBG: string;
    teamCardBG: string;
    team: {headshotLoc: string, name: string, role: string, linkedInLoc: string}[];
    teamCardNameColor: string;
    teamCardRoleColor: string;
    teamCardLinkedInIconColor: string;
}) {
    const teamCardsHTML =
        team && teamCardNameColor && teamCardRoleColor
        ? team.map((teammate, i) => (
            <div key={i} className={"flex flex-col items-center justify-center w-full h-full p-4 text-center rounded-lg lg:p-8 " + teamCardBG}>
                <img src={"/static/assets/img/headshots/" + teammate.headshotLoc} alt={teammate.name + "'s headshot"} className="w-1/2 mx-auto rounded-full filter grayscale" />
                <h2 className={"mt-4 text-sm font-medium " + teamCardNameColor}>{teammate.name}</h2>
                <h3 className={"text-xs " + teamCardRoleColor}>{teammate.role}</h3>
                <Link href={teammate.linkedInLoc} target="_blank" className="mt-4 w-fit">
                    <i className={"h-5 ri-linkedin-fill text-opacity-50 hover:text-opacity-100 " + teamCardLinkedInIconColor}></i>
                </Link>
            </div>
        )) : null;

  return (
    <div className={"flex-grow px-4 py-12 lg:px-0 " + teamBG}>
      <div className="grid items-stretch gap-4 mx-auto lg:grid-cols-4 lg:w-2/3">
        {teamCardsHTML}
      </div>
    </div>
  );
}
