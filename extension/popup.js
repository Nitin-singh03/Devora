const problemElement = document.getElementById("problem");

chrome.storage.local.get("currentProblem", (data) => {
  const problem = data.currentProblem;

  if (!problem) {
    problemElement.textContent = "Open a LeetCode problem.";
    return;
  }

  problemElement.innerHTML = `
        <strong>${problem.title}</strong>
        <p>${problem.platform}</p>
        <a href="${problem.url}" target="_blank">
            Open Problem
        </a>
    `;
});