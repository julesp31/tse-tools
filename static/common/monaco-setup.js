function loadMonacoEditor(callback) {
  if (window.monaco) {
    callback();
  } else {
    // Use the official Monaco pre-bundled loader
    const loaderScript = document.createElement("script");
    loaderScript.src = "https://cdn.jsdelivr.net/npm/monaco-editor@0.39.0/min/vs/loader.js";
    loaderScript.onload = () => {
      require.config({ paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.39.0/min/vs" } });
      require(["vs/editor/editor.main"], () => {
        monaco.languages.json.jsonDefaults.setDiagnosticsOptions({ validate: false });
        callback();
      });
    };
    document.body.appendChild(loaderScript);
  }
}
