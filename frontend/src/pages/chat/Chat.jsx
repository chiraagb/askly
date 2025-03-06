// import { useEffect, useRef, useState } from "react";
// import axios from "axios";
// import { useLocation } from "react-router-dom";
// import ViewPdf from "../../components/ViewPdf";
// import { IoSendSharp } from "react-icons/io5";
// import Menu from "./Menu";
// import { BsFillArrowDownCircleFill } from "react-icons/bs";
// import { toast } from "react-toastify";

// const Chat = () => {
//   const location = useLocation();
//   const [messageData, setMessageData] = useState([]);
//   const [inputMessage, setInputMessage] = useState("");
//   const [showScrollButton, setShowScrollButton] = useState(false);
//   const chatContainerRef = useRef(null);

//   // const scrollToBottom = () => {
//   //   const bottomMessage = document.getElementById("bottom-message");
//   //   if (bottomMessage) {
//   //     bottomMessage.scrollIntoView({ behavior: "smooth" });
//   //   }
//   // };

//   const scrollToBottom = () => {
//     if (chatContainerRef.current) {
//       chatContainerRef.current.scrollTop =
//         chatContainerRef.current.scrollHeight;
//     }
//   };

//   const getMessageData = async () => {
//     const pdf_key = localStorage.getItem("pdfKey");
//     try {
//       const res = await axios.get(
//         process.env.REACT_APP_BASE_URL +
//           `/api/v1/readpdf/chats/?pdfKey=${pdf_key}`,
//         {
//           headers: {
//             Authorization: "Token " + localStorage.getItem("token"),
//           },
//         }
//       );
//       setMessageData([...res.data.chats]);
//       scrollToBottom();
//       // console.log("chats", res.data.chats);
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   const chatResponse = async (data, client_message) => {
//     const pdf_key = localStorage.getItem("pdfKey");
//     try {
//       setMessageData([
//         ...data,
//         {
//           id: data.length,
//           msg: (
//             <div className="loader w-6 h-6 border-t-4 border-b-4 border-blue-500 border-solid rounded-full animate-spin"></div>
//           ),
//           client: false,
//         },
//       ]);

//       setTimeout(() => {
//         scrollToBottom();
//       }, 0);

//       const res = await axios.post(
//         process.env.REACT_APP_BASE_URL + "/api/v1/readpdf/qdrant-chat/",
//         {
//           client_message: client_message,
//           pdf_key: pdf_key,
//         },
//         {
//           headers: {
//             Authorization: "Token " + localStorage.getItem("token"),
//           },
//         }
//       );
//       const newMessage = {
//         id: data.length,
//         msg: res.data.msg,
//         client: false,
//       };
//       // console.log("res", res.data);
//       // console.log("messageData", messageData);
//       setMessageData([...data, newMessage]);
//       scrollToBottom();
//     } catch (err) {
//       if (err.response.data.msg == "Payment required") {
//         toast.warn("Plan Expired, Please upgrade your plan", {
//           autoClose: 2000,
//         });
//       }
//       // console.log("err",err.response.data);
//     }
//   };

//   const handleInput = (something = null) => {
//     const newMessageData = [
//       ...messageData,
//       {
//         id: messageData.length,
//         msg: something ? something : inputMessage,
//         client: true,
//       },
//     ];
//     setMessageData(newMessageData);
//     chatResponse(newMessageData, something ? something : inputMessage);
//     setInputMessage("");
//     scrollToBottom();
//   };

//   const handleInputKeyPress = (e) => {
//     if (e.key === "Enter") {
//       handleInput();
//     }
//   };

//   const handleScroll = () => {
//     if (chatContainerRef.current) {
//       const remainingScroll =
//         chatContainerRef.current.scrollHeight -
//         chatContainerRef.current.scrollTop -
//         chatContainerRef.current.clientHeight;

//       if (remainingScroll <= 10) {
//         setShowScrollButton(false);
//       } else {
//         setShowScrollButton(true);
//       }
//     }
//   };

//   useEffect(() => {
//     getMessageData();
//     const chatContainer = chatContainerRef.current;

//     if (chatContainer) {
//       chatContainer.addEventListener("scroll", handleScroll);
//     }

//     // Scroll to the bottom when the component initially loads
//     scrollToBottom();

//     return () => {
//       if (chatContainer) {
//         chatContainer.removeEventListener("scroll", handleScroll);
//       }
//     };
//   }, []);

//   return (
//     <div className="chat-container flex flex-col md:flex-row justify-evenly h-full md:h-screen w-full">
//       <div className="">
//         <Menu />
//       </div>
//       <div className="data-display border-x-2 w-full  h-full text-center">
//         <ViewPdf file={location.state.file} />
//       </div>
//       <div className="chatbot w-full  h-full text-center flex flex-col">
//         <div className="summary-container w-full  p-2">
//           <div className="summary text-sm py-2 px-4 font-sans text-left bg-gray-800 text-gray-200 rounded-lg">
//             {location.state.summary}
//             <div className="mt-5">
//               <p>Here are some sample questions :</p>
//               <br />
//               {location.state.questions.map((ele, index) => (
//                 <div
//                   key={index}
//                   onClick={(e) => handleInput(e.currentTarget.innerText)}
//                   className="flex gap-2 items-center py-[2px] cursor-pointer"
//                 >
//                   <IoSendSharp color="lightblue" />
//                   <p className="">{ele.question}</p>
//                 </div>
//               ))}
//             </div>
//           </div>
//         </div>
//         <div
//           className="chat-container  h-full flex flex-col justify-between overflow-y-auto"
//           ref={chatContainerRef}
//         >
//           <div className="chats-container  flex-grow flex flex-col gap-2 p-3">
//             {messageData.length === 0 ? (
//               <div className="w-full m-auto text-center text-gray-300">
//                 <img
//                   className="w-[300px] m-auto text-center"
//                   src="https://i.pinimg.com/736x/54/85/6a/54856ab427f28a0b40b1a305792a3b00.jpg"
//                   alt=""
//                 />
//               </div>
//             ) : (
//               messageData.map((ele, index) =>
//                 ele.client ? (
//                   <div className="w-full flex justify-end" key={index}>
//                     <span
//                       className="px-4 py-2 bg-blue-500 rounded-xl text-white text-sm text-left"
//                       id={ele.id}
//                     >
//                       {ele.msg}
//                     </span>
//                   </div>
//                 ) : (
//                   <div className="w-full flex justify-start" key={index}>
//                     <span
//                       className="px-4 py-2 rounded-xl border-gray-300 bg-gray-800 text-gray-200 border-[1px] text-sm max-w-[85%] text-left"
//                       id={ele.id}
//                     >
//                       {ele.msg}
//                     </span>
//                   </div>
//                 )
//               )
//             )}
//           </div>
//         </div>
//         <div className="chat-input-box-container flex  p-5">
//           <input
//             onKeyPress={handleInputKeyPress}
//             placeholder="Enter your query"
//             value={inputMessage}
//             onInput={(e) => setInputMessage(e.target.value)}
//             type="text"
//             className="w-full border-2 self-end border-blue-500 rounded-md py-1 px-3 "
//           />
//           <button
//             onClick={handleInput}
//             className="border-2 bg-blue-500 w-10 rounded-md  h-9 flex justify-center items-center"
//           >
//             <IoSendSharp color="white" />
//           </button>
//           {showScrollButton && (
//             <button
//               onClick={scrollToBottom}
//               className="fixed right-4 bottom-16 bg-blue-500 text-white rounded-full cursor-pointer"
//             >
//               <BsFillArrowDownCircleFill size={22} />
//             </button>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Chat;
