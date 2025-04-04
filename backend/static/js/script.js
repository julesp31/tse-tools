// main.js

window.addEventListener("load", () => {
  require.config({
    paths: {
      vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs"
    }
  });

  require(["vs/editor/editor.main"], () => {
    monaco.languages.json.jsonDefaults.setDiagnosticsOptions({ validate: false });

    const commonOpts = {
      language: "json",
      theme: "vs-dark",
      automaticLayout: true,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      scrollbar: { vertical: "auto", horizontal: "auto" },
      lineNumbers: "on",
      lineNumbersMinChars: 1,
      wordWrap: "on",
      glyphMargin: false,
      folding: false,
      contextmenu: false
    };

    const inputEditor = monaco.editor.create(
      document.getElementById("input-text"),
      { value: "", ...commonOpts }
    );

    const outputEditor = monaco.editor.create(
      document.getElementById("output-text"),
      { value: "", readOnly: true, ...commonOpts }
    );

    // Context menu
    const createMenu = (editor, items, x, y) => {
      const prev = document.getElementById("custom-context-menu");
      if (prev) prev.remove();
      const menu = document.createElement("div");
      menu.id = "custom-context-menu";
      // Set dynamic menu position
      menu.style.top = y + "px";
      menu.style.left = x + "px";
      // Add each menu item
      items.forEach(({ label, command }) => {
        const item = document.createElement("div");
        item.className = "menu-item";
        item.textContent = label;
        item.addEventListener("click", () => {
          editor.focus();
          editor.trigger("custom", command, null);
          menu.remove();
        });
        menu.appendChild(item);
      });
      document.body.appendChild(menu);
    };

    // Attach custom context menus to the editor containers
    document.getElementById("input-text").addEventListener("contextmenu", e => {
      e.preventDefault();
      createMenu(inputEditor, [
        { label: "Copy", command: "editor.action.clipboardCopyAction" },
        { label: "Paste", command: "editor.action.clipboardPasteAction" },
        { label: "Format", command: "editor.action.formatDocument" }
      ], e.pageX, e.pageY);
    });
    document.getElementById("output-text").addEventListener("contextmenu", e => {
      e.preventDefault();
      createMenu(outputEditor, [
        { label: "Copy", command: "editor.action.clipboardCopyAction" }
      ], e.pageX, e.pageY);
    });
    document.addEventListener("click", () => {
      const menu = document.getElementById("custom-context-menu");
      if (menu) menu.remove();
    });

    // Input editor paste and focus/blur events
    inputEditor.onDidPaste(() => {
      try {
        const raw = inputEditor.getValue();
        const formatted = JSON.stringify(JSON.parse(raw), null, 2);
        inputEditor.setValue(formatted);
        if (formatted.trim() !== "") {
          document.querySelector(".input-area").classList.add("focused");
          document.querySelector(".input-area .editor-container").classList.add("has-content");
        }
      } catch (e) {
        console.error("Invalid JSON", e);
      }
    });
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

    // Generate button logic
    document.getElementById("generate-btn").addEventListener("click", () => {
      fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputEditor.getValue() })
      })
      .then(res => res.json())
      .then(data => {
        outputEditor.setValue(data.printing_times);
        const outArea = document.querySelector(".output-area"),
              outCont = document.querySelector(".output-area .editor-container");
        if (data.printing_times.trim() !== "") {
          outArea.classList.add("focused");
          outCont.classList.add("has-content");
        } else {
          outArea.classList.remove("focused");
          outCont.classList.remove("has-content");
        }
      })
      .catch(err => console.error("Error:", err));
    });
  });
});