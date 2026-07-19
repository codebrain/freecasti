interface FreecastiWordmarkProps {
  className?: string;
}

/** Product wordmark in the rack display face (Michroma / Bricasti-style). */
export function FreecastiWordmark({
  className = "h-[1.35rem] md:h-[1.55rem] w-auto",
}: FreecastiWordmarkProps) {
  return (
    <svg
      role="img"
      aria-label="Freecasti"
      viewBox="0 0 196 26"
      className={className}
      xmlns="http://www.w3.org/2000/svg"
    >
      <text
        x="0"
        y="20"
        fill="var(--color-chrome)"
        style={{
          fontFamily: "var(--font-display)",
          fontSize: "19px",
          fontWeight: 700,
          letterSpacing: "0.16em",
        }}
      >
        Freecasti
      </text>
    </svg>
  );
}
