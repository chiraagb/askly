import { googleLogin } from "../../services/login.js";
import { FcGoogle } from "react-icons/fc";
import { Link } from "react-router-dom";

function GoogleSignInButton(props) {
  const hostname = window.location.hostname;

  const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  /*global google*/
  let client;
  if (typeof google != "undefined") {
    client = google.accounts.oauth2.initCodeClient({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      scope:
        "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
      callback: async (response) => {
        console.log(response, "response");
        await googleLogin(response.code, hostname).then((res) => {
          props.setVerified(true);
        });
      },
    });
  } else {
    async function wait_for_1_sec() {
      await delay(1000);
      client = google.accounts.oauth2.initCodeClient({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        scope:
          "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",

        callback: async (response) => {
          console.log(response, "response");

          await googleLogin(response.code, hostname).then((res) => {
            props.setVerified(true);
          });
        },
      });
    }
    wait_for_1_sec();
  }

  return (
    <button
      id="google-login-btn"
      onClick={() => client.requestCode()}
      className="flex items-center gap-[1vw]"
    >
      <div>
        <FcGoogle className="h-[1.5vw] w-[1.5vw]" />
      </div>
      <div>
        <h1 className="font-poppins font-semibold text-[1.2vw] text-black leading-[2vw]">
          Login with Google
        </h1>
      </div>
    </button>
  );
}
export default GoogleSignInButton;
