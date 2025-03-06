import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
// import { MdAccountCircle } from "react-icons/md";
// import { v4 as uuid } from "uuid";
// import GoogleLoginButton from "../../components/GoogleSignInButton";
// import DocuSensaLogo from "../../Images/DocuSensaLogo.png";

const Navbar = () => {
  const navigate = useNavigate();
  const [verified, setVerified] = useState(false);
  const [open, setOpen] = useState(false);
  const closeNavbar = () => {
    setOpen(false);
  };

  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const loginMessage = () => {
    toast.success("Login successfully!", {
      autoClose: 2000,
    });
  };

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      setVerified(true);
    }
  }, []);
  return (
    <div className="antialiased bg-gray-900 p-1">
      <div className="w-full text-white">
        {/* <div className="flex flex-col max-w-screen-xl px-4 mx-auto md:items-center md:justify-between md:flex-row md:px-6 lg:px-8"> */}
        <div className="flex flex-row items-center justify-between  px-8 ">
          <div>
            <Link to="/">
              <img
                // src={DocuSensaLogo}
                alt="logo"
                className="h-12 md:h-20 mr-3 rounded-full"
              />
            </Link>
          </div>

          {/* <div className="absolute text-white right-0  mx-10 my-5">
            {verified ? (
              <div>
                <MdAccountCircle
                  className="cursor-pointer"
                  size={45}
                  onClick={toggleDropdown}
                />
                {isOpen && (
                  <div className="origin-top-right absolute right-0 mt-2 w-auto rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                    <button
                      className="w-[120px] block px-4 py-2 font-bold  text-sm text-gray-700 hover:bg-gray-300 rounded-md"
                      onClick={() => {
                        localStorage.clear();
                        setVerified(false);
                      }}
                    >
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <GoogleLoginButton
                setVerified={setVerified}
                loginMessage={loginMessage}
              />
            )}
          </div> */}

          {/* user buttons */}
          <div className="flex gap-4 ">
            <Link to="/">
              <button className="text-white text-lg hover:border-b-white  px-2 py-2 text-center rounded-lg font-bold hidden md:block">
                Features
              </button>
            </Link>
            <Link to="/blog">
              <button className="text-white text-lg hover:border-b-white  px-2 py-2 text-center rounded-lg font-bold hidden md:block">
                Blog
              </button>
            </Link>
            <Link to="/pricing">
              <button className="text-white text-lg hover:border-b-white  px-4 py-2 text-center rounded-lg font-bold hidden md:block">
                Pricing
              </button>
            </Link>
            <Link to="/uploadFile">
              <button className="text-white bg-gradient-to-r  from-purple-500 via-purple-600 to-purple-700 hover:bg-gradient-to-br  focus:outline-none focus:ring-purple-300  text-sm px-5 py-2.5 text-center mr-2 mb-2 rounded-lg font-semibold hidden md:block">
                Get Started for free
              </button>
            </Link>
            <div className="relative inline-block text-left">
              <button
                onClick={toggleDropdown}
                id="dropdownUserAvatarButton"
                data-dropdown-toggle="dropdownAvatar"
                className="flex mx-3 text-sm bg-gray-800 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
                type="button"
              >
                <img
                  className="w-10 h-10 rounded-full"
                  src="https://as1.ftcdn.net/v2/jpg/02/09/95/42/1000_F_209954204_mHCvAQBIXP7C2zRl5Fbs6MEWOEkaX3cA.jpg"
                  alt="UserImage"
                />
              </button>
              {isOpen && (
                <div>
                  {verified ? (
                    // Render this when user is logged in
                    <div className="origin-top-right absolute right-0 mt-2 w-auto rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                      <div
                        className="py-1"
                        role="menu"
                        aria-orientation="vertical"
                        aria-labelledby="dropdownAvatarButton"
                      >
                        <a
                          href="/setting"
                          className="block w-[100px] font-semibold px-4 py-2 text-md text-gray-700 hover:bg-gray-300 rounded-md"
                          role="menuitem"
                          tabIndex="-1"
                          id="dropdownAvatarItem1"
                        >
                          Account
                        </a>
                      </div>
                      <div className="border-t border-gray-500" />
                      <div
                        className="py-1"
                        role="menu"
                        aria-orientation="vertical"
                        aria-labelledby="dropdownAvatarButton"
                      >
                        <button
                          className="block w-full font-semibold px-4 py-2 text-md text-gray-700 hover:bg-gray-300 rounded-md"
                          role="menuitem"
                          tabIndex="-4"
                          id="dropdownAvatarItem4"
                          onClick={() => {
                            localStorage.clear();
                            setVerified(false);
                            toast.success("User logged out Successfully", {
                              autoClose: 2000,
                            });
                            navigate("/");
                          }}
                        >
                          Sign out
                        </button>
                      </div>
                    </div>
                  ) : (
                    // Render this when user is not logged in
                    <div className="origin-top-right absolute right-0 mt-2 w-auto rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                      <a
                        href="/signin"
                        className="block font-semibold px-4 py-2 text-md text-gray-700 hover:bg-gray-300 rounded-md"
                        role="menuitem"
                        tabIndex="-1"
                        id="dropdownAvatarItem1"
                      >
                        Login
                      </a>
                      <a
                        href="/signup"
                        className="block font-semibold px-4 py-2 text-md text-gray-700 hover:bg-gray-300 rounded-md"
                        role="menuitem"
                        tabIndex="-2"
                        id="dropdownAvatarItem2"
                      >
                        Signup
                      </a>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
          {/* 
          <button
              className="rounded-lg md:hidden focus:outline-none focus:shadow-outline"
              onClick={() => setOpen(!open)}
            >
              <svg fill="currentColor" viewBox="0 0 20 20" className="w-6 h-6">
                {open ? (
                  <path
                    fill="black"
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  ></path>
                ) : (
                  <path
                    fill="black"
                    fillRule="evenodd"
                    d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z"
                    clipRule="evenodd"
                  ></path>
                )}
              </svg>
            </button> */}
        </div>
        {/* <nav
            className={`flex-col flex-grow ${
              open ? "flex" : "hidden"
            } pb-4 md:pb-0 md:flex md:justify-end md:flex-row bg-white`}
          >
            <div className="flex flex-col md:flex-row justify-center gap-3 item-center  md:ml-[6rem]">
              <button className=" text-[30px] md:text-[20px] font-bold text-black md:text-white">
                Login
              </button>
              <button className=" text-[30px] md:text-[20px] font-bold text-black md:text-white">
                Singup
              </button>
            </div>
          </nav> */}
      </div>
    </div>
    // </div>
  );
};

export default Navbar;
