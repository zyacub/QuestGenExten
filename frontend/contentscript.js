const url = document.location.href;
console.log(url);

chrome.storage.local.clear(function() {
    var error = chrome.runtime.lastError;
    if (error) {
        console.error(error);
    }
});

getQuestions = () => {
    let query_url = "https://questgen.ngrok.io/questions/get/" + encodeURIComponent(encodeURIComponent(url));
    console.log(query_url);
    fetch(query_url)
    .then(data => {
        return data.json()
    })
    .then(result => {
        console.log(result)
        if(result.result) {
            console.log("Questions found in cache");
            console.log(result.result.data);
            setQuestions(result.result.data);
        } else {
            console.log("Questions not found in database, running generation model...");
            generateQuestions()
        }
    })
}

generateQuestions = () => {
    let query_url = "https://questgen.ngrok.io/url/" + url;
    fetch(query_url)
    .then(data => {
        return data.json()
    })
    .then(result => {
        questions = result;
        console.log(questions);
        setQuestions(questions);
        writeQuestions(questions);

    })
    .catch(err => {
        console.error(err)
    })
    
};

writeQuestions = (questions) => {
    body = {
        "parameter": {
            "url": encodeURIComponent(url),
            "data": questions
        }
    }
    fetch("https://questgen.ngrok.io/questions/create", {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
        cache: 'default'
    });
}

setQuestions = (questions) => {
    chrome.storage.local.set({'questions': questions[0]}).then(() => { 
        console.log(questions[0]);
        console.log("Questions were set for " + url);
    });
    chrome.storage.local.set({'sources': questions[1]}).then(() => {
        console.log("Sources were set for " + url);
    });
    chrome.storage.local.set({'total_questions': questions[0]}).then(() => { 
    });
}

getQuestions();





