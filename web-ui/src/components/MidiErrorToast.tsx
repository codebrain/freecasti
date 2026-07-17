interface MidiErrorToastProps {
  message: string;
}

export function MidiErrorToast({ message }: MidiErrorToastProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed bottom-6 left-1/2 z-50 max-w-[min(24rem,calc(100vw-2rem))] -translate-x-1/2 rounded-lg border border-destructive/40 bg-destructive/20 px-4 py-2 text-center text-xs text-destructive shadow-lg"
    >
      MIDI: {message}
    </div>
  );
}
