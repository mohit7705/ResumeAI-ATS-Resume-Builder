import axios from "axios";

const API = "http://127.0.0.1:8000/certifications";

export const getCertifications = async () =>
  (await axios.get(API)).data;

export const addCertification = async (data: any) =>
  (await axios.post(API, data)).data;

export const deleteCertification = async (index: number) =>
  (await axios.delete(`${API}/${index}`)).data;