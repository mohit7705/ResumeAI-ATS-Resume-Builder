import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getProfile = async () => {
    return (await axios.get(API + "/personal")).data;
};

export const saveProfile = async (data:any) => {
    return (await axios.put(API + "/personal", data)).data;
};

export const getSummary = async () => {
    return (await axios.get(API + "/summary")).data;
};

export const saveSummary = async (data:any) => {
    return (await axios.put(API + "/summary", data)).data;
};