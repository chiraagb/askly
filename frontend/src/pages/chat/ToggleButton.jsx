import { useDispatch } from "react-redux";
import { toggle } from "../../redux/chat/sidebarSlice.js";

const ToggleButton = () => {
  const dispatch = useDispatch();

  return (
    <>
      <div className="flex items-center w-8 dark:bg-[#1d1d1d] bg-[#efefef] justify-center h-full">
        <button onClick={() => dispatch(toggle())}>
          <div className="bg-[#9B9B9B] hover:bg-[#3d3d3d] rounded-full outline-none h-full">
            <div className="hover:rotate-45 rounded-b-full h-[10px] w-1 "></div>
            <div className="hover:-rotate-45 rounded-t-full h-[10px] w-1 outline-none "></div>
          </div>
        </button>
      </div>
    </>
  );
};

export default ToggleButton;
