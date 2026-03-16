(function () {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const saveToFile = document.getElementById("saveToFile");
  const uploadSection = document.getElementById("uploadSection");
  const progressSection = document.getElementById("progressSection");
  const progressFilename = document.getElementById("progressFilename");
  const resultSection = document.getElementById("resultSection");
  const transcript = document.getElementById("transcript");
  const copyBtn = document.getElementById("copyBtn");
  const errorSection = document.getElementById("errorSection");
  const errorMessage = document.getElementById("errorMessage");
  const dismissError = document.getElementById("dismissError");

  function show(section) {
    [uploadSection, progressSection, resultSection, errorSection].forEach((el) => {
      el.classList.add("hidden");
    });
    if (section) section.classList.remove("hidden");
  }

  function setTranscript(text) {
    transcript.textContent = text || "";
  }

  dropzone.addEventListener("click", () => fileInput.click());

  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInput.click();
    }
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    const file = e.dataTransfer?.files?.[0];
    if (file) handleFile(file);
  });

  fileInput.addEventListener("change", () => {
    const file = fileInput.files?.[0];
    if (file) handleFile(file);
    fileInput.value = "";
  });

  function handleFile(file) {
    const formData = new FormData();
    formData.append("video", file);
    formData.append("save", saveToFile.checked ? "true" : "false");

    show(progressSection);
    progressFilename.textContent = file.name;

    fetch("/api/transcribe", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json().then((data) => ({ ok: res.ok, data })))
      .then(({ ok, data }) => {
        if (ok) {
          setTranscript(data.text);
          show(resultSection);
        } else {
          errorMessage.textContent = data.error || "Transcription failed.";
          show(errorSection);
        }
      })
      .catch((err) => {
        errorMessage.textContent = err.message || "Network error.";
        show(errorSection);
      });
  }

  copyBtn.addEventListener("click", () => {
    const text = transcript.textContent;
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      copyBtn.textContent = "Copied";
      copyBtn.classList.add("copied");
      setTimeout(() => {
        copyBtn.textContent = "Copy";
        copyBtn.classList.remove("copied");
      }, 2000);
    });
  });

  dismissError.addEventListener("click", () => show(uploadSection));
})();
