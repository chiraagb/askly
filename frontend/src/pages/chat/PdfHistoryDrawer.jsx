import axios from "axios";
import { useEffect, useState } from "react";
import { BiConversation } from "react-icons/bi";
import { MdPictureAsPdf } from "react-icons/md";
import { Link, useNavigate } from "react-router-dom";

const PdfHistoryDrawer = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [pdfData, setPdfData] = useState([]);
  const navigate = useNavigate();
  // console.log("pdfData", pdfData);
  // console.log("token", localStorage.getItem("token"));
  const openDrawer = () => {
    setIsOpen(true);
  };

  const closeDrawer = () => {
    setIsOpen(false);
  };

  const getData = async () => {
    try {
      const response = await axios.get(
        process.env.REACT_APP_BASE_URL + "/api/v1/readpdf/pdfs/",
        {
          headers: {
            Authorization: "Token " + localStorage.getItem("token"),
          },
        }
      );
      // console.log("response", response);
      setPdfData(response.data.reverse());

      // console.log("pdfdata1", response.data);
    } catch (error) {
      // Handle errors here
      console.error(error);
    }
  };
  const handleName = (e, file, id) => {
    localStorage.setItem("pdfKey", e);
    const res = {
      summary: "summary",
      examples: [
        { question: "Summarize this Document." },
        { question: "What is the main message in the document?" },
      ],
    };
    navigate(`/chat/${id}`, {
      state: {
        file: file,
        summary: res.summary,
        questions: res.examples,
      },
    });
  };

  useEffect(() => {
    getData();
  }, []);

  return (
    <div>
      {/* Show drawer button */}
      <div className="text-center">
        <button type="button" onClick={openDrawer}>
          <BiConversation />
        </button>
      </div>

      {/* Drawer component */}
      {isOpen && (
        <div
          id="drawer-example"
          className="fixed top-0 left-0 z-40 h-full md:h-screen p-4 overflow-y-auto bg-gray-800 "
          tabIndex="-1"
          aria-labelledby="drawer-label"
        >
          <h5
            id="drawer-label"
            className="inline-flex items-center mb-4 text-base font-semibold text-gray-500 dark:text-gray-400"
          >
            {/* Close button */}
            <button
              type="button"
              onClick={closeDrawer}
              className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 absolute top-2.5 right-2.5 inline-flex items-center justify-center dark:hover:bg-gray-600 dark:hover:text-white"
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
              <span className="sr-only">Close menu</span>
            </button>
          </h5>

          <h1 className="text-white text-[30px] font-bold text-center ">
            Conversation
          </h1>
          <div className="border border-white mt-2"></div>
          <div className="mt-4 text-center">
            <Link to="/uploadFile">
              <button className="bg-teal-700 p-2 rounded-lg">
                New Conversation
              </button>
            </Link>
          </div>

          <div>
            {pdfData.map((item, index) => (
              <div
                key={index}
                className="flex flex-row items-center gap-4  mt-4 justify-start "
              >
                <MdPictureAsPdf color="white" />
                <h5
                  onClick={() => handleName(item.key, item.pdf_file, item.id)}
                  className="font-bold text-[20px] text-white cursor-pointer"
                >
                  {item.pdf_name}
                </h5>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PdfHistoryDrawer;
