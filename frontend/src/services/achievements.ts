import axios from "axios";

const API = "/achievements";

export const getAchievements = async () =>
  (await axios.get(API)).data;

export const addAchievement = async (data: any) =>
  (await axios.post(API, data)).data;

export const deleteAchievement = async (index: number) =>
  (await axios.delete(`${API}/${index}`)).data;