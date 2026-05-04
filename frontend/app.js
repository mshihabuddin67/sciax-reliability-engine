async function run() {
    const prompt = document.getElementById("prompt").value;

    document.getElementById("out").innerText = "Analyzing...";

    try {
        const res = await fetch("http://localhost:5000/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({prompt})
        });

        const data = await res.json();
        document.getElementById("out").innerText =
            JSON.stringify(data, null, 2);

    } catch (e) {
        document.getElementById("out").innerText = "Error connecting API";
    }
}
