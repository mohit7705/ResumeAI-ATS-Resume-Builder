import axios from "axios";

const API = "http://127.0.0.1:8000/projects";

export const getProjects = async () =>
  (await axios.get(API)).data;

export const addProject = async (data: any) =>
  (await axios.post(API, data)).data;

export const updateProject = async (
  index: number,
  data: any
) =>
  (await axios.put(`${API}/${index}`, data)).data;

export const deleteProject = async (
  index: number
) =>
  (await axios.delete(`${API}/${index}`)).data;