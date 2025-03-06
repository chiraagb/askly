// import { useState } from "react";
// import { FiLogOut, FiMenu } from "react-icons/fi";
// import PdfHistoryDrawer from "./PdfHistoryDrawer";
// import ProfileModal from "./ProfileModal";
// import { BiUpload } from "react-icons/bi";
// import { AiFillHome, AiFillSetting } from "react-icons/ai";
// import { FaArrowAltCircleLeft, FaYoutube } from "react-icons/fa";
// import { SiMicrosoftexcel } from "react-icons/si";
// import { Link } from "react-router-dom";
// import { toast } from "react-toastify";
// import { CgDatabase } from "react-icons/cg";

// const navItems = [
//   // {
//   //   icon:(
//   //     <Link to="/">
//   //    <AiFillHome />
//   //     </Link>
//   //   )
//   // },
//   {
//     icon: (
//       <Link to="/uploadFile">
//         <BiUpload />
//       </Link>
//     ),
//     name: "Upload Document",
//   },
//   {
//     icon: <PdfHistoryDrawer />,
//     name: "Chat Conversation",
//   },
//   {
//     icon: (
//       <Link to="/UploadYoutubeUrl">
//         <FaYoutube />
//       </Link>
//     ),
//     name: "Upload Youtube Url",
//   },
//   // {
//   //   icon: (
//   //     <Link to="/youtube-summary">
//   //       <CgDatabase />
//   //     </Link>
//   //   ),
//   //   name: "Youtube Summary",
//   // },
//   {
//     icon: (
//       <Link to="/upload-excel">
//         <SiMicrosoftexcel />
//       </Link>
//     ),
//     name: "Upload Excel",
//   },
//   {
//     icon: (
//       <Link to="/setting">
//         <AiFillSetting />
//       </Link>
//     ),
//     name: "Settings",
//   },
//   {
//     icon: <ProfileModal />,
//     name: "Profile",
//   },
// ];

// export default function Menu() {
//   const [open, setOpen] = useState(false);

//   const handleDrawerOpen = () => {
//     setOpen(true);
//   };

//   const handleDrawerClose = () => {
//     setOpen(false);
//   };

//   const logout = () => {
//     localStorage.clear();
//     window.location.reload();
//   };

//   return (
//     <div className=" h-full md:h-screen  bg-gray-100">
//       <nav
//         className={`bg-gray-800 transition-all ${
//           open ? "w-60" : "w-14"
//         } h-full md:h-screen fixed z-50 top-0 left-0 flex flex-col justify-between`}
//       >
//         <div>
//           <div
//             className={`p-4 text-white flex items-center ${
//               open ? "justify-end" : "justify-between"
//             }  `}
//           >
//             {open ? (
//               <button onClick={handleDrawerClose} className="text-white">
//                 <FaArrowAltCircleLeft size={20} />
//               </button>
//             ) : (
//               <button onClick={handleDrawerOpen} className="text-white">
//                 <FiMenu size={20} />
//               </button>
//             )}
//           </div>
//           <div className="h-px bg-white mb-4"></div>
//           <ul className="text-white">
//             {/* {navItems.map((item, index) => (
//               <li key={item.name} className="mb-4">
//                 <a className={`flex items-center ${open ? "pl-6" : "pl-4"}`}>
//                   <h1 className="text-[20px] text-center">{item.icon}</h1>
//                   {open && <span className="ml-2">{item.name}</span>}
//                 </a>
//               </li>
//             ))} */}
//           </ul>
//         </div>

//         <div>
//           <div className="h-px bg-white my-4"></div>
//           <ul className="text-white pb-1">
//             <button
//               onClick={logout}
//               className={`flex items-center ${open ? "pl-6" : "pl-4"}`}
//             >
//               <h1 className="text-[20px]">
//                 <FiLogOut />
//               </h1>
//               {open && <span className="ml-2">Logout</span>}
//             </button>
//           </ul>
//         </div>
//       </nav>
//     </div>
//   );
// }
