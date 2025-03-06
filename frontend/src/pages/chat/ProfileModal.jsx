import React, { useEffect, useState } from "react";
import { BiUserCircle } from "react-icons/bi";
import { CgProfile } from "react-icons/cg";
import { MdOutlineArrowForwardIos } from "react-icons/md";
import { Link } from "react-router-dom";
import axios from "axios";

const ProfileModal = () => {
  const [isModalVisible, setModalVisible] = useState(false);
  const [userData, setUserData] = useState(null);

  const toggleModal = () => {
    setModalVisible(!isModalVisible);
  };

  const fetchData = async () => {
    try {
      const response = await axios.get(
        process.env.REACT_APP_BASE_URL + "/api/v1/accounts/user-email/",
        {
          headers: {
            Authorization: "Token " + localStorage.getItem("token"),
          },
        }
      );
      setUserData(response.data);
      // console.log(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    if (isModalVisible) {
      fetchData();
    }
  }, [isModalVisible]);

  return (
    <div>
      <button onClick={toggleModal}>
        {" "}
        <CgProfile />
      </button>

      {isModalVisible && (
        <div className="fixed inset-0 flex items-center justify-center z-50 overflow-auto bg-black bg-opacity-70">
          <div className="relative max-w-screen-md  p-8 md:p-12  rounded-lg shadow bg-gray-800">
            <div className="flex items-start justify-between p-4 border-b rounded-t dark:border-white">
              <h3 className="text-xl font-semibold  text-white">Profile</h3>
              <button
                type="button"
                onClick={toggleModal}
                className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ml-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
              >
                <svg
                  className="w-3 h-3"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 14 14"
                >
                  <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                  />
                </svg>
                <span className="sr-only">Close modal</span>
              </button>
            </div>
            <div className=" w-[350px] md:w-[500px] p-2 md:p-6  space-y-2 md:space-y-6 text-white">
              {userData && (
                <>
                  <div className="flex flex-row gap-10 items-center ">
                    <div className="text-[30px]">
                      <BiUserCircle />
                    </div>
                    <div className="flex flex-col text-left">
                      <label className="text-xl md:text-2xl">
                        Email Address
                      </label>
                      <h3 className="text-md md:text-xl">
                        {userData.user_email}
                      </h3>
                    </div>
                  </div>
                  <div>
                    <div className="flex flex-row justify-between items-center mt-10">
                      <div className="flex flex-col  items-start">
                        <h1 className="text-xl font-bold">Plan</h1>
                        <h5>{userData.plan}</h5>
                      </div>
                      <div>
                        <Link to="/setting">
                          <button className="p-2 border-4 text-xl font-semibold hover:border-purple-700 hover:text-purple-700 hover:bg-white hover:font-bold border-white rounded-lg">
                            Manage
                          </button>
                        </Link>
                      </div>
                    </div>
                    {/* 
                <div className="flex flex-row justify-between items-center mt-10">
                  <div>
                    <h1 className="text-xl font-bold">Delete Subscription</h1>
                  </div>
                  <div>
                    <button className="">
                      <MdOutlineArrowForwardIos />
                    </button>
                  </div>
                </div> */}
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileModal;
