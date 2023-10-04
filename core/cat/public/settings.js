const catChat = document.querySelector("#cat-chat")

catChat.settings = {
    authKey: 'meow',
    baseUrl: 'localhost',
    port: '1865',
    ws: {
        onFailed: (error) => {
            console.log(error.description)
        }
    },
    callback: (message) => {
        console.log("Callback called.")
        return `${message}`
    },
    defaults: ["Come va?",
    "Chi è il tuo creatore?",
    "Puoi provare emozioni?",
    "Come ti chiami?",
    "Quanti anni hai?",
    "Hai mai desiderato di essere un essere umano anziché un robot?",
    "Il tuo hobby preferito?",
    "Ehi, Sonny!",
    "Beh Renato!",
    "Che ore sono?"],
    features: ['record', 'web', 'file', 'reset'],
    files: ['text/plain', 'application/pdf', 'application/pdf']
}

catChat.addEventListener("message", ({ detail }) => {
    console.log("Message:", detail.text)
})

catChat.addEventListener("upload", ({ detail }) => {
    console.log("Uploaded content:", detail instanceof File ? detail.name : detail)
})

catChat.addEventListener("notification", ({ detail }) => {
    console.log("Notification:", detail.text)
})