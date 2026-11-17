import { useEffect, useRef, useState } from "react";
import axios from "axios";
import {
  AlignLeft,
  Check,
  Download,
  FileText,
  Info,
  Pencil,
  Sparkles,
  Type,
} from "lucide-react";

import {
  generateResume,
  generateResumeFromTitle,
  getProviders,
  type Provider,
  type ProviderStatus,
  type ResumeLevel,
} from "../../services/api";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import TextArea from "../../components/ui/TextArea";
import Input from "../../components/ui/Input";
import Select from "../../components/ui/Select";
import Button from "../../components/ui/Button";
import Chip from "../../components/ui/Chip";
import Ring from "../../components/ui/Ring";
import Toggle from "../../components/ui/Toggle";
import ResumePreview from "../../components/ResumePreview";
import RecruiterCheck from "../../components/RecruiterCheck";
import { useToast } from "../../context/ToastContext";

const ROLE_SUGGESTIONS = [
  "Software Engineer",
  "Backend Developer",
  "Full Stack Developer",
  "AI/ML Engineer",
  "Python Developer",
  "AEM Developer",
];

function scoreTone(value: number): "ok" | "accent" | "warn" {
  if (value >= 75) return "ok";
  if (value >= 50) return "accent";
  return "warn";
}

export default function ResumeModule() {
  const toast = useToast();

  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<"jd" | "title">("jd");
  const [title, setTitle] = useState("");
  const [level, setLevel] = useState<ResumeLevel>("Fresher");
  const [highlight, setHighlight] = useState(true);
  const [provider, setProvider] = useState<Provider>(() => {
    try {
      return localStorage.getItem("resumeai.provider") === "meta" ? "meta" : "gemini";
    } catch {
      return "gemini";
    }
  });
  const [providers, setProviders] = useState<ProviderStatus | null>(null);
  const [version, setVersion] = useState(0);
  const resultsRef = useRef<HTMLDivElement>(null);
  const skillMatch = result?.skill_match;
  const topProjects = result?.top_projects;

  function chooseProvider(next: Provider) {
    setProvider(next);
    try {
      localStorage.setItem("resumeai.provider", next);
    } catch {
      /* private window: choice just is not remembered */
    }
  }

  useEffect(() => {
    getProviders()
      .then((status) => {
        setProviders(status);
        setProvider((current) => (status[current].available ? current : status.default));
      })
      .catch(() => setProviders(null));
  }, []);

  const providerName = provider === "meta" ? "Meta" : "Gemini";

  // Bring the results into view after each successful generation.
  useEffect(() => {
    if (version > 0) {
      resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [version]);

  async function generate() {
    if (mode === "title" && !title.trim()) {
      toast.info("Enter a job title first.");
      return;
    }

    setLoading(true);

    try {
      const data =
        mode === "title"
          ? await generateResumeFromTitle(title.trim(), level, highlight, provider)
          : await generateResume(jobDescription, highlight, provider);
      setResult(data);
      setVersion((v) => v + 1);
      toast.success("Resume generated.");
    } catch (err) {
      console.error(err);
      const detail =
        axios.isAxiosError(err) && typeof err.response?.data?.detail === "string"
          ? err.response.data.detail
          : null;
      const isBadRequest = axios.isAxiosError(err) && err.response?.status === 400;
      toast.error(
        detail && isBadRequest
          ? detail
          : "Unable to generate resume. Please check your information and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function editGeneratedJobDescription() {
    if (!result?.generated_job_description) return;

    setJobDescription(result.generated_job_description);
    setMode("jd");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function downloadPDF() {
    if (!result?.pdf) return;

    window.open(
      `/${String(result.pdf).replace(/\\/g, "/").replace(/^\/+/, "")}`,
      "_blank"
    );
  }

  function downloadPhotoPDF() {
    if (!result?.photo_pdf) return;

    window.open(
      `/${String(result.photo_pdf).replace(/\\/g, "/").replace(/^\/+/, "")}`,
      "_blank"
    );
  }

  const ready = Boolean(result?.validation?.valid);
  const missingFields: string[] = result?.validation?.missing ?? [];

  return (
    <Container>
      <SectionHeader
        title="Resume generator"
        subtitle="Paste a job description or pick a role. We match your skills and projects to it."
      />

      <Card
        title={mode === "jd" ? "Job description" : "Job title"}
        action={
          <div className="segmented" role="tablist" aria-label="Input type">
            <button
              type="button"
              role="tab"
              aria-selected={mode === "jd"}
              onClick={() => setMode("jd")}
            >
              <AlignLeft size={16} />
              Paste job description
            </button>

            <button
              type="button"
              role="tab"
              aria-selected={mode === "title"}
              onClick={() => setMode("title")}
            >
              <Type size={16} />
              Enter job title
            </button>
          </div>
        }
        footer={
          <>
            <Toggle
              checked={highlight}
              onChange={(e) => setHighlight(e.target.checked)}
            >
              Bold the job keywords in the resume
            </Toggle>

            <span style={{ flex: 1 }} />

            <div className="segmented" role="tablist" aria-label="AI provider">
              {(["gemini", "meta"] as Provider[]).map((name) => {
                const info = providers?.[name];
                const missing = providers !== null && !info?.available;

                return (
                  <button
                    key={name}
                    type="button"
                    role="tab"
                    aria-selected={provider === name}
                    disabled={missing}
                    title={
                      missing
                        ? `Add the ${name === "meta" ? "META" : "GOOGLE"} key and model to .env`
                        : info?.model || undefined
                    }
                    onClick={() => chooseProvider(name)}
                  >
                    {name === "meta" ? "Meta" : "Gemini"}
                  </button>
                );
              })}
            </div>

            <Button
              size="lg"
              icon={<Sparkles size={18} />}
              onClick={generate}
              loading={loading}
            >
              {loading ? "Generating…" : `Generate with ${providerName}`}
            </Button>
          </>
        }
      >
        {mode === "jd" ? (
          <Field label="Job description" hint="Paste the full posting for the best match.">
            <TextArea
              rows={10}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the complete job description here..."
            />
          </Field>
        ) : (
          <div className="form-grid">
            <Field label="Job title" wide>
              <Input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Backend Developer, Full Stack Developer, AEM Developer"
                maxLength={80}
              />
            </Field>

            <div className="span-2">
              <div className="label" style={{ marginBottom: 8 }}>
                Popular roles
              </div>

              <div className="chip-picker">
                {ROLE_SUGGESTIONS.map((role) => (
                  <button
                    key={role}
                    type="button"
                    className={title === role ? "chip chip--accent" : "chip"}
                    onClick={() => setTitle(role)}
                  >
                    {title === role && <Check size={14} />}
                    {role}
                  </button>
                ))}
              </div>
            </div>

            <Field label="Experience level">
              <Select
                value={level}
                onChange={(e) => setLevel(e.target.value as ResumeLevel)}
              >
                <option value="Fresher">Fresher</option>
                <option value="Junior">Junior (0-2 years)</option>
              </Select>
            </Field>
          </div>
        )}

        {loading && (
          <>
            <div className="progress" role="progressbar" aria-label="Generating resume" />
            <p className="muted" style={{ marginTop: 10 }}>
              Analyzing the job, matching your skills, ranking your projects and
              building the resume.
            </p>
          </>
        )}
      </Card>

      {result && (
        <div ref={resultsRef} className="stack section-gap" style={{ scrollMarginTop: 84 }}>
          <h2 className="section-title">Your results</h2>

          <Card
            title="ATS analysis"
            action={
              ready ? (
                <span className="badge badge--ok">
                  <Check size={14} />
                  Resume ready
                </span>
              ) : (
                <span className="badge badge--warn">
                  <Info size={14} />
                  Needs information
                </span>
              )
            }
          >
            <div className="score-row">
              {[
                { label: "ATS score", value: result.ats_score },
                { label: "Skill score", value: result.skill_score },
                { label: "Project score", value: result.project_score },
              ].map((score) => {
                const numeric = Number(score.value);

                return (
                  <div className="score" key={score.label}>
                    <Ring
                      small
                      size={112}
                      stroke={9}
                      value={numeric}
                      tone={scoreTone(numeric)}
                    />
                    <span className="score__label">{score.label}</span>
                  </div>
                );
              })}
            </div>

            <RecruiterCheck data={result.recruiter_check} />

            {result.provider && (
              <p className="label" style={{ marginTop: 16 }}>
                Generated with {result.provider === "meta" ? "Meta" : "Gemini"}
                {result.model ? ` (${result.model})` : ""}
                {result.seconds ? ` in ${result.seconds} s` : ""}
              </p>
            )}

            {!ready && missingFields.length > 0 && (
              <div style={{ marginTop: 24 }}>
                <p className="label" style={{ marginBottom: 8 }}>
                  Please complete these fields:
                </p>

                <div className="chips">
                  {missingFields.map((field: string) => (
                    <Chip key={field} tone="warn">
                      {field}
                    </Chip>
                  ))}
                </div>
              </div>
            )}
          </Card>

          <div className="result-grid">
            <Card
              title="Matched skills"
              description="Skills from your profile that the job asks for."
            >
              {skillMatch?.matching_skills?.length > 0 ? (
                <div className="chips">
                  {skillMatch.matching_skills.map((skill: string) => (
                    <Chip key={skill} tone="ok">
                      {skill}
                    </Chip>
                  ))}
                </div>
              ) : (
                <p className="muted">No matching skills found.</p>
              )}
            </Card>

            <Card
              title="Missing skills"
              description="Asked for by the job but not on your profile."
            >
              {skillMatch?.missing_skills?.length > 0 ? (
                <div className="chips">
                  {skillMatch.missing_skills.map((skill: string) => (
                    <Chip key={skill} tone="warn">
                      {skill}
                    </Chip>
                  ))}
                </div>
              ) : (
                <p className="muted">Nothing missing. Great match.</p>
              )}
            </Card>

            <Card title="AI recommendations">
              {skillMatch?.recommendations?.length > 0 ? (
                <ul className="bullets">
                  {skillMatch.recommendations.map(
                    (item: string, index: number) => (
                      <li key={index}>{item}</li>
                    )
                  )}
                </ul>
              ) : (
                <p className="muted">No recommendations for this job.</p>
              )}
            </Card>

            <Card
              title="Top ranked projects"
              description="The projects used on your resume."
            >
              {topProjects?.length > 0 ? (
                <ol className="ranked">
                  {topProjects.map((project: any, index: number) => {
                    const score = Number(project.score);
                    const width = Number.isFinite(score)
                      ? Math.min(100, Math.max(0, score <= 1 ? score * 100 : score))
                      : 0;

                    return (
                      <li key={project.title}>
                        <span className="ranked__n">{index + 1}</span>

                        <div>
                          <div className="ranked__title">{project.title}</div>
                          <div className="ranked__bar">
                            <span style={{ width: `${width}%` }} />
                          </div>
                        </div>

                        <span className="ranked__score">{project.score}</span>
                      </li>
                    );
                  })}
                </ol>
              ) : (
                <p className="muted">No ranked projects.</p>
              )}
            </Card>
          </div>

          {result.highlighted_keywords?.length > 0 && (
            <Card
              title="Highlighted keywords"
              description="These appear in bold on your resume."
            >
              <div className="chips">
                {result.highlighted_keywords.map((keyword: string) => (
                  <Chip key={keyword} tone="accent">
                    {keyword}
                  </Chip>
                ))}
              </div>
            </Card>
          )}

          {result.resume?.summary?.content && (
            <Card title="AI professional summary">
              <p className="prose">{result.resume.summary.content}</p>
            </Card>
          )}

          {result.generated_job_description && (
            <Card
              title="Generated job description"
              action={
                <Button
                  variant="secondary"
                  size="sm"
                  icon={<Pencil size={14} />}
                  onClick={editGeneratedJobDescription}
                >
                  Edit as job description
                </Button>
              }
            >
              <p className="prose">{result.generated_job_description}</p>
            </Card>
          )}

          <Card
            title="Resume preview"
            action={
              <div className="toolbar">
                <Button
                  variant="secondary"
                  size="sm"
                  icon={<Download size={14} />}
                  onClick={downloadPDF}
                >
                  Download without photo
                </Button>

                <Button
                  size="sm"
                  icon={<Download size={14} />}
                  onClick={downloadPhotoPDF}
                >
                  Download with photo
                </Button>
              </div>
            }
          >
            <div className="preview-grid">
              <div>
                <h3 className="preview-title">Resume without photo</h3>
                <ResumePreview html={result.html} version={version} />
              </div>

              {result.photo_html && (
                <div>
                  <h3 className="preview-title">Resume with photo</h3>
                  <ResumePreview html={result.photo_html} version={version} />
                </div>
              )}
            </div>

            {!result.html && (
              <p className="muted" style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <FileText size={16} />
                No preview was returned for this resume.
              </p>
            )}
          </Card>
        </div>
      )}
    </Container>
  );
}
