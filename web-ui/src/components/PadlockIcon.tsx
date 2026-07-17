interface PadlockIconProps {
  locked?: boolean;
  className?: string;
  style?: React.CSSProperties;
}

export function PadlockIcon({ locked = true, className = "h-3 w-3", style }: PadlockIconProps) {
  return (
    <svg viewBox="0 0 16 16" className={className} style={style} aria-hidden fill="currentColor">
      {locked ? (
        <>
          <path
            d="M4.5 7V5a3.5 3.5 0 0 1 7 0v2"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.4"
          />
          <rect x="3.25" y="7" width="9.5" height="6.75" rx="1.2" />
        </>
      ) : (
        <>
          <path
            d="M4.5 7V5a3.5 3.5 0 0 1 7 0"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.4"
          />
          <rect
            x="3.25"
            y="7"
            width="9.5"
            height="6.75"
            rx="1.2"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.2"
          />
        </>
      )}
    </svg>
  );
}
