function loadMonacoEditor(callback) {
  if (window.monaco) {
    // Monaco already loaded
    callback();
  } else {
    require.config({
      paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs"
      }
    });

    require(["vs/editor/editor.main"], () => {
      // Disable JSON validation by default
      monaco.languages.json.jsonDefaults.setDiagnosticsOptions({ validate: false });
      callback();
    });
  }
}