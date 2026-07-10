import axios from "axios";

const API = "http://127.0.0.1:8000/achievements";

export const getAchievements = async () =>
  (await axios.get(API)).data;

export const addAchievement = async (data: any) =>
  (await axios.post(API, data)).data;

export const deleteAchievement = async (index: number) =>
  (await axios.delete(`${API}/${index}`)).data;