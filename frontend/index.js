const url = document.getElementById('url');
const start_button = document.getElementById('Startbtn')

start_button.addEventListener("click", () => {
    sendUrl()
});

sendUrl = () => {
    chrome.storage.local.set({'url': url.value}).then(() => { 
        console.log(url.value + " was set");
    });
}