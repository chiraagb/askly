import { useEffect, useRef } from "react";
import ReactDOM from "react-dom";
import { TbPencil } from "react-icons/tb";
import { RiDeleteBin6Line } from "react-icons/ri";

const PopUpMenu = ({ onRename, onDelete, top, left, closePopup }) => {
  const modalRef = useRef();

  const checkClickOutside = (e) => {
    console.log("Clicked Outside of popupmenu");
    if (!modalRef.current.contains(e.target)) {
      closePopup(e);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", checkClickOutside);
    return () => {
      document.removeEventListener("mousedown", checkClickOutside);
    };
  }, []);

  return ReactDOM.createPortal(
    <div
      ref={modalRef}
      className="absolute rounded-lg w-36 bg-white dark:bg-[#2f2f2f] shadow-lg z-50 p-2 dark:text-white"
      style={{ top: `${top}px`, left: `${left}px` }}
    >
      <div
        className="flex items-center gap-2 hover:bg-gray-100 dark:hover:bg-[#424242] cursor-pointer p-2 rounded-lg"
        onClick={onRename}
      >
        <TbPencil />
        <div>Rename</div>
      </div>
      <div
        className="flex items-center gap-2 hover:bg-gray-100 dark:hover:bg-[#424242] cursor-pointer p-2 rounded-lg text-red-400"
        onClick={onDelete}
      >
        <RiDeleteBin6Line />
        <div>Delete chat</div>
      </div>
    </div>,
    document.getElementById("portal-root")
  );
};

export default PopUpMenu;
