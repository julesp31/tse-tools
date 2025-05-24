window.addEventListener("load", () => {
  document.body.classList.add("loaded");

  loadMonacoEditor(() => {
    const adjustFontSize = () => window.innerWidth <= 1440 ? 13 : 14;

    const commonOpts = {
      fontFamily: 'JetBrains Mono, monospace',
      language: "json",
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

    const outputEditor = monaco.editor.create(
      document.getElementById("output-text"),
      { value: "", readOnly: true, ...commonOpts }
    );

    // English locale object for Air Datepicker
    const enLocale = {
      days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      daysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      daysMin: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
      months: ['January','February','March','April','May','June','July','August','September','October','November','December'],
      monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      today: 'Today',
      clear: 'Clear',
      dateFormat: 'mm/dd/yyyy',
      timeFormat: 'hh:ii aa',
      firstDay: 1
    };

    const fixMinutesToZero = (date) => {
      const fixed = new Date(date);
      fixed.setMinutes(0, 0, 0);
      return fixed;
    };

    new AirDatepicker('#created_from', {
      timepicker: true,
      minutesStep: 60,
      minHours: 0,
      maxHours: 23,
      locale: enLocale,
      onSelect({ date }) {
        this.selectDate(fixMinutesToZero(date));
      }
    });

    new AirDatepicker('#created_to', {
      timepicker: true,
      minutesStep: 60,
      minHours: 0,
      maxHours: 23,
      locale: enLocale,
      onSelect({ date }) {
        this.selectDate(fixMinutesToZero(date));
      }
    });

    // Resize handling
    window.addEventListener("resize", () => {
      const fontSize = adjustFontSize();
      outputEditor.updateOptions({ fontSize });
    });
  });
});
