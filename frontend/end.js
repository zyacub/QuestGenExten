// Sample "quest" array with questions
let quest = []

let helpful = [];

// Function to display questions in the list
function displayQuestions() {
    const questionList = document.getElementById("question-list");

    // Loop through the "quest" array and create list items with buttons
    for (let i = 0; i < quest.length; i++) {
        const question = quest[i];
        const listItem = document.createElement("li");

        // Create question text
        const questionText = document.createElement("span");
        questionText.textContent = question;
        listItem.appendChild(questionText);

        // Create "Yes" button
        const yesButton = document.createElement("button");
        yesButton.textContent = "Yes";
        yesButton.className = "answer-button";
        listItem.appendChild(yesButton);

        // Create "No" button
        const noButton = document.createElement("button");
        noButton.textContent = "No";
        noButton.className = "answer-button";
        listItem.appendChild(noButton);


        // Add click event listeners to "Yes" and "No" buttons
        yesButton.addEventListener("click", () => {
            helpful.push("Yes"); // Add "Yes" to the helpful array
            console.log(helpful);
        });

        noButton.addEventListener("click", () => {
            helpful.push("No"); // Add "No" to the helpful array
            console.log(helpful);
        });

        questionList.appendChild(listItem);
        console.log("Set");
    }
}


// Call the function to display questions when the page loads
window.onload = () => {
    chrome.storage.local.get('total_questions', (res) => {
        console.log(res.total_questions);
        quest = res.total_questions;
        displayQuestions(); // Call displayQuestions after quest has been populated
    });
};