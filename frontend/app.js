document.addEventListener("DOMContentLoaded", () => {
    const loadThemesButton = document.getElementById("load-themes");
    const themeList = document.getElementById("theme-list");
    const themeEditor = document.getElementById("theme-editor");
    const downloadButton = document.getElementById("download-theme");

    loadThemesButton.addEventListener("click", async () => {
        const response = await fetch("/api/style_builder/read_theme", {
            method: "POST",
            body: JSON.stringify({ theme_name: "example_theme" }),
        });
        const data = await response.json();
        themeList.innerHTML = JSON.stringify(data.theme, null, 2);
    });

    downloadButton.addEventListener("click", () => {
        // Implement theme download functionality
    });

    // Additional logic for creating and editing themes dynamically
});
