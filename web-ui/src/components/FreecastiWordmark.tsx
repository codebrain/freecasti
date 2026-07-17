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
      <defs>
        <linearGradient id="freecasti-word-fill" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="oklch(0.96 0.02 85)" />
          <stop offset="55%" stopColor="oklch(0.88 0.04 75)" />
          <stop offset="100%" stopColor="oklch(0.78 0.08 55)" />
        </linearGradient>
        <filter id="freecasti-word-glow" x="-20%" y="-80%" width="140%" height="260%">
          <feGaussianBlur stdDeviation="1.2" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <text
        x="0"
        y="20"
        fill="url(#freecasti-word-fill)"
        filter="url(#freecasti-word-glow)"
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
