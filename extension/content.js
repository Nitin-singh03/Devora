function detectProblem() {
    const slug = window.location.pathname
        .split("/")
        .filter(Boolean)[1];

    const titleElement =
        document.querySelector('[data-cy="question-title"]') ||
        document.querySelector("h1");

    const problem = {
        platform: "leetcode",
        slug: slug || "",
        title: titleElement?.textContent?.trim() || document.title,
        url: window.location.href
    };

    chrome.storage.local.set({
        currentProblem: problem
    });
}

detectProblem();

const observer = new MutationObserver(() => {
    detectProblem();
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});