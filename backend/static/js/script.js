// script.js

window.addEventListener("load", function () {
  require.config({
    paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs" }
  });

  require(["vs/editor/editor.main"], function () {
    // Disable JSON validation in Monaco
    monaco.languages.json.jsonDefaults.setDiagnosticsOptions({ validate: false });

    // Initialize Monaco Editor for Input
    var inputEditor = monaco.editor.create(document.getElementById("input-text"), {
      value: "",
      language: "json",
      theme: "vs-dark",
      automaticLayout: true,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      scrollbar: { vertical: "auto", horizontal: "auto" },
      lineNumbers: "on",
      lineNumbersMinChars: 1,
      wordWrap: "on"
    });

    // Initialize Monaco Editor for Output
    var outputEditor = monaco.editor.create(document.getElementById("output-text"), {
      value: "",
      language: "json",
      theme: "vs-dark",
      readOnly: true,
      automaticLayout: true,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      scrollbar: { vertical: "auto", horizontal: "auto" },
      lineNumbers: "on",
      lineNumbersMinChars: 1,
      wordWrap: "on"
    });

    // Format on paste in the input editor
    inputEditor.onDidPaste(() => {
      try {
        let raw = inputEditor.getValue();
        let formatted = JSON.stringify(JSON.parse(raw), null, 2);
        inputEditor.setValue(formatted);
        if (formatted.trim() !== "") {
          document.querySelector(".input-area").classList.add("focused");
          document.querySelector(".input-area .editor-container").classList.add("has-content");
        }
      } catch (e) {
        console.error("Invalid JSON", e);
      }
    });

    // Focus/blur events
    inputEditor.onDidFocusEditorText(() => {
      document.querySelector(".input-area").classList.add("focused");
      document.querySelector(".input-area .editor-container").classList.add("has-content");
    });
    inputEditor.onDidBlurEditorText(() => {
      if (inputEditor.getValue().trim() === "") {
        document.querySelector(".input-area").classList.remove("focused");
        document.querySelector(".input-area .editor-container").classList.remove("has-content");
      }
    });

    // Grab references for sidebar toggle
    const mainBox = document.querySelector('.main-box');
    const btnOne = document.querySelector('.btn-one');
    const btnTwo = document.querySelector('.btn-two');

    // Toggle .nav-open on the .main-box instead of .text-container/.hero
    btnOne.addEventListener('click', () => {
      mainBox.classList.add('nav-open');
    });
    btnTwo.addEventListener('click', () => {
      mainBox.classList.remove('nav-open');
    });

    // "Generate" button logic
    document.getElementById("generate-btn").addEventListener("click", function () {
      const inputVal = inputEditor.getValue();
      fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputVal })
      })
      .then(response => response.json())
      .then(data => {
        outputEditor.setValue(data.printing_times);
        if (data.printing_times.trim() !== "") {
          document.querySelector(".output-area").classList.add("focused");
          document.querySelector(".output-area .editor-container").classList.add("has-content");
        } else {
          document.querySelector(".output-area").classList.remove("focused");
          document.querySelector(".output-area .editor-container").classList.remove("has-content");
        }
      })
      .catch(error => {
        console.error("Error:", error);
      });
    });
  });
});
