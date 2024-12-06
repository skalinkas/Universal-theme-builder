document.addEventListener("DOMContentLoaded", () => {
    const loadThemesButton = document.getElementById("loadThemes");
    const themeList = document.getElementById("themeList");

    loadThemesButton.addEventListener("click", async () => {
        themeList.innerHTML = "<p>Loading themes...</p>";

        try {
            const response = await fetch("/api/services/style_builder/read_theme", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ theme_name: "default" }),
            });
            const data = await response.json();
            themeList.innerHTML = `<pre>${JSON.stringify(data.theme, null, 2)}</pre>`;
        } catch (err) {
            themeList.innerHTML = `<p>Error loading themes: ${err.message}</p>`;
        }
    });
});
