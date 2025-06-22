// Wait until the entire page and resources are fully loaded
window.addEventListener("load", () => {
  // Make the body visible after load (used to prevent flash of unstyled content)
  document.body.classList.add("loaded");

  // Load the Monaco Editor and set up editors, context menus, and button logic
  loadMonacoEditor(() => {

    // Adjust editor font size depending on screen width
    function adjustFontSize() {
      return window.innerWidth <= 1440 ? 13 : 14;
    }

    // Shared Monaco editor settings for both input and output editors
    const commonOpts = {
      fontFamily: 'JetBrains Mono, monospace',
      language: "plaintext",
      theme: "vs",
      automaticLayout: true,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      scrollbar: { vertical: "auto", horizontal: "auto" },
      lineNumbers: "on",
      lineNumbersMinChars: 1,
      wordWrap: "on",
      glyphMargin: false,
      folding: false,
      contextmenu: false,
      occurrencesHighlight: false,
      fontSize: adjustFontSize()
    };

    // Create the main editors
    const inputEditor = monaco.editor.create(document.getElementById("input-text"), {
      value: "",
      ...commonOpts
    });

    const outputEditor = monaco.editor.create(document.getElementById("output-text"), {
      value: "",
      readOnly: true,
      ...commonOpts
    });

    // Custom right-click menu handler (copy, paste, format, etc.)
    const createMenu = (editor, items, x, y) => {
      const prev = document.getElementById("custom-context-menu");
      if (prev) prev.remove();

      const menu = document.createElement("div");
      menu.id = "custom-context-menu";
      menu.style.top = y + "px";
      menu.style.left = x + "px";

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

    // Attach context menu to input and output editors
    document.getElementById("input-text").addEventListener("contextmenu", e => {
      e.preventDefault();
      createMenu(inputEditor, [
        { label: "Copy", command: "editor.action.clipboardCopyAction" },
        { label: "Paste", command: "editor.action.clipboardPasteAction" },
      ], e.pageX, e.pageY);
    });

    document.getElementById("output-text").addEventListener("contextmenu", e => {
      e.preventDefault();
      createMenu(outputEditor, [
        { label: "Copy", command: "editor.action.clipboardCopyAction" }
      ], e.pageX, e.pageY);
    });

    // Hide context menu when clicking anywhere else
    document.addEventListener("click", () => {
      const menu = document.getElementById("custom-context-menu");
      if (menu) menu.remove();
    });

    // Helper to toggle styling classes based on input editor content
    function updateInputStyling() {
      const hasContent = inputEditor.getValue().trim() !== "";
      const inputArea = document.querySelector(".input-area");
      const inputCont = document.querySelector(".input-area .editor-container");

      inputArea.classList.toggle("focused", hasContent);
      inputCont.classList.toggle("has-content", hasContent);
    }

    // Style the input area if it has content
    inputEditor.onDidPaste(() => {
      updateInputStyling();
    });

    // Apply or remove styling on focus/blur
    inputEditor.onDidFocusEditorText(updateInputStyling);
    inputEditor.onDidBlurEditorText(updateInputStyling);

    // Handle click on "Generate" button — send input to backend and display result
    document.getElementById("generate-btn").addEventListener("click", () => {
      const input = inputEditor.getValue();
      const endpoint = "/comma"; // Endpoint for comma-separated list formatter
      const body = { text: input };

      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      })
        .then(res => res.json())
        .then(data => {
          const result = data.printing_times || data.formatted || "";  // supports both tools
          outputEditor.setValue(result);

          const outArea = document.querySelector(".output-area");
          const outCont = document.querySelector(".output-area .editor-container");

          if (result.trim() !== "") {
            outArea.classList.add("focused");
            outCont.classList.add("has-content");
          } else {
            outArea.classList.remove("focused");
            outCont.classList.remove("has-content");
          }
        })
        .catch(err => console.error("Error:", err));
    });

    // Update editor font size when window is resized
    window.addEventListener("resize", () => {
      const fontSize = adjustFontSize();
      inputEditor.updateOptions({ fontSize });
      outputEditor.updateOptions({ fontSize });
    });

    // Info modal: open and close behavior for the "How to Use" popup
    const infoBtn = document.getElementById("info-button");
    const infoModal = document.getElementById("info-modal");
    const closeModal = document.querySelector(".info-modal .close");

    if (infoBtn && infoModal && closeModal) {
      infoBtn.addEventListener("click", () => {
        infoModal.style.display = "block";
      });

      closeModal.addEventListener("click", () => {
        infoModal.style.display = "none";
      });

      window.addEventListener("click", (event) => {
        if (event.target === infoModal) {
          infoModal.style.display = "none";
        }
      });
    }
  });
});
