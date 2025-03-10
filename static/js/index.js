// Mobile Menu Toggle
document.querySelector(".burger").addEventListener("click", () => {
    document.querySelector(".nav-links").classList.toggle("active");
});

// Smooth Scroll
document.querySelectorAll("a[href^='#']").forEach((link) => {
    link.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        window.scrollTo({
            top: target.offsetTop,
            behavior: "smooth",
        });
    });
});

// Hero Section Animation
window.addEventListener("DOMContentLoaded", () => {
    const heroTitle = document.querySelector(".hero-content h1");
    const heroText = document.querySelector(".hero-content p");
    const heroButton = document.querySelector(".hero-content button");

    heroTitle.style.opacity = "0";
    heroTitle.style.transform = "translateY(-20px)";
    heroText.style.opacity = "0";
    heroText.style.transform = "translateY(20px)";
    heroButton.style.opacity = "0";

    setTimeout(() => {
        heroTitle.style.transition = "all 1s ease-out";
        heroTitle.style.opacity = "1";
        heroTitle.style.transform = "translateY(0)";
    }, 200);

    setTimeout(() => {
        heroText.style.transition = "all 1s ease-out";
        heroText.style.opacity = "1";
        heroText.style.transform = "translateY(0)";
    }, 400);

    setTimeout(() => {
        heroButton.style.transition = "all 0.8s ease-out";
        heroButton.style.opacity = "1";
    }, 600);
});

// Chatbot toggle visibility
document.querySelector("#chatbot-icon").addEventListener("click", () => {
    document.querySelector("#chatbot").style.display = 'flex';
});

document.querySelector("#close-chat").addEventListener("click", () => {
    document.querySelector("#chatbot").style.display = 'none';
});

// Draggable chatbot
let chatbot = document.querySelector("#chatbot");
let drag = false;
let offsetX, offsetY;

chatbot.addEventListener("mousedown", function (e) {
    drag = true;
    offsetX = e.clientX - chatbot.getBoundingClientRect().left;
    offsetY = e.clientY - chatbot.getBoundingClientRect().top;
});

document.addEventListener("mousemove", function (e) {
    if (drag) {
        chatbot.style.left = `${e.clientX - offsetX}px`;
        chatbot.style.top = `${e.clientY - offsetY}px`;
    }
});

document.addEventListener("mouseup", function () {
    drag = false;
});

// Send User Message
document.querySelector("#send-message").addEventListener("click", () => {
    let userInput = document.querySelector("#user-input").value;
    if (userInput.trim() !== "") {
        let userMessage = document.createElement("div");
        userMessage.classList.add("chatbot-message", "user");
        userMessage.textContent = userInput;
        document.querySelector("#chat-content").appendChild(userMessage);

        document.querySelector("#user-input").value = "";

        // Simulate a bot response
        setTimeout(() => {
            let botMessage = document.createElement("div");
            botMessage.classList.add("chatbot-message", "bot");
            botMessage.textContent = "I'm here to assist you!";
            document.querySelector("#chat-content").appendChild(botMessage);
        }, 1000);
    }
});
