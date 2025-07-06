// Wait until the entire page and assets are fully loaded
window.addEventListener("load", () => {
  // Prevents flash of unstyled content
  document.body.classList.add("loaded");

  // Load Monaco Editor and initialize everything once ready
  loadMonacoEditor(() => {
    // Dynamically adjust font size based on screen width
    const adjustFontSize = () => (window.innerWidth <= 1440 ? 13 : 14);

    // Define custom Monaco Editor theme (line number colors)
    monaco.editor.defineTheme('my-custom-theme', {
      base: 'vs', // Or 'vs-dark' if you're using the dark theme
      inherit: true,
      rules: [
        { token: 'string.sql', foreground: '#FF6363' },   // aqua strings
        { token: 'number.sql', foreground: '#36B37E' },
        { token: 'delimiter.sql', foreground: '#8B7E66' }
      ],
      colors: {
        // Line numbers color
        "editorLineNumber.foreground": "#AAAAAA",
        // Active line number color
        "editorLineNumber.activeForeground": "#AAAAAA",
        // Scrollbar color
        "scrollbarSlider.background": "#DDDDDD"
      }
    });

    // Apply custom theme to Monaco
    monaco.editor.setTheme('my-custom-theme');

    // Shared Monaco Editor settings for both input and output editors
    const commonOpts = {
      fontFamily: 'JetBrains Mono, monospace',
      language: "sql",
      theme: "my-custom-theme",
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

    // Set up references to editors and cache DOM elements
    const inputContainer = document.getElementById("input-text");
    const outputContainer = document.getElementById("output-text");
    const inputArea = document.querySelector(".input-area");
    const inputCont = inputArea.querySelector(".editor-container");
    const outputArea = document.querySelector(".output-area");
    const outputCont = outputArea.querySelector(".editor-container");
    const generateBtn = document.getElementById("generate-btn");
    const infoBtn = document.getElementById("info-button");
    const infoModal = document.getElementById("info-modal");
    const closeModal = document.querySelector(".info-modal .close");

    // Create Monaco Editors
    const inputEditor = monaco.editor.create(inputContainer, {
      value: "",
      ...commonOpts
    });

    const outputEditor = monaco.editor.create(outputContainer, {
      value: "",
      readOnly: true,
      ...commonOpts
    });

    // Create custom right-click menu for Monaco editors
    const createMenu = (editor, items, x, y) => {
      document.getElementById("custom-context-menu")?.remove(); // Remove existing menu if any

      const menu = document.createElement("div");
      menu.id = "custom-context-menu";
      menu.style.top = `${y}px`;
      menu.style.left = `${x}px`;

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

    // Adds right-click menu to input box
    inputContainer.addEventListener("contextmenu", e => {
      e.preventDefault();
      createMenu(inputEditor, [
        { label: "Copy", command: "editor.action.clipboardCopyAction" },
        { label: "Paste", command: "editor.action.clipboardPasteAction" },
        { label: "Format", command: "editor.action.formatDocument" }
      ], e.pageX, e.pageY);
    });

    // Adds right-click menu to output box (Copy only)
    outputContainer.addEventListener("contextmenu", e => {
      e.preventDefault();
      createMenu(outputEditor, [
        { label: "Copy", command: "editor.action.clipboardCopyAction" }
      ], e.pageX, e.pageY);
    });

    // Closes custom context menu when clicking outside
    document.addEventListener("click", () => {
      document.getElementById("custom-context-menu")?.remove();
    });

    // Update input area styling (border and label) based on focus or content
    const updateInputStyling = (forceFocus = false) => {
      const hasContent = inputEditor.getValue().trim() !== "";
      inputArea.classList.toggle("focused", forceFocus || hasContent);
      inputArea.classList.toggle("has-content", hasContent);
    };

    // Format input when pasting content
    inputEditor.onDidPaste(() => {
      updateInputStyling();
    });

    // Update input area border and label on focus/blur
    inputEditor.onDidFocusEditorText(() => updateInputStyling(true));
    inputEditor.onDidBlurEditorText(() => updateInputStyling(false));

    // Handle click on "Generate" button — send input to backend and display result
    generateBtn.addEventListener("click", () => {
      const input = inputEditor.getValue();

      fetch("/comma", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input })
      })
        .then(res => res.json())
        .then(data => {
          const result = data.printing_times || data.formatted || "";
          outputEditor.setValue(result);

          const hasOutput = result.trim() !== "";
          outputArea.classList.toggle("focused", hasOutput);
          outputArea.classList.toggle("has-content", hasOutput);
        })
        .catch(err => console.error("Error:", err));
    });

    // Resize editor font size when window is resized
    window.addEventListener("resize", () => {
      const fontSize = adjustFontSize();
      inputEditor.updateOptions({ fontSize });
      outputEditor.updateOptions({ fontSize });
    });

    // Show and hide the "How to Use" info modal
    if (infoBtn && infoModal && closeModal) {
      infoBtn.addEventListener("click", () => infoModal.style.display = "block");
      closeModal.addEventListener("click", () => infoModal.style.display = "none");
      window.addEventListener("click", e => {
        if (e.target === infoModal) infoModal.style.display = "none";
      });
    }
  });
});