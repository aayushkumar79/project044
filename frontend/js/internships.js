requireLogin();
async function loadOpportunities(){
 const box=document.getElementById("opportunities");
 try{const data=await apiRequest(`/recommendations/${getStudentId()}`);const apps=await apiRequest(`/applications/${getStudentId()}`);const applied=apps.applications.map(a=>a.opportunity_id);
 box.innerHTML=data.recommendations.map(o=>`<div class="card opportunity"><h2>${o.title}</h2><p><b>${o.company}</b></p><p>Location: ${o.location||"Not specified"}</p><p>Type: ${o.opportunity_type||"Internship"}</p><p>Matched skills: ${o.matched_skills.length?o.matched_skills.join(", "):"None yet"}</p><h3>${o.match_score}% Match</h3>${applied.includes(o.opportunity_id)?'<span class="status">Applied</span>':`<button class="button" onclick="apply(${o.opportunity_id})">Apply Now</button>`}</div>`).join("")||'<div class="card"><p>No opportunities available yet. Ask an industry user to post one.</p></div>';}catch(e){box.innerHTML=`<div class="card"><p>${e.message}</p></div>`;}
}
async function apply(id){try{await apiRequest("/applications",{method:"POST",body:JSON.stringify({student_id:Number(getStudentId()),opportunity_id:id})});alert("Application submitted successfully!");loadOpportunities();}catch(e){alert(e.message);}}
loadOpportunities();
