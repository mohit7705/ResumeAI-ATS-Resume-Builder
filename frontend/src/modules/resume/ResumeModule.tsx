import { useState } from "react";
import { generateResume } from "../../services/api";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";
import ResumePreview from "../../components/ResumePreview";

export default function ResumeModule() {
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const skillMatch = result?.skill_match;
  const topProjects = result?.top_projects;

  async function generate() {
    setLoading(true);

    try {
      const data = await generateResume(jobDescription);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Unable to generate resume. Please check your information and try again.");
    } finally {
      setLoading(false);
    }
  }

  function downloadPDF() {
    if (!result?.pdf) return;

    window.open(
      "http://127.0.0.1:8000/generated/pdf/resume.pdf",
      "_blank"
    );
  }

  return (
    <Container>
      <SectionHeader
        title="Resume Generator"
        subtitle="Create an ATS-friendly resume"
      />

      <Card title="Job Description">
        <TextArea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the complete job description here..."
        />

        <br />

        <Button
           onClick={generate}
        >

          {loading
          ? "Generating..."
          : "Generate Resume"}

</Button>
      </Card>

      {loading && (
        <Card title="Status">
          <p>

           Analyzing Job Description...

          <br />

          Matching Skills...

          <br />

          Ranking Projects...

          <br />

          Generating Resume...

          </p>
        </Card>
      )}

      {result && (
        <>
          <Card title="Resume Status">
            <p>
              <strong>Status:</strong>{" "}
              {result.validation?.valid
                ? "Resume Ready"
                : "Resume Needs Information"}
            </p>

            {!result.validation?.valid &&
              result.validation?.missing?.length > 0 && (
                <>
                  <br />

                  <strong>Please complete these fields:</strong>

                  <ul
                    style={{
                      marginTop: 10,
                      paddingLeft: 20,
                      textAlign: "left",
                    }}
                  >
                    {result.validation.missing.map(
                      (field: string) => (
                        <li key={field}>{field}</li>
                      )
                    )}
                  </ul>
                </>
              )}
          </Card>

          <br />
          <br />

<Card title="ATS Analysis">

  <p>
    <strong>ATS Score:</strong> {result.ats_score}%
  </p>

  <p>
    <strong>Skill Score:</strong> {result.skill_score}%
  </p>

  <p>
    <strong>Project Score:</strong> {result.project_score}%
  </p>

</Card>

<br />

<Card title="Matched Skills">

  <ul
    style={{
      paddingLeft:20
    }}
  >

    {skillMatch?.matching_skills?.map(
      (skill:string)=>(
        <li key={skill}>
          {skill}
        </li>
      )
    )}

  </ul>

</Card>

<br />

<Card title="Missing Skills">

  <ul
    style={{
      paddingLeft:20
    }}
  >

    {skillMatch?.missing_skills?.map(
      (skill:string)=>(
        <li key={skill}>
          {skill}
        </li>
      )
    )}

  </ul>

</Card>

<br />

<Card title="AI Recommendations">

  <ul
    style={{
      paddingLeft:20
    }}
  >

    {skillMatch?.recommendations?.map(
      (item:string,index:number)=>(
        <li key={index}>
          {item}
        </li>
      )
    )}

  </ul>

</Card>

<br />

<Card title="Top Ranked Projects">

  {topProjects?.map(
    (project:any,index:number)=>(
      <div
        key={project.title}
        style={{
          marginBottom:15,
          borderBottom:"1px solid #ddd",
          paddingBottom:10
        }}
      >

        <strong>

          {index+1}. {project.title}

        </strong>

        <p>

          Score : {project.score}

        </p>

      </div>
    )
  )}

</Card>

<br />

<Card title="AI Professional Summary">

  <p>

    {result.resume.summary.content}

  </p>

</Card>

<br />

          <Card title="Resume Preview">
            <div
              style={{
                display: "flex",
                gap: 10,
                marginBottom: 15,
              }}
            >
              <Button onClick={downloadPDF}>
                Download PDF
              </Button>
            </div>

            <ResumePreview
              html={result.html}
            />
          </Card>
        </>
      )}
    </Container>
  );
}