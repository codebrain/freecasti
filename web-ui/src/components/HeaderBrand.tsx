import { ControlTooltip } from "@/components/ControlTooltip";
import { FreecastiWordmark } from "@/components/FreecastiWordmark";
import { HeaderLogo } from "@/components/HeaderLogo";

const STUDIO_URL = "https://www.futurestatestudios.com.au";

const FREECASTI_TOOLTIP =
  "Freecasti is a browser editor for the Bricasti M7 reverb — edit program and system parameters, browse factory presets, and send or receive SysEx over Web MIDI.";

interface HeaderBrandProps {
  logoClassName?: string;
  centered?: boolean;
}

export function HeaderBrand({
  logoClassName,
  centered = false,
}: HeaderBrandProps) {
  return (
    <div
      className={`flex min-w-0 items-center gap-3.5 ${
        centered ? "mx-auto flex-col text-center" : ""
      }`}
    >
      <HeaderLogo className={logoClassName} />
      <div className={`min-w-0 leading-tight ${centered ? "items-center" : ""}`}>
        <ControlTooltip description={FREECASTI_TOOLTIP}>
          <FreecastiWordmark />
        </ControlTooltip>
        <a
          href={STUDIO_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-0.5 block text-[0.58rem] tracking-[0.12em] text-[color:var(--color-label)] opacity-65 transition-[opacity,color] duration-200 hover:text-[color:var(--color-chrome)] hover:opacity-100 md:text-[0.62rem]"
        >
          Powered by Future State Studios
        </a>
      </div>
    </div>
  );
}
