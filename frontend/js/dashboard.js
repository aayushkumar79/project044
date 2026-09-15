requireLogin();

async function loadDashboard() {
    const id = getStudentId();
    try {
        const student = await apiRequest(`/student/${id}`);
        const skillsData = await apiRequest(`/skills/${id}`);
        const gapsData = await apiRequest(`/skill-gaps/${id}`);
        const recData = await apiRequest(`/recommendations/${id}`);
        const appsData = await apiRequest(`/applications/${id}`);

        document.querySelector(".hero h1").textContent = `Welcome back, ${student.name}!`;
        document.querySelector(".hero .small").textContent = "STUDENT DASHBOARD";
        document.querySelector(".stat:nth-child(1) strong").textContent = skillsData.skills.length;
        document.querySelector(".stat:nth-child(1) p").textContent = `${skillsData.skills.filter(s => s.skill_level >= 4).length} strong · ${skillsData.skills.filter(s => s.skill_level < 4).length} improving`;
        document.querySelector(".stat:nth-child(2) strong").textContent = recData.recommendations.length;
        document.getElementById("applicationCount").textContent = appsData.applications.length;

        const readiness = skillsData.skills.length ? Math.round(skillsData.skills.reduce((a,s) => a + s.skill_level, 0) / skillsData.skills.length * 20) : 0;
        document.querySelector(".readiness strong").textContent = readiness + "%";
        document.querySelector(".progress-fill").style.width = readiness + "%";

        const profileBox = document.querySelector("section:nth-of-type(3) .card");
        if (skillsData.skills.length) {
            profileBox.innerHTML = skillsData.skills.map(s => {
                const score = s.skill_level * 20;
                return `<div class="skill-row"><span>${s.skill_name}</span><div class="progress"><div class="progress-fill" style="width:${score}%"></div></div><b>${score}%</b></div>`;
            }).join("");
        } else {
            profileBox.innerHTML = "<p>No skills added yet. Add your skills from the Skills page.</p>";
        }

        const gapsBox = document.querySelector("section:nth-of-type(4) .grid");
        gapsBox.innerHTML = gapsData.skill_gaps.length ? gapsData.skill_gaps.slice(0,3).map(g => `<div class="card gap"><b>${g.skill}</b><span>Level ${g.current_level} → ${g.required_level}</span><p>Improve this skill for better opportunity matches.</p></div>`).join("") : `<div class="card"><p>No current skill gaps found.</p></div>`;

        const oppBox = document.querySelector("section:nth-of-type(5) .grid");
        oppBox.innerHTML = recData.recommendations.slice(0,3).map(o => `<div class="card opportunity"><h3>${o.title}</h3><p>${o.company}</p><b>${o.match_score}% Match</b><a href="internships.html">View</a></div>`).join("") || `<div class="card"><p>No opportunities available yet.</p></div>`;
    } catch (error) {
        console.error(error);
    }
}

loadDashboard();
