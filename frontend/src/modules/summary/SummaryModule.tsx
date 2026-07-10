import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";

import {
  getSummary,
  saveSummary,
} from "../../services/personal";

export default function SummaryModule() {
  const [summary, setSummary] = useState({
    summary: "",
  });

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setSummary(await getSummary());
  }

  async function save() {
    await saveSummary(summary);
    alert("Summary Saved");
  }

  return (
    <Container>
      <SectionHeader
        title="Summary"
        subtitle="Professional Summary"
      />

      <Card title="Summary">
        <Label>Summary</Label>

        <TextArea
          rows={8}
          value={summary.summary}
          onChange={(e) =>
            setSummary({
              summary: e.target.value,
            })
          }
        />

        <br />

        <Button onClick={save}>
          Save Summary
        </Button>
      </Card>
    </Container>
  );
}