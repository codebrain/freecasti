import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { initRenderMode } from "./app/renderMode";

initRenderMode();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
