import axios from "axios";

const API = "http://127.0.0.1:8000/skills";

export const getSkills = async () =>
  (await axios.get(API)).data;

export const saveSkills = async (data: any) =>
  (await axios.put(API, data)).data;