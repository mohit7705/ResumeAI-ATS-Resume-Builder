import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

import {
  getContact,
  saveContact,
} from "../../services/contact";

export default function ContactModule() {
  const [contact, setContact] = useState<any>({});

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setContact(await getContact());
  }

  async function save() {

    if (!contact.email?.trim()) {
      alert("Email is required.");
      return;
    }

    const emailRegex =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(contact.email)) {
      alert("Enter a valid email address.");
      return;
    }

    if (!contact.phone?.trim()) {
      alert("Phone number is required.");
      return;
    }

    const phone = contact.phone.replace(/\D/g, "");

    if (phone.length !== 10) {
      alert("Phone number must contain exactly 10 digits.");
      return;
    }

    if (
      contact.github &&
      !contact.github.startsWith("https://github.com/")
    ) {
      alert("GitHub URL must start with https://github.com/");
      return;
    }

    if (
      contact.linkedin &&
      !contact.linkedin.startsWith("https://www.linkedin.com/")
    ) {
      alert("LinkedIn URL must start with https://www.linkedin.com/");
      return;
    }

    if (
      contact.portfolio &&
      !/^https?:\/\/.+/.test(contact.portfolio)
    ) {
      alert("Portfolio must be a valid URL.");
      return;
    }

    await saveContact(contact);

    alert("Contact Saved Successfully.");

  }

  return (
    <Container>
      <SectionHeader
        title="Contact"
        subtitle="Contact Information"
      />

      <Card title="Contact Details">

        <Label>Email</Label>
        <Input
          value={contact.email || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              email: e.target.value,
            })
          }
        />

        <Label>Phone</Label>
        <Input
          value={contact.phone || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              phone: e.target.value,
            })
          }
        />

        <Label>City</Label>
        <Input
          value={contact.city || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              city: e.target.value,
            })
          }
        />

        <Label>State</Label>
        <Input
          value={contact.state || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              state: e.target.value,
            })
          }
        />

        <Label>Country</Label>
        <Input
          value={contact.country || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              country: e.target.value,
            })
          }
        />

        <Label>GitHub</Label>
        <Input
          value={contact.github || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              github: e.target.value,
            })
          }
        />

        <Label>LinkedIn</Label>
        <Input
          value={contact.linkedin || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              linkedin: e.target.value,
            })
          }
        />

        <Label>Portfolio</Label>
        <Input
          value={contact.portfolio || ""}
          onChange={(e) =>
            setContact({
              ...contact,
              portfolio: e.target.value,
            })
          }
        />

        <Button onClick={save}>
          Save Contact
        </Button>

      </Card>
    </Container>
  );
}