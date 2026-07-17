interface HeaderLogoProps {
  className?: string;
}

const STUDIO_URL = "https://www.futurestatestudios.com.au";
const LOGO_URL = `${import.meta.env.BASE_URL}logo.png`;

export function HeaderLogo({ className = "h-11 md:h-14 w-auto" }: HeaderLogoProps) {
  return (
    <a
      href={STUDIO_URL}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex shrink-0 rounded-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
    >
      <img
        src={LOGO_URL}
        alt="Future State Studios"
        className={`${className} object-contain`}
        width={150}
        height={150}
        draggable={false}
      />
    </a>
  );
}
