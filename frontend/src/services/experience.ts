import axios from "axios";

const API = "/experience";

export const getExperience = async () =>
  (await axios.get(API)).data;

export const addExperience = async (data: any) =>
  (await axios.post(API, data)).data;

export const updateExperience = async (
  index: number,
  data: any
) =>
  (await axios.put(`${API}/${index}`, data)).data;

export const deleteExperience = async (
  index: number
) =>
  (await axios.delete(`${API}/${index}`)).data;