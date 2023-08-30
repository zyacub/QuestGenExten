const question = document.getElementById('question');
const answer = document.getElementById('answer');
const submitanswer = document.getElementById('submit-answer');
const loader = document.getElementById('loader');
const game = document.getElementById('game');
const next_question = document.getElementById("next-question");
let query_url;

let currentQuestion = {};
let acceptingAnswers = true;
let score = 0;
let questionCounter = 0;
let availableQuestions = [];

let questions = [];

chrome.storage.local.get(['questions']).then((res) => {
  console.log(res.questions);
  if (res.questions) {
    questions = res.questions;
    console.log("Questions");
    console.log(questions);
    startGame();
  } else {
    fetchQuestions();
  }
})

submitanswer.addEventListener("click", () => {
  textareaValue();
});

next_question.addEventListener("click", () => {
  getNewQuestion();
});






fetchQuestions = () => {
  chrome.storage.local.get(['url']).then((res) => {
    url = res.url;
    console.log(url);
    query_url = "https://questgen.ngrok.io/url/" + url;
    fetch(query_url)
  .then(data => {
    return data.json()
  })
  .then(loadedQuestions => {
    questions = loadedQuestions;
    console.log("Questions")
    console.log(questions)
    sendDataToSession('questions', questions)
    startGame()
  })
  .catch(err => {
    console.error(err)
  })
  });
}


const CORRECT_BONUS = 10;
const MAX_QUESTIONS = 15;

startGame = () => {
    questionCounter = 0;
    score = 0;
    availableQuestions = [...questions];
    console.log(availableQuestions);
    getNewQuestion();
    game.classList.remove("hidden")
    loader.classList.add("hidden")
};

getNewQuestion = () => {
    if (availableQuestions.length === 0 || questionCounter >= MAX_QUESTIONS) {
        return window.location.assign("/end.html");
    }
    questionCounter++;
    const questionIndex = Math.floor(Math.random() * availableQuestions.length);
    currentQuestion = availableQuestions[questionIndex];
    question.innerText = currentQuestion;
    //correctAnswer = currentQuestion.context;
    
    document.getElementById('answer').value = "Enter answer here...";
    answer.disabled = false;
    submitanswer.disabled = false;
    submitanswer.innerText = 'Submit Answer'

    availableQuestions.splice(questionIndex, 1);
    setQuestions(availableQuestions);
    acceptingAnswers = true;

}



textareaValue = () => {
    document.getElementById('answer').value += '\n\n\n' + "---------------------" + '\n' + "The Correct answer is: " //+ correctAnswer;

    submitanswer.disabled = true;
    answer.disabled = true;
    submitanswer.innerText = 'Answer submitted...'
    console.log(answer);
};

sendDataToSession = (label2,data) => {
  chrome.storage.session.set({label2 : data}).then(() => { 
    console.log("data was set");
  });
}

setQuestions = (questions) => {

  chrome.storage.local.remove(["questions"]);

  chrome.storage.local.set({'questions': questions}).then(() => { 
    console.log("Questions set");
  });
}
