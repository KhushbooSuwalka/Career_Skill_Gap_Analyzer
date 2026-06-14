/**
 * Career Skill Gap Analyzer - Core Logic
 * Handles interactive skill addition, career selection, gap analysis, and dynamic roadmaps.
 */

// 1. Careers Database: Defines requirements and learning roadmaps for each target career
const CAREER_DATABASE = {
    "frontend-dev": {
        title: "Frontend Developer",
        description: "Builds user interfaces and dynamic web applications.",
        requiredSkills: ["HTML", "CSS", "JavaScript", "React", "Git", "Webpack"],
        roadmap: [
            { skill: "HTML", phase: "Phase 1: Structure", topic: "Master semantic markup, SEO basics, and modern web accessibility (A11y)." },
            { skill: "CSS", phase: "Phase 1: Styling", topic: "Learn Flexbox, CSS Grid, custom variables, responsive design, and CSS transitions." },
            { skill: "JavaScript", phase: "Phase 2: Interactivity", topic: "Understand ES6+ features, asynchronous programming (APIs/Fetch), and DOM manipulation." },
            { skill: "Git", phase: "Phase 2: Version Control", topic: "Learn Git branching, merging, pull requests, and collaborative workflows on GitHub." },
            { skill: "React", phase: "Phase 3: Frontend Framework", topic: "Learn React component lifecycle, Hooks (useState, useEffect), state management, and routing." },
            { skill: "Webpack", phase: "Phase 4: Tooling & Deploy", topic: "Learn build tools (Vite/Webpack), package managers (npm), and hosting platforms (Netlify/Vercel)." }
        ]
    },
    "data-scientist": {
        title: "Data Scientist",
        description: "Analyzes datasets to build machine learning models and extract insights.",
        requiredSkills: ["Python", "SQL", "Pandas", "Machine Learning", "Statistics", "Data Visualization"],
        roadmap: [
            { skill: "Python", phase: "Phase 1: Programming Basics", topic: "Learn core Python programming, data structures, loops, and custom functions." },
            { skill: "SQL", phase: "Phase 1: Database Querying", topic: "Master relational database structures, complex Joins, Subqueries, and data grouping." },
            { skill: "Pandas", phase: "Phase 2: Data Manipulation", topic: "Master Pandas and NumPy for cleaning, filtering, and preparing messy tabular datasets." },
            { skill: "Data Visualization", phase: "Phase 2: Storytelling", topic: "Learn data communication using Matplotlib, Seaborn, or interactive BI dashboards." },
            { skill: "Statistics", phase: "Phase 3: Mathematical Core", topic: "Learn hypothesis testing, regression analysis, probability models, and sampling distributions." },
            { skill: "Machine Learning", phase: "Phase 4: Predictive Models", topic: "Build models using Scikit-Learn (regression, trees, clustering) and evaluate performance." }
        ]
    },
    "product-manager": {
        title: "Product Manager",
        description: "Leads the design, execution, and release of new software products.",
        requiredSkills: ["Agile/Scrum", "Product Strategy", "User Research", "Data Analytics", "Wireframing", "Roadmapping"],
        roadmap: [
            { skill: "Agile/Scrum", phase: "Phase 1: Project Methodologies", topic: "Understand sprints, daily standups, backlog grooming, and issue tracking in Jira." },
            { skill: "User Research", phase: "Phase 1: Empathy & Needs", topic: "Conduct user interviews, design feedback surveys, and build target user personas." },
            { skill: "Wireframing", phase: "Phase 2: UX Prototyping", topic: "Learn basic layout prototyping and visual mockup creation using Figma or Balsamiq." },
            { skill: "Data Analytics", phase: "Phase 2: Product Metrics", topic: "Understand key metrics (AARRR funnel, retention), funnel conversions, and tracking platforms." },
            { skill: "Roadmapping", phase: "Phase 3: Prioritization", topic: "Learn feature estimation, MoSCoW prioritization, and building timelines with product planning software." },
            { skill: "Product Strategy", phase: "Phase 4: Market Validation", topic: "Define product positioning, analyze competitors, write PRDs, and coordinate launch plans." }
        ]
    },
    "cybersecurity-analyst": {
        title: "Cyber Security Analyst",
        description: "Monitors and secures computer networks, systems, and sensitive data.",
        requiredSkills: ["Networking", "Linux", "Ethical Hacking", "Cryptography", "Security Auditing", "Wireshark"],
        roadmap: [
            { skill: "Networking", phase: "Phase 1: Core Networking", topic: "Learn TCP/IP layers, routing protocols, subnets, ports, DNS, and local host configurations." },
            { skill: "Linux", phase: "Phase 1: Admin Basics", topic: "Master command-line operations, shell scripts, user permissions, and directory trees." },
            { skill: "Wireshark", phase: "Phase 2: Traffic Inspection", topic: "Learn to capture and analyze network packets to identify security anomalies." },
            { skill: "Cryptography", phase: "Phase 2: Safe Encryption", topic: "Understand symmetric/asymmetric encryption, hashing algorithms, and SSL/TLS standards." },
            { skill: "Ethical Hacking", phase: "Phase 3: Vulnerabilities", topic: "Perform network vulnerability scanning with Nmap and understand OWASP Top 10 vulnerabilities." },
            { skill: "Security Auditing", phase: "Phase 4: Governance & SIEM", topic: "Learn standard security frameworks (NIST, ISO), log auditing, and SIEM monitoring dashboards." }
        ]
    }
};

// 2. Global State Variables
let userSkills = ["HTML", "CSS", "Python"]; // Prepopulated with some starter skills
let selectedCareerId = "";

// 3. DOM Elements
const skillInput = document.getElementById("skill-input");
const btnAddSkill = document.getElementById("btn-add-skill");
const skillsContainer = document.getElementById("skills-container");
const careerCards = document.querySelectorAll(".career-card");
const btnAnalyze = document.getElementById("btn-analyze");
const resultsSection = document.getElementById("results-section");

// 4. Initial Setup / Event Listeners
document.addEventListener("DOMContentLoaded", () => {
    // Render starting prepopulated skills
    renderSkills();

    // Event listener: Add skill button click
    btnAddSkill.addEventListener("click", handleSkillInput);

    // Event listener: Enter key in skill input field
    skillInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            handleSkillInput();
        }
    });

    // Event listener: Career selection cards
    careerCards.forEach(card => {
        card.addEventListener("click", () => {
            // Remove active style from all cards
            careerCards.forEach(c => c.classList.remove("active"));
            
            // Add active style to selected card
            card.classList.add("active");
            
            // Save selected career ID
            selectedCareerId = card.getAttribute("data-career");
        });
    });

    // Event listener: Click on preset skill suggestions
    document.querySelectorAll(".btn-suggestion").forEach(btn => {
        btn.addEventListener("click", () => {
            const suggestedSkill = btn.getAttribute("data-skill");
            addSkill(suggestedSkill);
        });
    });

    // Event listener: Perform analysis
    btnAnalyze.addEventListener("click", analyzeGap);
});

// 5. Skill Addition / Removal Handlers
function handleSkillInput() {
    const rawSkillValue = skillInput.value.trim();
    if (rawSkillValue) {
        addSkill(rawSkillValue);
        skillInput.value = ""; // Clear input field
        skillInput.focus();
    }
}

function addSkill(skillName) {
    // Standardize input (e.g., capitalize correctly like "React" or "Python")
    const formattedName = formatSkillName(skillName);
    
    // Prevent empty inputs or duplicate additions
    if (formattedName && !userSkills.includes(formattedName)) {
        userSkills.push(formattedName);
        renderSkills();
    }
}

function removeSkill(skillToRemove) {
    userSkills = userSkills.filter(skill => skill !== skillToRemove);
    renderSkills();
}

// Format utility to make raw strings look professional
function formatSkillName(str) {
    if (!str) return "";
    
    const uppercaseSkills = ["html", "css", "sql", "js", "api", "ux", "siem", "it", "dns", "tcp/ip", "prd"];
    const lowercase = str.toLowerCase();
    
    if (uppercaseSkills.includes(lowercase)) {
        return lowercase.toUpperCase();
    }
    
    // Capitalize first letter of each word (e.g. "machine learning")
    return str.split(' ')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
              .join(' ');
}

// Redraws the visual skill tags inside Step 1
function renderSkills() {
    skillsContainer.innerHTML = "";
    
    if (userSkills.length === 0) {
        skillsContainer.innerHTML = `<span class="empty-state">No skills added yet. Use the input box or suggestions below to start!</span>`;
        return;
    }

    userSkills.forEach(skill => {
        const skillPill = document.createElement("span");
        skillPill.className = "skill-pill";
        skillPill.innerHTML = `
            ${skill}
            <button type="button" class="skill-pill-remove" aria-label="Remove ${skill}">&times;</button>
        `;
        
        // Remove button click listener
        skillPill.querySelector(".skill-pill-remove").addEventListener("click", () => {
            removeSkill(skill);
        });
        
        skillsContainer.appendChild(skillPill);
    });
}

// 6. Skill Gap Analysis & Roadmap Generation
function analyzeGap() {
    // Input validation: Must select a career path
    if (!selectedCareerId) {
        alert("Please select a target career path in Step 2 to perform the analysis!");
        return;
    }

    const career = CAREER_DATABASE[selectedCareerId];
    const required = career.requiredSkills;

    // Convert both arrays to uppercase for accurate comparison
    const userSkillsUpper = userSkills.map(s => s.toUpperCase());
    
    // Divide required skills into "matched" and "missing"
    const matchedSkills = [];
    const missingSkills = [];

    required.forEach(skill => {
        if (userSkillsUpper.includes(skill.toUpperCase())) {
            matchedSkills.push(skill);
        } else {
            missingSkills.push(skill);
        }
    });

    // Calculate Readiness Score
    const totalRequired = required.length;
    const totalMatched = matchedSkills.length;
    const readinessScore = Math.round((totalMatched / totalRequired) * 100);

    // Update UI elements
    updateReadinessUI(readinessScore);
    updateSkillsBreakdownUI(matchedSkills, missingSkills);
    generateRoadmapUI(career, missingSkills);

    // Reveal and scroll smoothly to Results
    resultsSection.style.display = "block";
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

// Updates circular score indicator and rating levels
function updateReadinessUI(score) {
    const scoreTextEl = document.getElementById("readiness-score-text");
    const circleEl = document.getElementById("progress-circle");
    const labelEl = document.getElementById("readiness-label");
    const descEl = document.getElementById("readiness-desc");

    // Animate circular SVG stroke
    // Radius of circle = 70; Circumference = 2 * PI * 70 = 439.82 (~440)
    const circumference = 440;
    circleEl.style.strokeDasharray = circumference;
    const offset = circumference - (score / 100) * circumference;
    circleEl.style.strokeDashoffset = offset;

    // Counter counting up
    let startVal = 0;
    const duration = 600; // ms
    const stepTime = 15;
    const steps = duration / stepTime;
    const increment = score / steps;
    
    const timer = setInterval(() => {
        startVal += increment;
        if (startVal >= score) {
            scoreTextEl.textContent = `${score}%`;
            clearInterval(timer);
        } else {
            scoreTextEl.textContent = `${Math.round(startVal)}%`;
        }
    }, stepTime);

    // Determine readiness assessment label
    labelEl.className = "readiness-level";
    if (score >= 80) {
        labelEl.textContent = "Career Ready";
        labelEl.classList.add("level-high");
        descEl.textContent = "Incredible work! You possess almost all the core skills needed for this target role. Focus on minor refinements or building a standout capstone project.";
    } else if (score >= 40) {
        labelEl.textContent = "Moderate Fit";
        labelEl.classList.add("level-medium");
        descEl.textContent = "You have a solid foundation, but there are important skills missing. Follow the learning roadmap below to bridge the remaining gaps.";
    } else {
        labelEl.textContent = "Aspiring";
        labelEl.classList.add("level-low");
        descEl.textContent = "You're at the beginning of your journey for this career. Don't worry! Everyone starts somewhere. Follow the structured roadmap step-by-step to build up your skillset.";
    }
}

// Renders the badges in the Results lists
function updateSkillsBreakdownUI(matched, missing) {
    const matchedContainer = document.getElementById("matched-skills-list");
    const missingContainer = document.getElementById("missing-skills-list");
    const matchedCount = document.getElementById("matched-count");
    const missingCount = document.getElementById("missing-count");

    // Update numbers
    matchedCount.textContent = matched.length;
    missingCount.textContent = missing.length;

    // Matched skills pills
    matchedContainer.innerHTML = "";
    if (matched.length === 0) {
        matchedContainer.innerHTML = `<span class="empty-state">No matching skills yet. Add more of your skills in Step 1!</span>`;
    } else {
        matched.forEach(skill => {
            matchedContainer.innerHTML += `<span class="result-pill has">✓ ${skill}</span>`;
        });
    }

    // Missing skills pills
    missingContainer.innerHTML = "";
    if (missing.length === 0) {
        missingContainer.innerHTML = `<span class="empty-state">No missing skills! You've got it all.</span>`;
    } else {
        missing.forEach(skill => {
            missingContainer.innerHTML += `<span class="result-pill missing">✗ ${skill}</span>`;
        });
    }
}

// Builds the visual vertical timeline roadmap based on missing skills
function generateRoadmapUI(career, missingSkills) {
    const timelineEl = document.getElementById("roadmap-timeline");
    timelineEl.innerHTML = "";

    const missingSkillsUpper = missingSkills.map(s => s.toUpperCase());

    // Filter roadmap phases: if the skill is in missingSkills, show it as an active training step.
    // If the skill is already matched, show it as a completed milestone!
    let index = 1;
    career.roadmap.forEach((step) => {
        const isMissing = missingSkillsUpper.includes(step.skill.toUpperCase());
        
        const stepEl = document.createElement("div");
        stepEl.className = `roadmap-step ${!isMissing ? 'completed' : ''}`;
        
        stepEl.innerHTML = `
            <div class="roadmap-step-phase">${step.phase} ${!isMissing ? '✓ (Acquired)' : '• (Learn Next)'}</div>
            <div class="roadmap-step-title">${step.skill}: ${!isMissing ? 'Verified Skill' : 'Gap Identified'}</div>
            <div class="roadmap-step-desc">${isMissing ? step.topic : `You already know <strong>${step.skill}</strong>. This foundational step is completed!`}</div>
        `;
        timelineEl.appendChild(stepEl);
        index++;
    });
    
    // If there were no gaps at all
    if (missingSkills.length === 0) {
        const successMessage = document.createElement("div");
        successMessage.className = "roadmap-step completed";
        successMessage.innerHTML = `
            <div class="roadmap-step-phase" style="color: var(--success)">Fully Prepared</div>
            <div class="roadmap-step-title">All Gaps Solved!</div>
            <div class="roadmap-step-desc">You match all required core skills for ${career.title}. Next steps: build portfolio projects, update your resume, and start applying!</div>
        `;
        timelineEl.prepend(successMessage);
    }
}
