import { useEffect, useState } from "react";
import { Award, Calendar, ExternalLink, Plus } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Chip from "../../components/ui/Chip";
import EmptyState from "../../components/ui/EmptyState";
import DeleteButton from "../../components/ui/DeleteButton";

import { useToast } from "../../context/ToastContext";
import { formatDate } from "../../utils/format";

import {
  getCertifications,
  addCertification,
  deleteCertification,
} from "../../services/certifications";

export default function CertificationsModule() {
  const toast = useToast();

  const empty = {
    title: "",
    issuer: "",
    issue_date: "",
    credential_url: "",
  };

  const [form, setForm] = useState(empty);
  const [items, setItems] = useState<any[]>([]);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setItems(await getCertifications());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your certifications. Check that the backend is running.");
    }
  }

  async function add() {

    if (!form.title.trim()) {
      toast.error("Certificate title is required.");
      return;
    }

    if (!form.issuer.trim()) {
      toast.error("Certificate issuer is required.");
      return;
    }

    if (!form.issue_date) {
      toast.error("Issue date is required.");
      return;
    }

    if (
      form.credential_url &&
      !/^https?:\/\/.+/.test(form.credential_url)
    ) {
      toast.error("Credential URL must be a valid URL.");
      return;
    }

    setSaving(true);

    try {
      await addCertification(form);

      setForm(empty);

      load();

      toast.success("Certification added.");
    } catch (error) {
      console.error(error);
      toast.error("Could not add this certification. Please try again.");
    } finally {
      setSaving(false);
    }

  }

  async function remove(index: number) {
    try {
      await deleteCertification(index);
      load();
      toast.success("Certification removed.");
    } catch (error) {
      console.error(error);
      toast.error("Could not remove this certification. Please try again.");
    }
  }

  return (
    <Container>

      <SectionHeader
        title="Certifications"
        subtitle="Courses and credentials that back up your skills."
      />

      <Card
        title="Add certification"
        footer={
          <Button
            icon={<Plus size={16} />}
            loading={saving}
            onClick={add}
          >
            Add certification
          </Button>
        }
      >
        <div className="form-grid">
          <Field label="Title" required>
            <Input
              value={form.title}
              onChange={(e)=>
                setForm({...form,title:e.target.value})
              }
            />
          </Field>

          <Field label="Issuer" required>
            <Input
              value={form.issuer}
              onChange={(e)=>
                setForm({...form,issuer:e.target.value})
              }
            />
          </Field>

          <Field label="Issue date" required>
            <Input
              type="date"
              value={form.issue_date}
              onChange={(e)=>
                setForm({...form,issue_date:e.target.value})
              }
            />
          </Field>

          <Field label="Credential URL" hint="Optional link to verify it">
            <Input
              type="url"
              value={form.credential_url}
              onChange={(e)=>
                setForm({...form,credential_url:e.target.value})
              }
            />
          </Field>
        </div>
      </Card>

      <Card
        title="Your certifications"
        action={items.length > 0 ? <Chip>{items.length}</Chip> : undefined}
      >
        {items.length === 0 ? (
          <EmptyState
            icon={<Award size={20} />}
            title="No certifications yet"
            text="Add a course or credential above and it will appear on your resume."
          />
        ) : (
          <div className="item-grid">
            {items.map((item,index)=>(
              <article className="item" key={index}>
                <div className="item__top">
                  <div>
                    <h3 className="item__title">{item.title}</h3>
                    <p className="item__sub">{item.issuer}</p>
                  </div>

                  <DeleteButton onConfirm={()=>remove(index)} />
                </div>

                <div className="item__meta">
                  {item.issue_date && (
                    <span>
                      <Calendar size={14} />
                      {formatDate(item.issue_date)}
                    </span>
                  )}
                </div>

                {item.credential_url && (
                  <div className="item__links">
                    <a
                      href={item.credential_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      <ExternalLink size={14} />
                      View credential
                    </a>
                  </div>
                )}
              </article>
            ))}
          </div>
        )}
      </Card>

    </Container>
  );
}
