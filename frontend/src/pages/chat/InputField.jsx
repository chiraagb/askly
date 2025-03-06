import { useEffect, useRef, useState } from "react";
import { FiStopCircle } from "react-icons/fi";
import { IoSend } from "react-icons/io5";
import { useLocation, useNavigate } from "react-router-dom";
import { useSession } from "../../context/summaryContext";
import { FaRegPlusSquare } from "react-icons/fa";
import { IoMdClose } from "react-icons/io";
import { FaHandPointRight } from "react-icons/fa";
// eslint-disable-next-line react/prop-types
const InputField = ({ scrollToBottom }) => {
  const [messages, setMessages] = useState("");
  const inputRef = useRef(null);
  const location = useLocation();
  const {
    setHomeContent,
    generateSessionId,
    sessionId,
    setSessionId,
    data,
    setData,
    ws,
    setIsLoading,
    initChatSession,
    isGeneratingResponse,
    setIsGeneratingResponse,
    setWs,
    setSelectedSessionId,
    fetchSessionChats,
  } = useSession();
  const navigate = useNavigate();
  const [isExpanded, setIsExpanded] = useState(false);

  const handleInput = async (
    session_Id,
    wsInstance,
    inputMessage = messages
  ) => {
    if (isGeneratingResponse) {
      console.log(
        "Response is currently generating. Cannot send new messages."
      );
      return; // Exit the function if a response is generating
    }
    // navigate(`/c/${session_Id}`);
    // Check if the message is empty or WebSocket is not ready
    // if (!messages.trim()) {
    //   console.error("Unable to send message: Input is empty");
    //   return;
    // }
    if (!wsInstance) {
      console.error(
        `Unable to send message: WebSocket is not open or undefined, ${wsInstance}, ${session_Id}`
      );
      return;
    }

    const userMessage = {
      id: data.length,
      message: inputMessage,
      client: true,
    };

    if (inputRef.current) {
      inputRef.current.style.height = "53px";
    }

    setData((prevMessages) => [...prevMessages, userMessage]);
    // console.log(userMessage, data, "After setting data user message is");

    const messageObject = {
      client_message: inputMessage,
    };
    console.log(wsInstance);
    wsInstance.send(JSON.stringify(messageObject));
    console.log(
      "Client Message",
      messageObject.client_message,
      `for ${session_Id}`
    );

    setData((prevMessages) => [
      ...prevMessages,
      {
        id: data.length,
        message: "",
        client: false,
      },
    ]);

    setIsLoading(true);
    setMessages("");
    setIsGeneratingResponse(true);
    localStorage.setItem("data-length", JSON.stringify(data.length));
  };

  const handleInputKeyPress = async (e) => {
    try {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();

        if (isGeneratingResponse) {
          console.log(
            "Response is currently generating. Cannot send new messages."
          );
          return; // Do not send messages if response is generating
        }

        /** For handling empty input */
        if (!messages.trim()) {
          console.log("Empty input, no action taken.");
          return;
        }

        setHomeContent(false);

        if (location.pathname === "/") {
          console.log("Currently on home page", sessionId);
          try {
            if (ws && ws.readyState !== WebSocket.CLOSED) {
              console.log("Websocket closed: ", ws);
              ws.close();
            }

            const newSessionId = await generateSessionId();
            console.log(newSessionId, "new sessionId is generated InputField");

            setSessionId(newSessionId);
            setSelectedSessionId(newSessionId);

            const wsInstance = await initChatSession(newSessionId);
            setWs(wsInstance);

            await fetchSessionChats(newSessionId);
            navigate(`/c/${newSessionId}`);

            console.log("sending message to: ", newSessionId, wsInstance);
            handleInput(newSessionId, wsInstance);
          } catch (error) {
            console.error(
              "Error in generating session Id or websocket setup: ",
              error
            );
          }
        } else {
          console.log(
            "Directly sending message to existing session",
            sessionId
          );
          handleInput(sessionId, ws);
        }
        // scrollToBottom();
      }
    } catch (error) {
      console.error("Error in pressing Enter key", error);
    }
  };
  const handleTextAreaInput = (e) => {
    e.target.style.height = "56px";
    e.target.style.height = `${e.target.scrollHeight}px`;
    setMessages(e.target.value);
  };
  const handleResponse = () => {
    if (ws) {
      const messageObject = { stop_response: "stop" };
      ws.send(JSON.stringify(messageObject));
      console.log("Stop message sent to WebSocket server.");
      setIsGeneratingResponse(false); // Ensuring that response generation is stopped
      setIsLoading(false); // Make sure to stop loading indication
    } else {
      console.error("WebSocket is not connected.");
    }
  };
  useEffect(() => {
    inputRef.current.focus();
  }, []);

  const handlePrompt = () => {
    const predefinedMessage = "/summarize";
    handleInput(sessionId, ws, predefinedMessage);
  };
  return (
    <>
      <div className="relative flex items-center justify-center w-full">
        {/* Text Area  */}
        <textarea
          type="text"
          className={`w-full dark:bg-opacity-5 dark:bg-white pl-5 h-[53px] rounded-md border-[3px] border-[#EFEFEF] dark:placeholder-[#E5E5E54D] dark:border dark:border-transparent dark:border-opacity-20 dark:text-white outline-none resize-none pt-[12px] max-sm:pt-[17px] max-sm:placeholder:text-[9px]`}
          placeholder="Example: What is the bidding date of the project ?"
          onKeyPress={handleInputKeyPress}
          value={messages}
          onInput={handleTextAreaInput}
          onChange={(e) => e.target.value}
          ref={inputRef}
          style={{
            maxHeight: "150px",
            resize: "none",
          }}
          // disabled={isGeneratingResponse}
        />

        {/* Stop Response  */}
        {console.log("genrating response catched", isGeneratingResponse)}
        {isGeneratingResponse ? (
          <div className="absolute right-[10px] bottom-[7px]">
            <div
              className="flex items-center gap-2 text-white p-3 rounded-lg cursor-pointer"
              style={{
                background:
                  "linear-gradient(91.96deg, #5815EE -16.64%, #3387F7 117.28%)",
              }}
              onClick={() => {
                handleResponse();
              }}
            >
              <div>
                <FiStopCircle />
              </div>
            </div>
          </div>
        ) : (
          <button
            className="absolute flex items-center justify-center bottom-[6.5px] right-[10px] w-[40px] h-[40px] rounded-lg text-white"
            style={{
              background:
                "linear-gradient(91.96deg, #227BD1 -16.64%, #8F56E2 117.28%)",
            }}
          >
            <IoSend
              className="h-4 w-4"
              onClick={() => handleInput(sessionId, ws)}
            />
          </button>
        )}
        <div className="relative" onClick={() => setIsExpanded(!isExpanded)}>
          <div
            className="h-[30px] w-[60px] absolute right-0 bottom-[34px] cursor-pointer flex items-center justify-center rounded-[4px]"
            style={{
              background:
                "linear-gradient(91.96deg, #5815EE -16.64%, #3387F7 117.28%)",
            }}
          >
            <div className="h-[20px] text-[12px] flex items-center justify-center text-white">
              <p>Prompts</p>
            </div>
          </div>
          {isExpanded && (
            <div className="absolute bottom-[60px] right-0 mb-2 w-[200px] p-2 text-white rounded-md shadow-lg bg-[#171717]">
              <div className="flex items-end justify-end cursor-pointer">
                <IoMdClose
                  className="w-[20px] h-[20px]"
                  onClick={() => setIsExpanded(false)}
                />
              </div>
              <ul className="space-y-2">
                <li
                  className="hover:bg-[#292929] p-2 rounded-md cursor-pointer flex items-center justify-center gap-[14px]"
                  onClick={() => handlePrompt()}
                >
                  <FaHandPointRight /> <p>Summarize the bid</p>
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </>
  );
};
export default InputField;
