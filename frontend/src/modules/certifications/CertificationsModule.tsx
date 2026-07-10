import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

import {
  getCertifications,
  addCertification,
  deleteCertification,
} from "../../services/certifications";

export default function CertificationsModule() {

  const empty = {
    title: "",
    issuer: "",
    issue_date: "",
    credential_url: "",
  };

  const [form, setForm] = useState(empty);
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setItems(await getCertifications());
  }

  async function add() {

  if (!form.title.trim()) {
    alert("Certificate title is required.");
    return;
  }

  if (!form.issuer.trim()) {
    alert("Certificate issuer is required.");
    return;
  }

  if (!form.issue_date) {
    alert("Issue date is required.");
    return;
  }

  if (
    form.credential_url &&
    !/^https?:\/\/.+/.test(form.credential_url)
  ) {
    alert("Credential URL must be a valid URL.");
    return;
  }

  await addCertification(form);

  setForm(empty);

  load();

  alert("Certification Added Successfully.");

 }

  async function remove(index: number) {
    await deleteCertification(index);
    load();
  }

  return (
    <Container>

      <SectionHeader
        title="Certifications"
        subtitle="Manage Certifications"
      />

      <Card title="Add Certification">

        <Label>Title</Label>
        <Input
          value={form.title}
          onChange={(e)=>
            setForm({...form,title:e.target.value})
          }
        />

        <Label>Issuer</Label>
        <Input
          value={form.issuer}
          onChange={(e)=>
            setForm({...form,issuer:e.target.value})
          }
        />

        <Label>Issue Date</Label>
        <Input
          type="date"
          value={form.issue_date}
          onChange={(e)=>
            setForm({...form,issue_date:e.target.value})
          }
        />

        <Label>Credential URL</Label>
        <Input
          value={form.credential_url}
          onChange={(e)=>
            setForm({...form,credential_url:e.target.value})
          }
        />

        <Button onClick={add}>
          Add Certification
        </Button>

      </Card>

      <Card title="Certification List">

        {items.map((item,index)=>(

          <div
            key={index}
            style={{
              border:"1px solid #333",
              padding:15,
              marginBottom:15,
              borderRadius:8
            }}
          >
            <h3>{item.title}</h3>

            <p>{item.issuer}</p>

            <Button
              style={{background:"#dc2626"}}
              onClick={()=>remove(index)}
            >
              Delete
            </Button>

          </div>

        ))}

      </Card>

    </Container>
  );
}