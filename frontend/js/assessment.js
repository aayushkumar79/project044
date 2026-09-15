requireLogin();
document.getElementById("assessmentForm").onsubmit=async function(e){
 e.preventDefault();
 let score=0;
 for(let i=1;i<=5;i++){let answer=document.querySelector(`input[name="q${i}"]:checked`);if(answer)score+=Number(answer.value);}
 const percentage=score*20;
 try{
   const id=Number(getStudentId());
   const skills=["Python","SQL","APIs","FastAPI","Data Structures"];
   const values=[document.querySelector('input[name="q1"]:checked')?.value,document.querySelector('input[name="q2"]:checked')?.value,document.querySelector('input[name="q3"]:checked')?.value,document.querySelector('input[name="q4"]:checked')?.value,document.querySelector('input[name="q5"]:checked')?.value];
   for(let i=0;i<skills.length;i++){await apiRequest("/assessment",{method:"POST",body:JSON.stringify({student_id:id,skill_name:skills[i],score:Number(values[i]||0)*100})}); await apiRequest("/skills",{method:"POST",body:JSON.stringify({student_id:id,skill_name:skills[i],skill_level:Math.max(1,Math.ceil(Number(values[i]||0)*5))})});}
   document.getElementById("result").innerHTML=`<div class="result-card"><h2>Assessment Complete</h2><p>Your score is <strong>${percentage}%</strong>.</p><p>Your results have been saved to your SkillFill profile.</p><a class="button" href="internships.html">See Recommendations</a></div>`;
 }catch(error){document.getElementById("result").innerHTML=`<div class="result-card"><p>${error.message}</p></div>`;}
};
