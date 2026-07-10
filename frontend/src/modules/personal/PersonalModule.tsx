import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

import {
  getProfile,
  saveProfile,
} from "../../services/personal";

export default function ProfileModule() {
  const [profile, setProfile] = useState<any>({});

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setProfile(await getProfile());
  }

  async function save() {

  if (!profile.first_name?.trim()) {
    alert("First Name is required.");
    return;
  }

  if (!profile.last_name?.trim()) {
    alert("Last Name is required.");
    return;
  }

  if (!profile.professional_title?.trim()) {
    alert("Professional Title is required.");
    return;
  }

  await saveProfile(profile);

  alert("Profile Saved Successfully.");

}

  return (
    <Container>
      <SectionHeader
        title="Profile"
        subtitle="Professional Information"
      />

      <Card title="Basic Information">
        <Label>First Name</Label>

        <Input
          value={profile.first_name || ""}
          onChange={(e) =>
            setProfile({
              ...profile,
              first_name: e.target.value,
            })
          }
        />

        <Label>Last Name</Label>

        <Input
          value={profile.last_name || ""}
          onChange={(e) =>
            setProfile({
              ...profile,
              last_name: e.target.value,
            })
          }
        />

        <Label>Professional Title</Label>

        <Input
          value={profile.professional_title || ""}
          onChange={(e) =>
            setProfile({
              ...profile,
              professional_title: e.target.value,
            })
          }
        />

        <br />

        <Button onClick={save}>
          Save Profile
        </Button>
      </Card>
    </Container>
  );
}