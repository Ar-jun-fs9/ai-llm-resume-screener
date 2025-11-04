// File upload handling
const resumeUpload = document.getElementById("resumeUpload");
const jobUpload = document.getElementById("jobUpload");
const resumeFiles = document.getElementById("resumeFiles");
const jobFile = document.getElementById("jobFile");

// Resume upload handlers
resumeUpload.addEventListener("click", () =>
  document.getElementById("resumes").click()
);
jobUpload.addEventListener("click", () =>
  document.getElementById("job_description").click()
);

// Drag and drop functionality
function setupDragAndDrop(element, inputElement) {
  element.addEventListener("dragover", (e) => {
    e.preventDefault();
    element.classList.add("dragover");
    element.classList.add("border-green-500");
    element.classList.add("bg-green-50");
  });

  element.addEventListener("dragleave", (e) => {
    e.preventDefault();
    element.classList.remove("dragover");
    element.classList.remove("border-green-500");
    element.classList.remove("bg-green-50");
  });

  element.addEventListener("drop", (e) => {
    e.preventDefault();
    element.classList.remove("dragover");
    element.classList.remove("border-green-500");
    element.classList.remove("bg-green-50");
    const files = e.dataTransfer.files;
    inputElement.files = files;
    updateFileDisplay();
  });
}

setupDragAndDrop(resumeUpload, document.getElementById("resumes"));
setupDragAndDrop(jobUpload, document.getElementById("job_description"));

// File selection handlers
document
  .getElementById("resumes")
  .addEventListener("change", updateFileDisplay);
document
  .getElementById("job_description")
  .addEventListener("change", updateFileDisplay);

function updateFileDisplay() {
  // Display selected resume files with remove buttons
  const resumeFilesList = document.getElementById("resumes").files;
  resumeFiles.innerHTML = "";
  if (resumeFilesList.length > 0) {
    const filesHtml = Array.from(resumeFilesList)
      .map(
        (file, index) => `
                <div class="bg-gray-50 rounded-lg p-3 animate-slide-up flex items-center justify-between min-w-0">
                  <div class="flex items-center flex-1 min-w-0 mr-3">
                    <i class="fas fa-file text-blue-500 mr-2 flex-shrink-0"></i>
                    <p class="text-gray-800 font-medium text-sm truncate" title="${file.name}">${file.name}</p>
                  </div>
                  <button
                    type="button"
                    class="text-red-500 hover:text-red-700 hover:bg-red-100 p-1 rounded-full transition-colors duration-200 flex-shrink-0 ml-2"
                    onclick="removeResumeFile(${index})"
                    title="Remove file"
                  >
                    <i class="fas fa-times text-sm"></i>
                  </button>
                </div>
              `
      )
      .join("");
    resumeFiles.innerHTML = filesHtml;
  }

  // Display selected job description file with remove button
  const jobFileList = document.getElementById("job_description").files;
  jobFile.innerHTML = "";
  if (jobFileList.length > 0) {
    jobFile.innerHTML = `
            <div class="flex items-center justify-between bg-green-50 border border-green-200 rounded-lg p-3 animate-slide-up">
              <div class="flex items-center">
                <i class="fas fa-file-alt text-green-500 mr-3"></i>
                <span class="text-green-800 font-medium">${jobFileList[0].name}</span>
              </div>
              <button
                type="button"
                class="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-full transition-colors duration-200"
                onclick="removeJobFile()"
                title="Remove file"
              >
                <i class="fas fa-times-circle"></i>
              </button>
            </div>
          `;
  }

  // Enable rank button automatically when both files are uploaded
  const rankBtn = document.getElementById("rankBtn");

  if (resumeFilesList.length > 0 && jobFileList.length > 0) {
    rankBtn.disabled = false;
  } else {
    rankBtn.disabled = true;
  }
}

function removeResumeFile(index) {
  const input = document.getElementById("resumes");
  const dt = new DataTransfer();

  // Add all files except the one to remove
  for (let i = 0; i < input.files.length; i++) {
    if (i !== index) {
      dt.items.add(input.files[i]);
    }
  }

  input.files = dt.files;
  updateFileDisplay();
}

function removeJobFile() {
  document.getElementById("job_description").value = "";
  updateFileDisplay();
}

// Form submission
document.getElementById("resumeForm").addEventListener("submit", async (e) => {
  e.preventDefault();
});

// Rank button click
document.getElementById("rankBtn").addEventListener("click", async () => {
  const formData = new FormData();
  const resumes = document.getElementById("resumes").files;
  const jobDesc = document.getElementById("job_description").files[0];

  if (resumes.length === 0 || !jobDesc) {
    alert("Please select both resumes and a job description file.");
    return;
  }

  // Append files to form data
  for (let i = 0; i < resumes.length; i++) {
    formData.append("resumes", resumes[i]);
  }
  formData.append("job_description", jobDesc);

  // Show loading spinner
  document.getElementById("loadingSpinner").classList.remove("hidden");
  document.getElementById("resultsSection").classList.add("hidden");

  try {
    const response = await fetch("/rank", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      displayResults(data.results);
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    alert("Network error: " + error.message);
  } finally {
    document.getElementById("loadingSpinner").classList.add("hidden");
  }
});

function displayResults(results) {
  const resultsBody = document.getElementById("resultsBody");
  resultsBody.innerHTML = "";

  results.forEach((result, index) => {
    const scorePercentage = (result["Similarity Score"] * 100).toFixed(2);
    let scoreColorClass = "text-red-600";
    if (result["Similarity Score"] >= 0.7) {
      scoreColorClass = "text-green-600";
    } else if (result["Similarity Score"] >= 0.4) {
      scoreColorClass = "text-yellow-600";
    }

    const row = document.createElement("tr");
    row.className = "hover:bg-gray-50 transition-colors duration-200";
    row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${
              index + 1
            }</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${
              result.Candidate
            }</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold ${scoreColorClass}">${scorePercentage}%</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
                      onclick="summarizeCandidate('${result.Candidate}')"
                      id="summarize-${result.Candidate.replace(
                        /[^a-zA-Z0-9]/g,
                        "-"
                      )}">
                <i class="fas fa-file-alt mr-1"></i>Summarize
              </button>
            </td>
          `;
    resultsBody.appendChild(row);
  });

  document.getElementById("resultsSection").classList.remove("hidden");
}

// Download results
document.getElementById("downloadBtn").addEventListener("click", () => {
  window.open("/download", "_blank");
});

// Clear Page
document.getElementById("clearPageBtn").addEventListener("click", () => {
  document.getElementById("resumeForm").reset();
  resumeFiles.innerHTML = "";
  jobFile.innerHTML = "";
  document.getElementById("resultsSection").classList.add("hidden");
  document.getElementById("loadingSpinner").classList.add("hidden");
  document.getElementById("resultsBody").innerHTML = "";

  // Clear global storage
  window.storedResumes = {};
  window.storedJobText = "";
});

// Modal functions
function closeModal() {
  document.getElementById("summaryModal").classList.add("hidden");
}

// Function to summarize candidate
async function summarizeCandidate(candidateName) {
  const buttonId = `summarize-${candidateName.replace(/[^a-zA-Z0-9]/g, "-")}`;
  const button = document.getElementById(buttonId);
  const originalText = button.innerHTML;

  // Show loading state on button
  button.disabled = true;
  button.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i>Generating...';

  // Show modal with loading state
  document.getElementById("summaryLoading").classList.remove("hidden");
  document.getElementById("summaryContent").classList.add("hidden");
  document.getElementById("summaryError").classList.add("hidden");
  document.getElementById("summaryModal").classList.remove("hidden");

  try {
    const formData = new FormData();
    formData.append("candidate_name", candidateName);

    const response = await fetch("/generate_summary", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.summary) {
  // Populate modal with candidate name
  document.getElementById(
    "summaryCandidateName"
  ).textContent = `Candidate: ${candidateName}`;

  // Convert summary text to HTML with bold numbered headings
  let htmlText = data.summary.replace(
    /^(\d+\.\s.+)$/gm, // Match lines like "1. Candidate Profile Summary"
    '<strong>$1</strong>'
  );

  // Replace hyphens in Recommendations section with bullet points
  htmlText = htmlText.replace(
    /(\d+\. Recommendations[\s\S]*?)(?=\n\d+\.|$)/gm, // Match Recommendations block
    function (match) {
      return match.replace(/^\s*-\s/gm, '• ');
    }
  );

  document.getElementById("candidateSummary").innerHTML = htmlText;

  // Show content, hide loading
  document.getElementById("summaryLoading").classList.add("hidden");
  document.getElementById("summaryContent").classList.remove("hidden");
} else {
  // Show error
  document.getElementById("summaryErrorMessage").textContent =
    data.error || "Unknown error occurred";
  document.getElementById("summaryLoading").classList.add("hidden");
  document.getElementById("summaryError").classList.remove("hidden");
}

} catch (error) {
  // Show error
  document.getElementById("summaryErrorMessage").textContent =
    "Network error: " + error.message;
  document.getElementById("summaryLoading").classList.add("hidden");
  document.getElementById("summaryError").classList.remove("hidden");
} finally {
  // Restore button state
  button.disabled = false;
  button.innerHTML = originalText;
}

}

// Close modal when clicking outside
document.getElementById("summaryModal").addEventListener("click", function (e) {
  if (e.target === this) {
    closeModal();
  }
});

// Escape key to close modal
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeModal();
  }
});
