window.addEventListener('load', function() {
  // Initialize CodeMirror for input
  var inputEditor = CodeMirror.fromTextArea(document.getElementById("input-text"), {
    mode: { name: "javascript", json: true },
    lineNumbers: true,
    theme: "material-darker",
    viewportMargin: Infinity,
    lineWrapping: true,
    coverGutterNextToScrollbar: true
  });

  var cmWrapper = inputEditor.getWrapperElement();
  cmWrapper.addEventListener("paste", function(e) {
    console.log("Paste event on CodeMirror container detected.");
  });
  
  // Initialize CodeMirror for output
  var outputEditor = CodeMirror.fromTextArea(document.getElementById("output-text"), {
    mode: { name: "javascript", json: true },
    lineNumbers: true,
    readOnly: "nocursor",
    theme: "material-darker",
    viewportMargin: Infinity,
    lineWrapping: true
  });
  
// Listen for paste events on the input editor and convert pasted text to valid JSON
// Listen for input read events on the input editor
inputEditor.on("inputRead", function(cm, change) {
  if (change.origin === "paste") {
    try {
      const raw = cm.getValue();
      const parsed = JSON5.parse(raw);
      let formatted = JSON.stringify(parsed, null, 2);

      if (raw !== formatted) {
        cm.setValue(formatted);
        cm.refresh();
        
        // Delay setting the cursor until after the re-render
        setTimeout(() => {
          let lastLine = cm.lineCount() - 1;
          // Move up if the last line is empty
          while (lastLine > 0 && cm.getLine(lastLine).trim() === "") {
            lastLine--;
          }
          const lastCh = cm.getLine(lastLine).length;
          cm.setCursor({ line: lastLine, ch: lastCh });
        }, 0);
      }
    } catch (e) {
      console.error("Error parsing pasted JSON:", e);
    }
  }
});

  // Attach focus/blur events to update container classes for label transitions on input editor
  inputEditor.on("focus", function() {
    document.querySelector(".input-area").classList.add("focused");
  });
  inputEditor.on("blur", function() {
    // Remove the focused class if there is no content
    if (inputEditor.getValue().trim() === "") {
      document.querySelector(".input-area").classList.remove("focused");
    }
  });
  inputEditor.on("change", function() {
    if (inputEditor.getValue().trim() !== "") {
      document.querySelector(".input-area").classList.add("focused");
    } else {
      document.querySelector(".input-area").classList.remove("focused");
    }
  });
  
  // Sidebar toggle
  const textContainer = document.querySelector('.text-container');
  const heroBanner = document.querySelector('.hero');
  const btnOne = document.querySelector('.btn-one');
  const btnTwo = document.querySelector('.btn-two');

  btnOne.addEventListener('click', () => {
    textContainer.style.marginLeft = '250px';
    textContainer.style.marginRight = '10px';
    heroBanner.style.marginLeft = '240px';
  });

  btnTwo.addEventListener('click', () => {
    textContainer.style.marginLeft = '10px';
    heroBanner.style.marginLeft = '0px';
  });

  // When the Generate button is clicked, send input to server and update output editor
  document.getElementById("generate-btn").addEventListener("click", function () {
    // Get the JSON text from the CodeMirror input editor
    const inputText = inputEditor.getValue();

    fetch("/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: inputText })
    })
    .then(response => response.json())
    .then(data => {
      // Pretty-print the JSON output
      const jsonOutput = JSON.stringify(data, null, 2);
      // Set the output in the CodeMirror read-only editor
      outputEditor.setValue(jsonOutput);
      // Add "focused" class if valid output exists
      if(jsonOutput.trim() !== "") {
        document.querySelector(".output-area").classList.add("focused");
      } else {
        document.querySelector(".output-area").classList.remove("focused");
      }
    })
    .catch(error => {
      console.error("Error:", error);
    });
  });
});