import { useEffect, useState } from "react";
import type { ChangeEvent } from "react";
import { Save } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

import { useToast } from "../../context/ToastContext";

import {
  getContact,
  saveContact,
} from "../../services/contact";

export default function ContactModule() {
  const toast = useToast();
  const [contact, setContact] = useState<any>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setContact(await getContact());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your contact details. Check that the backend is running.");
    }
  }

  async function save() {

    if (!contact.email?.trim()) {
      toast.error("Email is required.");
      return;
    }

    const emailRegex =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(contact.email)) {
      toast.error("Enter a valid email address.");
      return;
    }

    if (!contact.phone?.trim()) {
      toast.error("Phone number is required.");
      return;
    }

    const phone = contact.phone.replace(/\D/g, "");

    if (phone.length !== 10) {
      toast.error("Phone number must contain exactly 10 digits.");
      return;
    }

    if (
      contact.github &&
      !contact.github.startsWith("https://github.com/")
    ) {
      toast.error("GitHub URL must start with https://github.com/");
      return;
    }

    if (
      contact.linkedin &&
      !contact.linkedin.startsWith("https://www.linkedin.com/")
    ) {
      toast.error("LinkedIn URL must start with https://www.linkedin.com/");
      return;
    }

    if (
      contact.portfolio &&
      !/^https?:\/\/.+/.test(contact.portfolio)
    ) {
      toast.error("Portfolio must be a valid URL.");
      return;
    }

    setSaving(true);

    try {
      await saveContact(contact);
      toast.success("Contact details saved.");
    } catch (error) {
      console.error(error);
      toast.error("Could not save your contact details. Please try again.");
    } finally {
      setSaving(false);
    }

  }

  function set(field: string) {
    return (e: ChangeEvent<HTMLInputElement>) =>
      setContact({
        ...contact,
        [field]: e.target.value,
      });
  }

  return (
    <Container>
      <SectionHeader
        title="Contact"
        subtitle="Recruiters use these details to reach you. They appear in your resume header."
      />

      <Card
        footer={
          <Button
            icon={<Save size={16} />}
            loading={saving}
            onClick={save}
          >
            Save contact
          </Button>
        }
      >
        <div className="form-section">
          <h3 className="form-section__title">Reach you</h3>

          <div className="form-grid">
            <Field label="Email" required>
              <Input
                type="email"
                autoComplete="email"
                value={contact.email || ""}
                onChange={set("email")}
              />
            </Field>

            <Field label="Phone" required hint="10 digits">
              <Input
                type="tel"
                autoComplete="tel"
                value={contact.phone || ""}
                onChange={set("phone")}
              />
            </Field>
          </div>
        </div>

        <div className="form-section">
          <h3 className="form-section__title">Location</h3>

          <div className="form-grid">
            <Field label="City">
              <Input value={contact.city || ""} onChange={set("city")} />
            </Field>

            <Field label="State">
              <Input value={contact.state || ""} onChange={set("state")} />
            </Field>

            <Field label="Country">
              <Input value={contact.country || ""} onChange={set("country")} />
            </Field>
          </div>
        </div>

        <div className="form-section">
          <h3 className="form-section__title">Online profiles</h3>

          <div className="form-grid">
            <Field label="GitHub" hint="Starts with https://github.com/">
              <Input
                type="url"
                value={contact.github || ""}
                onChange={set("github")}
              />
            </Field>

            <Field label="LinkedIn" hint="Starts with https://www.linkedin.com/">
              <Input
                type="url"
                value={contact.linkedin || ""}
                onChange={set("linkedin")}
              />
            </Field>

            <Field label="Portfolio" wide>
              <Input
                type="url"
                value={contact.portfolio || ""}
                onChange={set("portfolio")}
              />
            </Field>
          </div>
        </div>
      </Card>
    </Container>
  );
}
