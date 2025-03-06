import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { MdOutlineChatBubbleOutline } from "react-icons/md";
import PopUpMenu from "./PopUpMenu";
import { toast } from "react-toastify";
import { useNavigate, useParams } from "react-router-dom";
import { useSession } from "../../context/summaryContext";

const SessionHistory = () => {
  const [editingSessionId, setEditingSessionId] = useState(null);
  const [editingName, setEditingName] = useState({});
  const [activePopupId, setActivePopupId] = useState(null);
  const [popupPosition, setPopupPosition] = useState({ top: 0, left: 0 });
  const {
    sessionSummaries,
    sessionId,
    setSessionId,
    selectedSessionId,
    setSelectedSessionId,
    setHomeContent,
    initChatSession,
    setWs,
    fetchSessionChats,
    sessions,
    setSessions,
    setSelectedFileUrl,
    setIsSessionLoading,
    isGeneratingResponse,
    setIsGeneratingResponse,
  } = useSession();
  const navigate = useNavigate();
  const inputRef = useRef();
  const { sessionId: paramSessionId } = useParams();

  useEffect(() => {
    console.log(paramSessionId, "Params session Id catched");
    if (paramSessionId) {
      setIsGeneratingResponse(false);
      handleSessionNameClick(paramSessionId);
    }
  }, [paramSessionId]);

  useEffect(() => {
    if (editingSessionId !== null && inputRef.current) {
      inputRef.current.focus(); // Focus the input element when editing session
    }
  }, [editingSessionId]);

  const getChatHistory = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get(
        import.meta.env.VITE_BASE_URL + `/api/v1/chat/session/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );
      console.log(res);
      setSessions(res.data);
      // console.log(sessions);
      // console.log(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getChatHistory();
  }, [sessionId]);

  const saveSessionName = async (session_Id) => {
    const newName = editingName[session_Id].trim(); // Trim to remove any whitespace

    // Fetch the original name for comparison and fallback
    const originalName = sessions.find((s) => s.id === session_Id)?.name || "";

    // Check if newName is empty after trimming and if it's not just the original name
    if (!newName && newName !== originalName) {
      toast.error("Session name cannot be empty", {
        position: "top-center",
        autoClose: 2000,
      });
      // Revert to the original name if new name is empty
      setEditingName({
        ...editingName,
        [session_Id]: originalName,
      });
      setEditingSessionId(null);
      return;
    }

    // Continue with the name update only if it has changed
    if (newName !== originalName) {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.put(
          `${import.meta.env.VITE_BASE_URL}/api/v1/chat/session/${session_Id}/`,
          { name: newName },
          { headers: { Authorization: `Token ${token}` } }
        );
        console.log("Session updated:", response.data);

        setSessions(
          sessions.map((session) =>
            session.id === session_Id ? { ...session, name: newName } : session
          )
        );
        toast.success("Session name updated successfully");
      } catch (error) {
        console.error("Failed to update session name:", error);
        toast.error("Failed to update session name");
      }
    }

    // Always clear editing state, even if the name didn't change
    setEditingSessionId(null);
  };

  useEffect(() => {
    console.log("Active Popup ID changed:", activePopupId);
  }, [activePopupId]);

  const togglePopup = (e, session_Id) => {
    e.stopPropagation(); // Prevent the click from bubbling up to higher elements which might have their own handlers.
    const rect = e.currentTarget.getBoundingClientRect();
    const top = rect.top + rect.height;
    const left = rect.left;

    setActivePopupId((current) => {
      const newValue = current === session_Id ? null : session_Id;
      console.log(`Toggling popup. Was: ${current}, Will be: ${newValue}`);
      if (newValue !== null) {
        setPopupPosition({ top, left });
      }
      return newValue;
    });
  };

  const handleRename = (e, session_Id) => {
    e.stopPropagation(); // Stop the click from bubbling up
    setActivePopupId(null); // Close any open popup

    // Retrieve the current session name from the sessions array
    const currentName = sessions.find(
      (session) => session.id === session_Id
    )?.name;

    if (currentName !== undefined) {
      setEditingName({
        ...editingName,
        [session_Id]: currentName, // Set the current name as the initial value for editing
      });
    }

    setEditingSessionId(session_Id); // Set the current session as being edited
  };

  const handleDelete = async (e, session_Id) => {
    e.stopPropagation();
    try {
      const token = localStorage.getItem("token");
      await axios.delete(
        `${import.meta.env.VITE_BASE_URL}/api/v1/chat/session/${session_Id}/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      const updatedSessions = sessions.filter(
        (session) => session.id !== session_Id
      );
      setSessions(updatedSessions);

      if (selectedSessionId === session_Id) {
        setSelectedSessionId(null);
        setSessionId(null);
        setWs(null);
        setHomeContent(true);

        if (updatedSessions.length > 0) {
          const nextSessionId = updatedSessions[0].id;
          setSelectedSessionId(nextSessionId);
          setSessionId(nextSessionId);
          navigate(`/c/${nextSessionId}`);

          const wsInstance = await initChatSession(nextSessionId);
          setWs(wsInstance);
          await fetchSessionChats(nextSessionId);
          const nextSession = updatedSessions.find(
            (session) => session.id === nextSessionId
          );
          if (nextSession) {
            setSelectedFileUrl(nextSession.file);
          }
          console.log(
            "Navigated to next session with updated file:",
            nextSessionId
          );
        } else {
          navigate("/");
          console.log("No sessions left, redirected to home.");
        }
      }

      setActivePopupId(null);
      console.log("Deleted session:", session_Id);
    } catch (error) {
      console.error("Failed to delete session:", error);
      toast.error("Failed to delete session");
    }
  };

  const handleSessionNameClick = async (session_Id) => {
    setIsSessionLoading(true);
    try {
      setSessionId(session_Id);
      const wsInstance = await initChatSession(session_Id);
      setWs(wsInstance);
      // console.log("Websocket connected and then naivgating");
      await fetchSessionChats(session_Id);
      const selectedSession = sessions.find(
        (session) => session.id === session_Id
      );
      if (selectedSession) {
        // console.log(selectedSession.file);
        setSelectedFileUrl(selectedSession.file);
      }

      navigate(`/c/${session_Id}`);
    } catch (error) {
      console.error("Error in navigating and connecting to websocket...");
    } finally {
      setIsSessionLoading(false);
    }
  };

  const handleSessionClick = (e, session_Id) => {
    try {
      if (location.pathname === "/") {
        setSelectedSessionId(session_Id);
      }
      e.stopPropagation();
      // localStorage.setItem("selectedSessionId", session_Id);
      setSelectedSessionId(localStorage.getItem("selectedSessionId"));

      if (ws && isGeneratingResponse) {
        const messageObject = { stop_response: "stop" };
        ws.send(JSON.stringify(messageObject));
        console.log("Stop message sent to WebSocket server.");
        console.log("Inside sessionClick");
        setIsGeneratingResponse(false);
        setIsLoading(false);
      }
    } catch (error) {
      console.error("Error handling session click:", error);
    }
  };

  const closePopup = (e) => {
    e.stopPropagation();
    setActivePopupId(null);
  };

  return (
    <>
      {/* Session History  */}

      <div className="overflow-y-scroll h-[calc(100vh-251px)] p-4 pt-0 pb-[16px] w-[100%] ">
        <div className="flex flex-col gap-1 pt-0 pb-0 w-[100%]">
          {sessions.map((session) => (
            <div
              className={`flex items-center justify-between cursor-pointer hover:rounded-lg gap-3 w-[100%] ${
                sessionStorage.getItem("selectedSessionId") == session.id
                  ? "bg-[#e5e5e5] dark:bg-[#292929]   rounded-lg"
                  : "hover:bg-[#E5e5e5] dark:hover:bg-[#292929] hover:rounded-lg"
              }`}
              key={session.id}
              onClick={(e) => {
                handleSessionClick(e, session.id);
                setSelectedSessionId(
                  sessionStorage.setItem("selectedSessionId", session.id)
                );
              }}
            >
              {/* {console.log(paramSessionId, "inside JSX", session.id)} */}
              <div className="flex items-center justify-between w-full dark:text-white text-black">
                <div className="flex items-center justify-center w-full">
                  <div className="p-3">
                    <MdOutlineChatBubbleOutline className="h-5 w-5" />
                  </div>

                  <div
                    className="text-[16px] leading-[24px] font-normal w-full"
                    style={{
                      maxWidth: "100%",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {editingSessionId === session.id ? (
                      <input
                        ref={inputRef}
                        type="text"
                        value={editingName[session.id]}
                        onChange={(e) =>
                          setEditingName({
                            ...editingName,
                            [session.id]: e.target.value,
                          })
                        }
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            e.preventDefault();
                            saveSessionName(session.id);
                          }
                        }}
                        onBlur={() => saveSessionName(session.id)}
                        className="input dark:bg-white dark:bg-opacity-[10%] border-[2px] border-[#2563EB] outline-none p-1 dark:text-white"
                      />
                    ) : (
                      <div
                        className="w-full h-full p-3 pl-0"
                        onClick={() => {
                          handleSessionNameClick(session.id);
                        }}
                      >
                        {session.name}
                      </div>
                    )}
                  </div>
                  <div className="p-3">
                    <div
                      className="relative"
                      onClick={(e) => togglePopup(e, session.id)}
                    >
                      <BsThreeDotsVertical />
                    </div>
                  </div>
                  {activePopupId == session.id && (
                    <PopUpMenu
                      onRename={(e) => handleRename(e, session.id)}
                      onDelete={(e) => handleDelete(e, session.id)}
                      top={popupPosition.top}
                      left={popupPosition.left}
                      closePopup={(e) => closePopup(e)}
                      session_Id={session.id}
                    />
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};
export default SessionHistory;
