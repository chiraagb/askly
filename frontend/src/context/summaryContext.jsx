import axios from "axios";
import { createContext, useContext, useEffect, useState } from "react";

const SessionContext = createContext();

// eslint-disable-next-line react-refresh/only-export-components
export function useSession() {
  return useContext(SessionContext);
}

// eslint-disable-next-line react/prop-types
export const SessionProvider = ({ children }) => {
  const [sessions, setSessions] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [homeContent, setHomeContent] = useState(false);
  const [data, setData] = useState([]);
  const [ws, setWs] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isGeneratingResponse, setIsGeneratingResponse] = useState(false);
  const [selectedFileUrl, setSelectedFileUrl] = useState("");
  const [isSessionLoading, setIsSessionLoading] = useState(false);
  const [selectedSessionId, setSelectedSessionId] = useState(null);

  useEffect(() => {
    if (location.pathname === "/") {
      setSelectedSessionId(null);
    } else {
      setSelectedSessionId(sessionStorage.getItem("selectedSessionId"));
    }
  }, [selectedSessionId]);
  const generateSessionId = async () => {
    try {
      const token = localStorage.getItem("token");
      // console.log(token);
      const sessionIdResponse = await axios.post(
        import.meta.env.VITE_BASE_URL + `/api/v1/aila/session/`,
        {},
        {
          headers: {
            "content-type": "text/json",
            Authorization: `Token ${token}`,
          },
        }
      );

      if (sessionIdResponse.data.id) {
        setSessionId(sessionIdResponse.data.id);
        return sessionIdResponse.data.id;
      }
    } catch (error) {
      console.log(error);
    }
  };

  const initChatSession = async (session_Id) => {
    return new Promise((resolve, reject) => {
      console.log(session_Id, "defined in initChatSession");
      const token = localStorage.getItem("token");
      const wsBaseUrl = import.meta.env.VITE_WS_BASE_URL;
      const wsUrl = `${wsBaseUrl}/ws/chat-async/${session_Id}/?token=${token}`;
      // const socket = new WebSocket(wsUrl);

      if (!session_Id) {
        console.error("Session ID is null");
        reject(new Error("Invalid session ID"));
      }

      let socket;
      if (ws && ws.readyState !== WebSocket.CLOSED) {
        ws.close();
      }

      socket = new WebSocket(wsUrl);

      socket.onopen = () => {
        console.log("Web Socket Connected..!", session_Id);
        resolve(socket);
      };

      socket.onmessage = (event) => {
        try {
          console.log("Message received for: ", session_Id);
          const responseData = JSON.parse(event.data);
          const { response, is_complete } = responseData;
          setIsLoading(false);
          console.log(data);
          setData((prevData) => {
            if (prevData.length === 0 || prevData[prevData.length - 1].client) {
              return [
                ...prevData,
                { id: prevData.length, message: response, client: false },
              ];
            } else {
              // Append the message to the last bot message
              const lastMessage = { ...prevData[prevData.length - 1] };

              lastMessage.message += response;
              return [...prevData.slice(0, -1), lastMessage];
            }
          });
          if (is_complete) {
            setIsGeneratingResponse(false);
            console.log(session_Id);
            // fetchSessionSummary(session_Id);
          } else {
            setIsGeneratingResponse(true);
          }
        } catch (error) {
          console.error("Error parsing incoming message: ", error);
        }
      };

      socket.onerror = (err) => {
        console.error("Error in web socket connection: ", err);
        reject(err);
      };

      socket.onclose = () => {
        console.log(`WebSocket closed for session ${session_Id}`);
      };
    });
  };
  // const fetchSessionSummary = async (session_Id) => {
  //   console.log("Fetching session summary...", session_Id);
  //   try {
  //     const token = localStorage.getItem("token");
  //     const res = await axios.get(
  //       import.meta.env.VITE_BASE_URL +
  //         `/api/v1/aila/session-summary/${session_Id}/`,
  //       {
  //         headers: {
  //           Authorization: `Token ${token}`,
  //         },
  //       }
  //     );
  //     setSessionSummaries((prevSummaries) => ({
  //       ...prevSummaries,
  //       [session_Id]: res.data.msg,
  //     }));
  //     // console.log(res.data);
  //   } catch (error) {
  //     console.error("Failed to fetch session summary:", error);
  //   }
  // };

  const fetchSessionChats = async (session_Id) => {
    console.log("Fetching session chats for", session_Id);

    const token = localStorage.getItem("token");
    try {
      if (session_Id) {
        const res = await axios.get(
          import.meta.env.VITE_BASE_URL +
            `/api/v1/chat/session-chats/${session_Id}/`,
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        console.log(res);
        setData(res.data);
      }
    } catch (error) {
      console.error("Error fetching session chats:", error);
    }
  };

  return (
    <SessionContext.Provider
      value={{
        sessionId,
        setSessionId,
        generateSessionId,
        homeContent,
        setHomeContent,
        data,
        setData,
        ws,
        setWs,
        isLoading,
        setIsLoading,
        isGeneratingResponse,
        setIsGeneratingResponse,
        initChatSession,
        fetchSessionChats,
        sessions,
        setSessions,
        selectedFileUrl,
        setSelectedFileUrl,
        isSessionLoading,
        setIsSessionLoading,
        selectedSessionId,
        setSelectedSessionId,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
};
