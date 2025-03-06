import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import InputField from "./InputField";
import { FaFlagUsa } from "react-icons/fa";
import { IoArrowDown, IoCheckmarkDone } from "react-icons/io5";
import { MdContentCopy } from "react-icons/md";
import { useSession } from "../../context/summaryContext";
import PdfViewer from "../../components/PdfViewer.jsx";
import SessionLoader from "../../components/SessionLoader.jsx";
import "./ChatScreen.css";
import { useParams } from "react-router-dom";

const ChatScreen = () => {
  const [isCopied, setIsCopied] = useState({});
  const [showScrollButton, setShowScrollButton] = useState(false);
  const { sessionId: paramSessionId } = useParams();

  const {
    data,
    setData,
    selectedFileUrl,
    isLoading,
    setIsLoading,
    ws,
    isSessionLoading,
    isGeneratingResponse,
  } = useSession();

  useEffect(() => {
    if (data.length > 0) {
      scrollToBottom();
    }
  }, [data]);

  useEffect(() => {
    const handleBeforeUnload = (event) => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ stop_response: "stop" }));
      }
      event.preventDefault();
      event.returnValue = ""; // Required for some browsers
    };
    console.log(isGeneratingResponse);
    if (isGeneratingResponse) {
      window.addEventListener("beforeunload", handleBeforeUnload);
    }

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, [isGeneratingResponse]);

  const handleScroll = () => {
    const div = document.querySelector("#chatInterface");
    const isAtBottom =
      div.scrollHeight - div.scrollTop === div.clientHeight ||
      div.scrollHeight - div.scrollTop - 1 <= div.clientHeight;
    setShowScrollButton(!isAtBottom);
  };
  useEffect(() => {
    const div = document.querySelector("#chatInterface");
    if (div) {
      div.addEventListener("scroll", handleScroll);
      return () => {
        div.removeEventListener("scroll", handleScroll);
      };
    }
  }, []);
  const scrollToBottom = () => {
    const div = document.querySelector("#chatInterface");
    div?.scrollTo({
      top: div.scrollHeight,
      behavior: "smooth",
    });
  };
  useEffect(() => {
    scrollToBottom();
  }, [paramSessionId, data]);

  const handleCopyToClipboard = (text, messageId) => {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        console.log("Copied", messageId);
        setIsCopied((prev) => ({ ...prev, [messageId]: true }));
        setTimeout(
          () => setIsCopied((prev) => ({ ...prev, [messageId]: false })),
          3000
        );
      })
      .catch((error) => {
        console.error("Failed to copy text: ", error);
      });
  };

  const setFileUrl = (selectedFileUrl) => {
    localStorage.setItem("pdf", selectedFileUrl);
    return <PdfViewer file={localStorage.getItem("pdf")} />;
  };

  return (
    <>
      {isSessionLoading ? (
        <SessionLoader />
      ) : (
        <div className="w-full flex">
          <div className="w-full">
            {selectedFileUrl ? (
              setFileUrl(selectedFileUrl)
            ) : (
              <>
                <PdfViewer file={localStorage.getItem("pdf")} />
              </>
            )}
          </div>
          <div className="relative dark:bg-[#1d1d1d] bg-[#efefef] w-full h-screen dark:text-white text-black flex flex-col justify-between items-center">
            <div
              id="chatInterface"
              className="overflow-y-scroll flex justify-center dark:text-white w-full h-[80%]"
            >
              <div className="flex w-[90%] ml-2">
                <div className="flex text-justify w-[100%] h-full p-2">
                  <div className="flex flex-col flex-grow" id={`bot-content`}>
                    {/* User's messages */}
                    {data.map((ele, index) =>
                      ele.client ? (
                        <div className="flex justify-end pt-[4rem]" key={index}>
                          <div className="w-[50%] relative flex bg-white dark:bg-[#4B4F5B] rounded-3xl py-2 px-3 dark:text-white text-sm ">
                            <div className="absolute top-[-1rem] left-[-1rem] flex items-center justify-center w-[40px] h-[40px] bg-black dark:bg-[#3f3f3f] rounded-full text-white dark:text-white">
                              <img
                                src={localStorage.getItem("profile")}
                                className="rounded-full h-10 w-10"
                              />
                            </div>
                            <div className="absolute flex gap-2 top-[-1.2rem] left-7 w-[10rem]">
                              <p className="font-semibold text-[15px] dark:text-[#EEEEEE]">
                                {localStorage.getItem("first_name")}
                              </p>
                              <p className="font-normal text-[12px] dark:text-[#ABABAB99]"></p>
                            </div>
                            <p className="p-2 text-[16px] leading-[25px] tracking-normal">
                              {ele.message}
                            </p>
                          </div>
                        </div>
                      ) : (
                        <div
                          className="w-[100%] flex justify-start gap-5 px-2 pt-[2rem]"
                          key={index}
                        >
                          <div className="relative flex bg-white dark:bg-[#28303F] rounded-3xl py-2 px-3 dark:text-white text-sm ">
                            <div className="absolute top-[-1rem] left-[-1rem] flex items-center justify-center w-[40px] h-[40px] bg-black dark:bg-[#4D2C97] rounded-full text-white dark:text-white">
                              <FaFlagUsa />
                            </div>
                            <div className="absolute flex gap-2 top-[-1.2rem] left-7 w-[12rem]">
                              <p className="font-semibold text-[15px] dark:text-[#EEEEEE]">
                                BidAmerica
                              </p>
                              <p className="font-normal text-[12px] dark:text-[#ABABAB99]"></p>
                            </div>
                            <div className="flex flex-col">
                              {/* {console.log(data.length, "data length", index+1)} */}
                              {!ele.message &&
                              isLoading &&
                              data.length === index + 1 ? (
                                <div className="ml-8 mr-auto flex h-10 min-h-[10px] max-w-2xl items-center gap-1 overflow-hidden rounded-2xl bg-opacity-80 p-3 text-left backdrop-blur-3xl backdrop-filter">
                                  <div className="animate-slide-1 h-2 w-2 rounded-full bg-[#555657]"></div>
                                  <div className="animate-slide-2 h-2 w-2 rounded-full bg-[#555657]"></div>
                                  <div className="animate-slide-3 h-2 w-2 rounded-full bg-[#555657]"></div>
                                </div>
                              ) : (
                                <div>
                                  <p
                                    className="p-2 text-[16px]"
                                    // ref={responseDivRef}
                                  >
                                    <ReactMarkdown
                                      id={`bot-content-${ele.id}`}
                                      className="prose dark:text-white"
                                      style={{
                                        color: "white",
                                      }}
                                    >
                                      {ele.message}
                                    </ReactMarkdown>
                                  </p>
                                  <div className="flex dark:text-white justify-end gap-2 h-[2rem]">
                                    <div
                                      className="flex items-center justify-center gap-1 w-[5rem] bg-[#D8D8D8] dark:bg-black rounded-lg cursor-pointer font-semibold"
                                      onClick={() =>
                                        handleCopyToClipboard(
                                          ele.message,
                                          `bot-content-${ele.id}`
                                        )
                                      }
                                    >
                                      <div>
                                        {isCopied[`bot-content-${ele.id}`] ? (
                                          <IoCheckmarkDone />
                                        ) : (
                                          <MdContentCopy />
                                        )}
                                      </div>
                                      <div>
                                        <p className="text-[15px] leading-[8px] font-normal">
                                          {isCopied[`bot-content-${ele.id}`]
                                            ? "Copied"
                                            : "Copy"}
                                        </p>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div className="relative flex items-center justify-center">
              <button
                id="buttonScroll"
                onClick={scrollToBottom}
                className={`absolute bottom-[10rem] border border-[#292929] bg-[#292929] text-[#ECECEC]  outline-none text-2xl p-3  hover:scale-105 duration-500 rounded-full ${
                  showScrollButton ? "visible" : "opacity-0"
                }`}
              >
                {<IoArrowDown />}
              </button>
            </div>

            <div className="absolute flex items-center justify-center bottom-[3rem] w-[90%]">
              <InputField
                data={data}
                setData={setData}
                ws={ws}
                setIsLoading={setIsLoading}
              />
              {/* <InputField scrollToBottom={scrollToBottom} /> */}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatScreen;
