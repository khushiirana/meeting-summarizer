import axios from "axios";

const API_BASE = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
});

export const uploadMeeting = (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress,
  });
};

export const listMeetings = () => api.get("/meetings");

export const getMeeting = (id) => api.get(`/meetings/${id}`);

export const deleteMeeting = (id) => api.delete(`/meetings/${id}`);
