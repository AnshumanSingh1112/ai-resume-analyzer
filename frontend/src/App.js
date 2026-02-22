import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState("software_developer");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please upload a resume PDF");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("role", role);

    try {
      setLoading(true);
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze/",
        formData
      );
      setResult(response.data);
    } catch (error) {
      alert("Backend not connected");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1>🚀 AI Resume Skill Gap & ATS Analyzer</h1>

        <form className="upload-card" onSubmit={handleSubmit}>
          <label className="file-upload">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />
            {file ? file.name : "Upload Resume (PDF)"}
          </label>

          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="software_developer">Software Developer</option>
            <option value="data_analyst">Data Analyst</option>
            <option value="full_stack_developer">Full Stack Developer</option>
            <option value="backend_developer">Backend Developer</option>
            <option value="frontend_developer">Frontend Developer</option>
            <option value="machine_learning_engineer">
              Machine Learning Engineer
            </option>
          </select>

          <button type="submit">
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </form>

        {result && (
          <div className="results-card">
            <h2>Skill Match</h2>

            <div className="progress-bar">
              <div
                className="progress"
                style={{ width: `${result.skill_match_percentage}%` }}
              >
                {result.skill_match_percentage}%
              </div>
            </div>

            <h3>Matched Skills</h3>
            <div className="tags green">
              {result.matched_skills.map((skill, index) => (
                <span key={index}>{skill}</span>
              ))}
            </div>

            <h3>Missing Skills</h3>
            <div className="tags red">
              {result.missing_skills.map((skill, index) => (
                <span key={index}>{skill}</span>
              ))}
            </div>

            <h3>Learning Roadmap</h3>
            {result.learning_roadmap.map((item, index) => (
              <div key={index} className="roadmap">
                <strong>{item.skill}</strong>
                <ul>
                  <li>{item.plan.week_1}</li>
                  <li>{item.plan.week_2}</li>
                  <li>{item.plan.practice}</li>
                </ul>
              </div>
            ))}

            <h3>Recommended Roles</h3>
            <div className="roles">
              {result.recommended_roles.map((r, index) => (
                <div key={index} className="role-card">
                  {r.role.replace(/_/g, " ")}
                  <span>{r.match}%</span>
                </div>
              ))}
            </div>

            <h3>ATS Suggestions</h3>
            <ul>
              {result.ats_suggestions.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
