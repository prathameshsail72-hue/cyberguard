async function analyzeURL() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert("Please enter a URL to scan.");
        return;
    }

    const response = await fetch('/api/analyze-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    });

    const data = await response.json();

    const resultBox = document.getElementById('resultBox');
    const riskLevel = document.getElementById('riskLevel');
    const riskScore = document.getElementById('riskScore');
    const issuesList = document.getElementById('issuesList');

    resultBox.classList.remove('hidden');
    riskLevel.innerText = `Status: ${data.risk_level}`;
    riskScore.innerText = data.score;

    issuesList.innerHTML = '';
    if (data.issues.length === 0) {
        issuesList.innerHTML = '<li>No major suspicious indicators detected.</li>';
    } else {
        data.issues.forEach(issue => {
            const li = document.createElement('li');
            li.innerText = issue;
            issuesList.appendChild(li);
        });
    }
}