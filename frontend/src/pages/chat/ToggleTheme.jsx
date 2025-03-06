import { MdOutlineNightsStay, MdOutlineWbSunny } from "react-icons/md";
import { useDispatch, useSelector } from "react-redux";
import { toggleTheme } from "../../redux/theme/themeSlice.js";
const ToggleTheme = () => {
  const theme = useSelector((state) => state.theme.mode);
  const dispatch = useDispatch();

  return (
    <>
      <div
        className="flex items-center gap-2 p-2 mt-3 cursor-pointer"
        onClick={() => dispatch(toggleTheme())}
        role="button"
        aria-label={theme === "dark" ? "light" : "dark"}
        tabIndex={0}
      >
        <div>
          {theme === "dark" ? (
            <MdOutlineWbSunny className="h-5 w-5 animate-rotate-360 delay-[0.8s]" />
          ) : (
            <MdOutlineNightsStay className="h-5 w-5 animate-rotate-360 delay-[0.8s]" />
          )}
        </div>
        <div>
          {theme === "dark" ? (
            <p>Switch Light Mode</p>
          ) : (
            <p>Switch Dark Mode</p>
          )}
        </div>
      </div>
    </>
  );
};
export default ToggleTheme;
