window.addEventListener("load", function () {
  require.config({
    paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs" }
  });

  require(["vs/editor/editor.main"], function () {
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

    // Initialize Monaco Editor for Output (Read-Only)
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

    // When text is pasted into the input editor,
    // format it and add a "focused" state if non-empty.
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

    // Focus and blur events for the input editor.
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

    // Sidebar toggle logic: toggle nav-open class on hero and text container
    const textContainer = document.querySelector('.text-container');
    const heroBanner = document.querySelector('.hero');
    const btnOne = document.querySelector('.btn-one');
    const btnTwo = document.querySelector('.btn-two');

    btnOne.addEventListener('click', () => {
      textContainer.classList.add('nav-open');
      heroBanner.classList.add('nav-open');
    });
    btnTwo.addEventListener('click', () => {
      textContainer.classList.remove('nav-open');
      heroBanner.classList.remove('nav-open');
    });

    // Handle Generate Button Click:
    // Populate output editor and toggle focused state on output-area.
    document.getElementById("generate-btn").addEventListener("click", function () {
      const inputVal = inputEditor.getValue();
      fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputVal })
      })
      .then(response => response.json())
      .then(data => {
        const jsonOutput = JSON.stringify(data, null, 2);
        outputEditor.setValue(jsonOutput);
        if (jsonOutput.trim() !== "") {
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
