import axios from "axios";

const API = "/skills";

export const getSkills = async () =>
  (await axios.get(API)).data;

export const saveSkills = async (data: any) =>
  (await axios.put(API, data)).data;