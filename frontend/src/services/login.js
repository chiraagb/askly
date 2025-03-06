import axios from "axios";

export const googleLogin = async (code, hostname) => {
  console.log(code, "code");

  let res = await axios.post(
    import.meta.env.VITE_BASE_URL + "/api/v1/accounts/google/auth/",
    {
      code: code,
    }
  );

  window.localStorage.setItem("token", res.data.key);
  const config = {
    headers: {
      Authorization: `Token ${window.localStorage.getItem("token")}`,
    },
  };
  let resp = await axios.get(
    import.meta.env.VITE_BASE_URL + "/api/v1/accounts/user-detail/",
    config
  );

  localStorage.setItem("first_name", resp.data.first_name);
  localStorage.setItem("last_name", resp.data.last_name);
  localStorage.setItem("profile", resp.data.profile_pic);

  return resp;
};
