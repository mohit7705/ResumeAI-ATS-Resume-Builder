import { useEffect, useState } from "react";
import { Save } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";

import { useToast } from "../../context/ToastContext";

import {
  getSummary,
  saveSummary,
} from "../../services/personal";

export default function SummaryModule() {
  const toast = useToast();
  const [summary, setSummary] = useState({
    summary: "",
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setSummary(await getSummary());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your summary. Check that the backend is running.");
    }
  }

  async function save() {
    setSaving(true);

    try {
      await saveSummary(summary);
      toast.success("Summary saved.");
    } catch (error) {
      console.error(error);
      toast.error("Could not save your summary. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  const words = summary.summary.trim()
    ? summary.summary.trim().split(/\s+/).length
    : 0;

  return (
    <Container>
      <SectionHeader
        title="Summary"
        subtitle="Two or three sentences that introduce you at the top of your resume."
      />

      <div className="split">
        <Card
          title="Professional summary"
          footer={
            <>
              <span className="card__foot-note">{words} words</span>

              <Button
                icon={<Save size={16} />}
                loading={saving}
                onClick={save}
              >
                Save summary
              </Button>
            </>
          }
        >
          <Field label="Summary">
            <TextArea
              rows={9}
              value={summary.summary}
              onChange={(e) =>
                setSummary({
                  summary: e.target.value,
                })
              }
            />
          </Field>
        </Card>

        <aside className="split__aside">
          <Card title="What works well">
            <ul className="bullets">
              <li>Name your field and level, for example “AI and ML student”.</li>
              <li>Mention two or three core tools you have actually used.</li>
              <li>Say what you want to build or learn next.</li>
              <li>Aim for 40 to 70 words so it fits above the fold.</li>
            </ul>
          </Card>
        </aside>
      </div>
    </Container>
  );
}
