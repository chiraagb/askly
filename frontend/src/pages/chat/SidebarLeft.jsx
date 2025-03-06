import { useSelector } from "react-redux";
// import ToggleTheme from "../ToggleTheme";
import { MdOutlinePowerSettingsNew } from "react-icons/md";

import { Link, useNavigate } from "react-router-dom";
import { FaFlagUsa } from "react-icons/fa";
import SessionHistory from "./Sessionhistory.jsx";
import { useSession } from "../../context/summaryContext.jsx";
import ToggleTheme from "./ToggleTheme.jsx";

// import { useSession } from "../../context/summaryContext";

const SidebarLeft = () => {
  const isOpen = useSelector((state) => state.sidebar.isOpen);
  const navigate = useNavigate();
  const {
    generateSessionId,
    selectedSessionId,
    setSelectedSessionId,
    setHomeContent,
    initChatSession,
    setWs,
    fetchSessionChats,
    setSelectedFileUrl,
    setIsSessionLoading,
  } = useSession();

  const handleNewChatClick = async () => {
    try {
      navigate("/");
      setIsSessionLoading(false);
      setWs(null);
      setSelectedSessionId(sessionStorage.setItem("selectedSessionId", null));
      setSelectedFileUrl("");
    } catch (error) {
      console.error("Error in clicking new chat", error);
    }
  };

  return (
    <div
      className={`transform top-0 left-0 w-[15%] fixed overflow-auto ease-in-out transition-all duration-300 z-30 dark:bg-[#1D1D1D] text-white  ${
        isOpen ? "translate-x-0" : "-translate-x-full"
      }`}
    >
      <div className="flex flex-col justify-between p-0 bg-white dark:bg-[#171717] dark:text-[rgb(229,229,229)] w-[100%] h-screen">
        <div className="flex flex-col">
          <div className="p-4">
            <div className="flex items-center justify-between gap-3 w-[100%] bg-aila-left-div dark-bg-aila-left-div rounded-lg cursor-pointer ">
              <div className="flex items-center justify-center">
                <div
                  className="flex items-center justify-center w-[30px] h-[30px] bg-black dark:bg-[#4d4d4d] rounded-full text-white dark:text-white border-[1px] border-[#171717]"
                  onClick={() => {
                    setIsSessionLoading(false);
                    setSelectedSessionId(
                      sessionStorage.setItem("selectedSessionId", null)
                    );
                    navigate("/");
                  }}
                >
                  <p className="text-[18px] ">
                    <FaFlagUsa className="w-3 h-3" />
                  </p>
                </div>
                <div className="ml-2">
                  <h1 className="text-black dark:text-white font-semibold">
                    AI Plan Room
                  </h1>
                </div>
              </div>

              <div onClick={handleNewChatClick}>
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="icon-md dark:text-white text-black"
                >
                  <path
                    d="M16.7929 2.79289C18.0118 1.57394 19.9882 1.57394 21.2071 2.79289C22.4261 4.01184 22.4261 5.98815 21.2071 7.20711L12.7071 15.7071C12.5196 15.8946 12.2652 16 12 16H9C8.44772 16 8 15.5523 8 15V12C8 11.7348 8.10536 11.4804 8.29289 11.2929L16.7929 2.79289ZM19.7929 4.20711C19.355 3.7692 18.645 3.7692 18.2071 4.2071L10 12.4142V14H11.5858L19.7929 5.79289C20.2308 5.35499 20.2308 4.64501 19.7929 4.20711ZM6 5C5.44772 5 5 5.44771 5 6V18C5 18.5523 5.44772 19 6 19H18C18.5523 19 19 18.5523 19 18V14C19 13.4477 19.4477 13 20 13C20.5523 13 21 13.4477 21 14V18C21 19.6569 19.6569 21 18 21H6C4.34315 21 3 19.6569 3 18V6C3 4.34314 4.34315 3 6 3H10C10.5523 3 11 3.44771 11 4C11 4.55228 10.5523 5 10 5H6Z"
                    fill="currentColor"
                  ></path>
                </svg>
              </div>
            </div>
          </div>
          <SessionHistory />
        </div>
        <div className="flex flex-col w-[100%]  dark:border-t-white">
          <div className="p-4 border-t-[1px] border-t-[#1d1d1d] dark:border-t-white dark:border-opacity-25 border-opacity-20">
            <div className="border-left-div-bottom-section text-black dark:text-[#E5E5E5] text-[1em]">
              <Link className="flex items-center gap-2 p-2 mt-3 cursor-pointer">
                <img
                  src={localStorage.getItem("profile")}
                  alt="profile-picture"
                  className="h-5 w-5 rounded-full"
                />
                <div>
                  <p>
                    {localStorage.getItem("first_name")}{" "}
                    {localStorage.getItem("last_name")}
                  </p>
                </div>
              </Link>
              <div>
                <ToggleTheme />
              </div>

              <Link
                to={"/login"}
                className="flex items-center gap-2 p-2 mt-3 cursor-pointer text-[#FF5555] "
                onClick={() => {
                  localStorage.removeItem("token");
                  setSelectedSessionId(
                    sessionStorage.setItem("selectedSessionId", null)
                  );
                  // navigate("/login");
                }}
              >
                <div>
                  <MdOutlinePowerSettingsNew className="h-5 w-5" />
                </div>
                <div>
                  <p>Logout</p>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SidebarLeft;
