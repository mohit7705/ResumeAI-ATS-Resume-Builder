import axios from "axios";

const API = "http://127.0.0.1:8000";

export const generateResume = async (job_description: string) => {
  const res = await axios.post(`${API}/generate`, {
    job_description,
  });

  return res.data;
};