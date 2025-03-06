import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import GoogleSignInButton from "./GoogleSigninButton";
// import menu_icon from "../assets/sign-in-menu-icon.svg";
// import signin_vector from "../assets/sign-in-vector.svg";
// import profile_demo from "../assets/profile-demo.svg";
// import aila_demo from "../assets/aila_demo.svg";
// import copy from "../assets/copy.svg";
// import save from "../assets/save.svg";
import demo_signup from "../../assets/demo-bg-bidamerica.png";

import "./signup.css";
import { MdFileDownload } from "react-icons/md";
import { FaFlagUsa } from "react-icons/fa";
const Signin = () => {
  const navigate = useNavigate();
  const [verified, setVerified] = useState(false);
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setVerified(true);
      navigate("/");
    }
  }, [verified]);

  return (
    <>
      <div className="absolute lg:w-[45vw] lg:h-[45vw] lg:top-[3%] lg:left-[10%] circle-1"></div>
      <div className="absolute lg:top-[-30%] lg:left-[-30%] lg:w-[90vw] lg:h-[40vw] ellipse-signin"></div>
      <div className="absolute circle-2 lg:w-[35vw] lg:h-[35vw] bottom-[0%] left-[-3%]"></div>
      <div className="bg-[#393939] shadow-sign-up flex flex-col w-full h-screen font-lato ">
        <div className="absolute rectangle w-full h-[40%] bottom-0"></div>
        <div className="flex items-center justify-between absolute w-full">
          <div className=" ml-[5%] mt-[2%]">
            <div className="flex items-center justify-center w-[3vw] h-[3vw] bg-[#4D2C97] rounded-full text-white dark:text-white cursor-pointer">
              <FaFlagUsa />
            </div>
          </div>
          <div className="mr-[5%] mt-[2%] cursor-pointer">
            {/* <img src={menu_icon} alt="Menu Icon" className="w-[3vw]" /> */}
          </div>
        </div>

        <div className="absolute  lg:top-[10%] lg:left-[10%]">
          <img src={demo_signup} className="w-[40vw]" />
        </div>

        {/* Logo and Menu  */}
        <div className="absolute lg:top-[30%] right-[0%] text-[#E5E5E5] flex flex-col items-center gap-[4vw] font-semibold">
          <div className="flex gap-[2vw] w-[45vw]">
            <div className="lg:text-[3vw]">Welcome to</div>
            <div className="relative flex items-center bg-aila w-[20vw] pl-[0.7vw] border-l-[0.5vw] border-l-[#3F6CA1]">
              <p className="absolute text-[2vw] top-[-28%] left-[-6%]">
                <FaFlagUsa />
              </p>
              <div className="lg:text-[3vw]">AI Plan Room</div>
            </div>
          </div>
          {/* Google Button  */}
          <div className="flex items-center justify-center gap-4 w-[30vw] h-[3.5vw] bg-[#F6FBE9] p-3 rounded-[1vw] cursor-pointer border-[1px] border-[#CCCCF5]">
            <GoogleSignInButton setVerified={setVerified} />
          </div>
        </div>
      </div>
    </>
  );
};

export default Signin;
