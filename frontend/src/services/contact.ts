import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getContact = async () => {
  return (await axios.get(API + "/contact")).data;
};

export const saveContact = async (data: any) => {
  return (await axios.put(API + "/contact", data)).data;
};