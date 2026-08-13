/* Runs before paint (sync, tiny) so the chosen theme never flashes.
   No stored choice = follow the system via prefers-color-scheme in CSS. */
try {
  var t = localStorage.getItem("mentio-theme");
  if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
} catch (e) {}
