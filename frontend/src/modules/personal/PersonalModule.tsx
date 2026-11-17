import { useEffect, useState } from "react";
import { Save } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

import { useToast } from "../../context/ToastContext";
import { initials } from "../../utils/format";

import {
  getProfile,
  saveProfile,
} from "../../services/personal";

export default function ProfileModule() {
  const toast = useToast();
  const [profile, setProfile] = useState<any>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setProfile(await getProfile());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your profile. Check that the backend is running.");
    }
  }

  async function save() {

    if (!profile.first_name?.trim()) {
      toast.error("First name is required.");
      return;
    }

    if (!profile.last_name?.trim()) {
      toast.error("Last name is required.");
      return;
    }

    if (!profile.professional_title?.trim()) {
      toast.error("Professional title is required.");
      return;
    }

    setSaving(true);

    try {
      await saveProfile(profile);
      toast.success("Profile saved.");
    } catch (error) {
      console.error(error);
      toast.error("Could not save your profile. Please try again.");
    } finally {
      setSaving(false);
    }

  }

  const fullName = [profile.first_name, profile.last_name]
    .filter(Boolean)
    .join(" ");

  return (
    <Container>
      <SectionHeader
        title="Profile"
        subtitle="Your name and professional title appear at the very top of your resume."
      />

      <div className="split">
        <Card
          title="Basic information"
          footer={
            <Button
              icon={<Save size={16} />}
              loading={saving}
              onClick={save}
            >
              Save profile
            </Button>
          }
        >
          <div className="form-grid">
            <Field label="First name" required>
              <Input
                autoComplete="given-name"
                value={profile.first_name || ""}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    first_name: e.target.value,
                  })
                }
              />
            </Field>

            <Field label="Last name" required>
              <Input
                autoComplete="family-name"
                value={profile.last_name || ""}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    last_name: e.target.value,
                  })
                }
              />
            </Field>

            <Field
              label="Professional title"
              required
              wide
              hint="For example: AI & Machine Learning Student | Python Developer"
            >
              <Input
                value={profile.professional_title || ""}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    professional_title: e.target.value,
                  })
                }
              />
            </Field>
          </div>
        </Card>

        <aside className="split__aside">
          <Card title="How it looks">
            <div className="user-chip" style={{ gap: 16 }}>
              <span
                className="avatar"
                style={{ width: 56, height: 56, fontSize: 18 }}
              >
                {initials(profile.first_name, profile.last_name)}
              </span>

              <div>
                <div
                  style={{
                    fontFamily: "var(--font-display)",
                    fontSize: 26,
                    lineHeight: 1.1,
                  }}
                >
                  {fullName || "Your name"}
                </div>

                <div className="muted" style={{ marginTop: 4 }}>
                  {profile.professional_title || "Your professional title"}
                </div>
              </div>
            </div>
          </Card>
        </aside>
      </div>
    </Container>
  );
}
