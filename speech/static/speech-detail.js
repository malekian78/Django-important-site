function syncTranscript(current) {
    const lines = document.querySelectorAll(".line");

    lines.forEach(line => {
        const start = parseFloat(line.dataset.start);
        const end = parseFloat(line.dataset.end);

        if (current >= start && current <= end) {
            line.classList.add("active");
            // line.scrollIntoView({ behavior: "smooth", block: "center" });
        } else {
            line.classList.remove("active");
        }
    });
}




const audio = document.getElementById("audio");
const btnPlay = document.getElementById("btn-play");
// const progress = document.getElementById("ap-progress");
const curr = document.getElementById("ap-current");
const dur = document.getElementById("ap-duration");

function formatTime(sec) {
    if (isNaN(sec)) return "00:00";
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
}

audio.addEventListener("loadedmetadata", () => {
    dur.textContent = formatTime(audio.duration);
    // progress.max = audio.duration;
});

audio.addEventListener("timeupdate", () => {
    curr.textContent = formatTime(audio.currentTime);
    // progress.value = audio.currentTime;

    // Sync Transcript Highlight
    syncTranscript(audio.currentTime);
});

btnPlay.addEventListener("click", () => {
    if (audio.paused) {
        audio.play();
        btnPlay.textContent = "⏸"; // Pause icon
    } else {
        audio.pause();
        btnPlay.textContent = "▶"; // Play icon
    }
});

// progress.addEventListener("input", () => {
//     audio.currentTime = progress.value;
// });

const apBar = document.getElementById("ap-bar");
const apFill = document.getElementById("ap-bar-fill");
const apThumb = document.getElementById("ap-bar-thumb");
const tooltip = document.getElementById("ap-tooltip");

audio.addEventListener("timeupdate", () => {
    const percent = (audio.currentTime / audio.duration) * 100;
    apFill.style.width = percent + "%";
    apThumb.style.left = percent + "%";
});

apBar.addEventListener("click", (e) => {
    const rect = apBar.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const percent = clickX / rect.width;

    audio.currentTime = percent * audio.duration;

    apFill.style.width = (percent * 100) + "%";
    apThumb.style.left = (percent * 100) + "%";
});

apBar.addEventListener("mousemove", (e) => {
    const rect = apBar.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percent = x / rect.width;

    const previewTime = percent * audio.duration;

    // نمایش زمان به فرمت طبیعی
    tooltip.textContent = formatTime(previewTime);

    // موقعیت tooltip
    tooltip.style.left = x + "px";
    tooltip.style.opacity = 1;
});

apBar.addEventListener("mouseleave", () => {
    tooltip.style.opacity = 0;
});