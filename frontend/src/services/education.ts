import axios from "axios";

const API = "http://127.0.0.1:8000/education";

export const getEducation = async () =>
  (await axios.get(API)).data;

export const addEducation = async (data: any) =>
  (await axios.post(API, data)).data;

export const updateEducation = async (
  index: number,
  data: any
) =>
  (await axios.put(`${API}/${index}`, data)).data;

export const deleteEducation = async (
  index: number
) =>
  (await axios.delete(`${API}/${index}`)).data;