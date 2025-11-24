document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.querySelector(".menuToggle");
    const navigation = document.querySelector(".navigation");

    menuToggle.addEventListener("click", () => {
        menuToggle.classList.toggle("active");
        navigation.classList.toggle("active");
    });

    window.addEventListener("scroll", () => {
        const header = document.querySelector("header");
        header.classList.toggle("sticky", window.scrollY > 0);
    });
});