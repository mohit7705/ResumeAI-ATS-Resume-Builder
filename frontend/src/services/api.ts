import axios from "axios";

const API = "";

export type ResumeLevel = "Fresher" | "Junior";
export type Provider = "gemini" | "meta";

export type ProviderInfo = { available: boolean; model: string };

export type ProviderStatus = {
  default: Provider;
  gemini: ProviderInfo;
  meta: ProviderInfo;
};

export const getProviders = async (): Promise<ProviderStatus> => {
  const res = await axios.get(`${API}/ai/providers`);
  return res.data;
};

export const generateResume = async (
  job_description: string,
  highlight: boolean = true,
  provider?: Provider
) => {
  const res = await axios.post(`${API}/generate`, {
    job_description,
    highlight,
    provider,
  });

  return res.data;
};

export const generateResumeFromTitle = async (
  title: string,
  level: ResumeLevel = "Fresher",
  highlight: boolean = true,
  provider?: Provider
) => {
  const res = await axios.post(`${API}/generate/title`, {
    title,
    level,
    highlight,
    provider,
  });

  return res.data;
};
