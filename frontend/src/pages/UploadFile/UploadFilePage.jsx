import { useState } from "react";
import StatusModal from "./StatusModal";
import { useLocation, useNavigate } from "react-router";
import axios from "axios";
import { toast } from "react-toastify";
import SidebarLeft from "../chat/SidebarLeft";
import { useSelector } from "react-redux";
import ToggleButton from "../chat/ToggleButton";
import { useSession } from "../../context/summaryContext";
import SessionLoader from "../../components/SessionLoader";

const UploadFilePage = () => {
  // Modelsection
  const [showModal, setShowModal] = useState(false);
  const isOpen = useSelector((state) => state.sidebar.isOpen);
  const {
    setSelectedSessionId,
    setSessionId,
    initChatSession,
    setWs,
    fetchSessionChats,
    isSessionLoading,
  } = useSession();

  const openModal = () => {
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
  };
  var intervalId;
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [status, setStatus] = useState("");

  const location = useLocation();

  const handleFile = (e) => {
    return new Promise((resolve, reject) => {
      const selectedFile = e.target.files[0];
      const fileType = ["application/pdf"];

      if (!selectedFile) {
        reject(new Error("No file selected"));
        toast.warn("No file selected", {
          autoClose: 2000,
        });
        return;
      }

      console.log(selectedFile.size, "File size catched");

      if (selectedFile.size > 10485760) {
        console.log("inside if");
        // toast.error("File size should not exceed 10MB", {
        //   autoClose: 2000,
        // });
        setLoading(false);
        reject(new Error("File size should not exceed 10MB"));
        return;
      }

      if (fileType.includes(selectedFile.type)) {
        let reader = new FileReader();
        reader.readAsDataURL(selectedFile);
        reader.onload = (e) => {
          const result = e.target.result;
          resolve(result);
        };
        reader.onerror = (error) => {
          reject(error);
        };
      } else {
        setLoading(false);
        toast.warn("Invalid file type. Please upload a PDF.", {
          autoClose: 2000,
        });
        // reject(new Error("Invalid file type"));
      }
    });
  };

  const handleResponse = async (res) => {
    console.log(res);
    switch (res.data.status) {
      case "STARTING":
        localStorage.setItem("pdfKey", res.data.pdf_key);
        return setStatus("Uploading Pdf ..");
      case "LOADING":
        return setStatus("Loading Pdf ...");
      // case "ANALYZING":
      //   return setStatus("Analysing Pdf ...");
      // case "SUMMARIZING":
      //   return setStatus("Summarizing Pdf ...");
      // case "ANALYZING":
      //   return setStatus("Analysing Pdf ...");
      // case "SUMMARIZING":
      //   return setStatus("Summarizing Pdf ...");
      case "FAILED":
        return setStatus("Failed due to some issues, please try again!");
      case "SUCCESS": {
        console.log(res, "resss");
        setSelectedSessionId(res.data.msg.session_id);
        sessionStorage.setItem("selectedSessionId", res.data.msg.session_id);
        setSessionId(res.data.msg.session_id);
        const wsInstance = await initChatSession(res.data.msg.session_id);
        setWs(wsInstance);
        await fetchSessionChats(res.data.msg.session_id);
        clearInterval(intervalId);
        const pdf_file = localStorage.setItem("pdf", res.data.msg.file);
        return navigate(`/c/${res.data.msg.session_id}`, {
          state: { file: pdf_file },
        });
      }
      default:
        throw new Error(`Unknown status from server ${res.data.status}`);
    }
  };

  const getPdfStatus = async () => {
    const pdfKey = localStorage.getItem("pdfKey");
    // console.log("here");
    try {
      await axios
        .get(
          import.meta.env.VITE_BASE_URL +
            `/api/v1/chat/pdf-upload-status/${pdfKey}/`,

          {
            headers: {
              Authorization: "Token " + localStorage.getItem("token"),
            },
          }
        )
        .then((res) => handleResponse(res));
    } catch (err) {
      setLoading(false);
      console.log("err", err);
    }
  };

  // const upload = async (e) => {
  //   const formData = new FormData();
  //   formData.append("file", e.target.files[0]);
  //   let file = null;
  //   handleFile(e)
  //     .then((res) => {
  //       file = res;
  //     })
  //     .catch((err) => {
  //       toast.error(err.message, {
  //         autoClose: 3000,
  //       });
  //       return;
  //     });

  //   try {
  //     setLoading(true);
  //     const res = await axios.post(
  //       import.meta.env.VITE_BASE_URL + "/api/v1/chat/pdf-upload/",
  //       formData,
  //       {
  //         headers: {
  //           "Content-Type": "multipart/form-data",
  //           Authorization: "Token " + localStorage.getItem("token"),
  //         },
  //       }
  //     );
  //     console.log(res);
  //     handleResponse(res);
  //     intervalId = setInterval(() => getPdfStatus(), 1000);
  //   } catch (err) {
  //     console.log("Error in try-catch", err);
  //     setLoading(false);
  //     alert("File size should be less than 10mb");
  //     toast.error("File size should be less than 10mb", {
  //       autoClose: 3000,
  //     });
  //   }
  // };

  const upload = async (e) => {
    setLoading(true);
    handleFile(e)
      .then((res) => {
        const formData = new FormData();
        formData.append("file", e.target.files[0]);
        return axios.post(
          import.meta.env.VITE_BASE_URL + "/api/v1/chat/pdf-upload/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: "Token " + localStorage.getItem("token"),
            },
          }
        );
      })
      .then((res) => {
        console.log(res);
        handleResponse(res);
        intervalId = setInterval(() => getPdfStatus(), 1000);
      })
      .catch((err) => {
        console.error("Error in upload:", err);
        toast.error(err.message, {
          autoClose: 3000,
        });
        setLoading(false);
        document.getElementById("dropzone-file").value = "";
      });
  };

  return (
    // <>
    //   <div className="w-full h-screen dark:bg-[#1c1e1f] font-poppins">
    //     <SidebarLeft />
    //     <div
    //       className={`flex-1 transition-margin duration-300 ${
    //         isOpen ? "ml-[15%]" : "ml-0"
    //       }`}
    //     >
    //       <div className="flex  h-screen">
    //         <ToggleButton />
    //         <div className="flex items-center justify-center w-full h-full">
    //           <div className="flex flex-col dark:bg-[#181a1b] w-[80%] h-[80%] rounded-xl">
    //             <div className="flex justify-between dark:text-[#DAD7D2] p-10">
    //               <h1 className="font-semibold text-[35px] leading-[48px] w-[250px]">
    //                 Upload your document
    //               </h1>
    //               <p className="font-medium text-[16px] leading-[30px] w-[350px]">
    //                 You&apos;ll be able to start a conversation based on the
    //                 document uploaded
    //               </p>
    //             </div>
    //             <div className="border-t-[1px] border-t-[#dad7d2] border-opacity-[20%] p-3 ">
    //               <div className="h-[200px] w-[1030px]"></div>
    //             </div>
    //           </div>
    //         </div>
    //       </div>
    //     </div>
    //   </div>
    // </>
    <>
      {isSessionLoading ? (
        <SessionLoader />
      ) : (
        <div className="dark:bg-[#1d1d1d] bg-[#FFF] h-screen w-full text-black dark:text-[#dad7d2]">
          {/* After Login & Signup UploadFilePage Front Page */}
          <div className="w-10/12 m-auto mt-[30px] pt-16">
            <div className="flex justify-center">
              {/* <img src={DocuSensaLogo} alt="logo" className="h-12 md:h-24 " /> */}
            </div>
            <div className="flex md:flex-row flex-col items-center justify-between mb-4">
              <h1 className=" text-[40px] font-bold  w-full ">
                Upload your document
              </h1>
              <p className=" md:w-2/5 w-full ">
                You can initiate a conversation based on the document you've
                uploaded.
              </p>
            </div>

            <div className="border dark:border-white"></div>
            {/* <div>
          <button className="text-white mt-4 border-2 border-white rounded-xl p-2">
            Upload Document
          </button>
        </div> */}

            <div className="mt-4 flex items-center justify-center">
              <div className="flex items-center justify-center w-[40%] h-[500px]">
                <label
                  for="dropzone-file"
                  className="flex flex-col items-center justify-center w-full h-80 border-2 border-dashed rounded-lg cursor-pointer bg-gray-800  border-white  bg-clip-bg bg-gradient-to-r from-purple-700 to-red-400 hover:from-red-400 hover:to-purple-700"
                >
                  <div className="flex flex-col items-center justify-center pt-5 pb-6 ">
                    <svg
                      className="w-8 h-8 mb-4 text-white"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 20 16"
                    >
                      <path
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                      />
                    </svg>
                    <p className="mb-2 text-2xl text-white">
                      <span className="font-semibold">Click to upload</span>
                    </p>
                    <p className="text-xs text-white">Supported Pdf</p>
                  </div>
                  <input
                    onChange={upload}
                    onClick={openModal}
                    id="dropzone-file"
                    type="file"
                    className="hidden"
                  />
                </label>
              </div>
            </div>

            {loading && (
              <StatusModal
                closeModal={closeModal}
                status={status}
                loading={loading}
              />
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default UploadFilePage;
