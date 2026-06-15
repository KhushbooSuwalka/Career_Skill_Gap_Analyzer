document.addEventListener("DOMContentLoaded", () => {
    // 1. Scroll to results if present
    document.getElementById("results-section")?.scrollIntoView({ behavior: "smooth", block: "start" });

    // 2. Numeric count-up animation for readiness score
    const scoreEl = document.getElementById("readiness-score-text");
    if (scoreEl) {
        const target = parseInt(scoreEl.getAttribute("data-score"), 10) || 0;
        let count = 0;
        const timer = setInterval(() => {
            count += Math.ceil(target / 40);
            if (count >= target) {
                scoreEl.textContent = `${target}%`;
                clearInterval(timer);
            } else {
                scoreEl.textContent = `${Math.round(count)}%`;
            }
        }, 15);
    }

    // 3. Dynamic career details card preview
    const selectEl = document.getElementById("career-select");
    const detailsCard = document.getElementById("career-details-card");
    const detailsIcon = document.getElementById("career-details-icon");
    const detailsTitle = document.getElementById("career-details-title");
    const detailsDesc = document.getElementById("career-details-desc");
    const detailsSkills = document.getElementById("career-details-skills");

    let careersData = {};
    try {
        const dataScript = document.getElementById("careers-data");
        if (dataScript) careersData = JSON.parse(dataScript.textContent);
    } catch (e) {
        console.error("Error parsing careers data:", e);
    }

    function updateCareerDetails() {
        const selectedId = selectEl.value;
        const data = careersData[selectedId];
        if (data) {
            detailsIcon.textContent = data.icon;
            detailsTitle.textContent = data.title;
            detailsDesc.textContent = data.description;
            detailsSkills.innerHTML = data.skills
                .map(skill => `<span class="bg-[#222f4d] text-[0.8rem] px-2.5 py-1 rounded-full font-medium text-textMuted">${skill}</span>`)
                .join("");
            detailsCard.classList.remove("hidden");
        } else {
            detailsCard.classList.add("hidden");
        }
    }

    if (selectEl) {
        selectEl.addEventListener("change", updateCareerDetails);
        if (selectEl.value) {
            updateCareerDetails();
        }
    }

    // 4. Mirror unsubmitted typed skill before analysis form submit
    const analyzeForm = document.getElementById("analyze-form");
    const skillInput = document.querySelector('input[name="skill"]');
    const hiddenSkillInput = document.getElementById("unadded-skill-hidden");

    if (analyzeForm && skillInput && hiddenSkillInput) {
        analyzeForm.addEventListener("submit", () => {
            hiddenSkillInput.value = skillInput.value.trim();
        });
    }
});

