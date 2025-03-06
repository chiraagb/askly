import { Routes, Route, BrowserRouter, Navigate } from "react-router-dom";
import UploadFilePage from "../pages/UploadFile/UploadFilePage.jsx";
import ChatScreen from "../pages/chat/ChatScreen.jsx";
import Signin from "../pages/signin/Signup.jsx";
import PdfViewer from "../components/PdfViewer.jsx";
import SidebarLeft from "../pages/chat/SidebarLeft.jsx";
import { SessionProvider } from "../context/summaryContext.jsx";
import ToggleButton from "../pages/chat/ToggleButton.jsx";
import { useSelector } from "react-redux";
import { useEffect } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
// import Homepage from "../pages/home/Homepage";
export const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  const isOpen = useSelector((state) => state.sidebar.isOpen);

  if (!token) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex h-screen bg-[#3A3A3A]">
      <SessionProvider>
        <SidebarLeft />
        <div
          className={`flex-1 transition-margin duration-300 ${
            isOpen ? "ml-[15%]" : "ml-0"
          }`}
        >
          <div className="flex h-screen">
            <ToastContainer />
            <ToggleButton />
            {children}
          </div>
        </div>
      </SessionProvider>
    </div>
  );
};
const MainRoutes = () => {
  const theme = useSelector((state) => state.theme.mode);
  useEffect(() => {
    document.body.className = theme;
  }, [theme]);
  return (
    <BrowserRouter>
      <Routes>
        {/* <Route path="/" element={<Homepage />} /> */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <UploadFilePage />
            </PrivateRoute>
          }
        />

        <Route
          path="/c/:sessionId"
          element={
            <PrivateRoute>
              <ChatScreen />
            </PrivateRoute>
          }
        />
        <Route path="/pdf" element={<PdfViewer />} />
        <Route path="/login" element={<Signin />} />
      </Routes>
    </BrowserRouter>
  );
};
export default MainRoutes;
