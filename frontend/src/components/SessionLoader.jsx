import Loader from "react-js-loader";

const SessionLoader = () => {
  return (
    <>
      <div className="flex items-center justify-center h-[100vh] w-[100%] ">
        <div className={"item"}>
          <Loader
            type="spinner-circle"
            bgColor="#171717"
            color="#efefef"
            title={"Hang tight, we're fetching your data!"}
            size={100}
          />
        </div>
      </div>
    </>
  );
};
export default SessionLoader;
